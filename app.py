import os
import importlib
import logging
from flask import Flask, render_template, request, make_response, url_for, session, redirect, flash, Response, current_app, jsonify, send_file
from fpdf import FPDF, XPos, YPos
from fpdf.enums import XPos, YPos
from modules.module1 import module1
from modules.module2 import module2
from modules.module3 import module3 
from modules.module4 import module4
from modules.module5 import module5
from modules.module6 import module6
from config.pflegegrad_config import MODULE_WEIGHTS
from config.benefits_data import pflegegrad_benefits
from utils import calculations

# Configure logging (basic configuration)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__) # Create a logger instance named after the current module

app = Flask(__name__)
app.secret_key = os.urandom(24)

all_modules = {
    1: module1,
    2: module2,
    3: module3,
    4: module4,
    5: module5,
    6: module6,
}
TOTAL_MODULES = len(all_modules)

# Adjust the path if necessary
FONT_DIR = os.path.join(os.path.dirname(__file__), 'fonts')
DEJAVU_REGULAR = os.path.join(FONT_DIR, 'DejaVuSans.ttf')
DEJAVU_BOLD = os.path.join(FONT_DIR, 'DejaVuSans-Bold.ttf')
DEJAVU_ITALIC = os.path.join(FONT_DIR, 'DejaVuSans-Oblique.ttf') # Added Italic path

# --- Routes ---

@app.route('/')
def intro():
    """Displays the introduction page and clears previous session data."""
    # Clear all relevant session data for a new assessment
    session.pop('module_answers', None) # Use the key you actually use to store answers
    session.pop('scores', None)         # Use the key you actually use to store calculation results
    session.pop('client_info', None)
    session.pop('final_notes', None)
    session.pop('current_module_index', None) # Clear module progress tracker
    # Add any other session keys you might use that need clearing here

    current_app.logger.info("Session cleared for new assessment.") # Optional: Log that session was cleared
    return render_template('intro.html')


# --- Update module_page_submit function ---
# --- Route for DISPLAYING module page (GET requests) ---
@app.route('/module/<int:module_id>', methods=['GET']) # Removed endpoint='module_page' unless you specifically need it elsewhere
def module_page(module_id):
    """Displays the page for a specific module."""

    if module_id not in all_modules:
        flash("Ungültiges Modul.", "danger")
        return redirect(url_for('module_page', module_id=1)) # Redirect to first module

    module_data = all_modules[module_id]
    module_id_str = str(module_id)

    # Get existing answers for THIS module only, to pre-fill form
    all_session_answers = session.get('module_answers', {}) # Use 'answers' consistently
    current_module_answers = all_session_answers.get(module_id_str, {})

    # --- Calculate Simple Progress (Example) ---
    total_modules = 6 # Or len(all_modules)
    # Check which modules have *any* data saved (could be just 'visited' or actual answers)
    completed_modules = len([mid for mid in all_session_answers.keys() if mid.isdigit()])
    progress_percent = int((completed_modules / total_modules) * 100) if total_modules > 0 else 0
    print(f"DEBUG Progress: Module {module_id}, Session Keys: {list(all_session_answers.keys())}, Completed: {completed_modules}, Percent: {progress_percent}")
    # Or, more accurately, check for a 'visited' flag if you save one upon submission
    # completed_modules = len([mid for mid, data in all_session_answers.items() if mid.isdigit() and data.get('visited')])
    # Get notes for the current module if they exist
    current_notes = current_module_answers.get('notes', '')

  

    return render_template(
        'module_page.html',
        module=module_data,
        module_id=module_id,
        current_answers=current_module_answers, # Pass answers for this module
        current_notes=current_notes,
        progress_percent=progress_percent, # Pass simple progress
        total_modules=total_modules,
        
    )


# --- Route for HANDLING module submission (POST requests) ---
@app.route('/module/<int:module_id>/submit', methods=['POST'])
def module_page_submit(module_id):

    log.debug(f"--- Entering submit for module {module_id} ---") # Added marker

    """
    Handles the submission of answers for a specific module.
    Stores answers in the session using the new dictionary format.
    """
    if not 1 <= module_id <= TOTAL_MODULES:
        flash("Ungültige Modul-ID.", "danger")
        return redirect(url_for('module_page', module_id=1))

    # --- Load the correct module data ---
    try:
        # Dynamically import the module based on module_id
        module_data_import = importlib.import_module(f'modules.module{module_id}')
        # Access the module dictionary (assuming it's named 'moduleX')
        module_definition = getattr(module_data_import, f'module{module_id}')
    except (ImportError, AttributeError):
        flash(f"Fehler beim Laden der Moduldefinition für Modul {module_id}.", "danger")
        return redirect(url_for('module_page', module_id=1))

    # --- Initialize or retrieve session data ---
    if 'module_answers' not in session:
        session['module_answers'] = {}

    # Use module_id as string key for consistency
    module_id_str = str(module_id)
    if module_id_str not in session['module_answers']:
        session['module_answers'][module_id_str] = {}
        log.debug(f"Initialized new entry for module '{module_id_str}' in session['module_answers'].") # Added log
    

    current_module_answers = session['module_answers'][module_id_str]

    log.debug(f"Raw form data received for module {module_id}: {request.form.to_dict()}") # Log the entire form data

    # --- Process form data ---
    processed_questions = set() # Keep track of questions processed via radio buttons

    for key, value in request.form.items():
        # Check if the key is a question ID from the current module definition
        if key in module_definition['questions']:
            question_id = key
            # Store the selected score (which is the value submitted)
            current_module_answers[question_id] = value # Value is the score string ("0", "1", "3", etc.)
            processed_questions.add(question_id)

            # +++ ADD THIS LOGGING +++
            log.debug(f"  Processed radio/select: q_id='{question_id}', value='{value}'")
            # ++++++++++++++++++++++++

        # Check for frequency count input (e.g., "freq_count_5.1.1")
        elif key.startswith('freq_count_'):
            question_id = key.replace('freq_count_', '')
            if question_id in module_definition.get('questions', {}):
                freq_key = f"{question_id}_freq"
                if freq_key not in current_module_answers:
                    current_module_answers[freq_key] = {}
                count_val = value if value.isdigit() else '0'
                current_module_answers[freq_key]['count'] = count_val
                # +++ ADD THIS LOGGING +++
                log.debug(f"  Processed freq_count: q_id='{question_id}', count='{count_val}'")
                # ++++++++++++++++++++++++

        # Check for frequency unit input (e.g., "freq_unit_5.1.1")
        elif key.startswith('freq_unit_'):
            question_id = key.replace('freq_unit_', '')
            if question_id in module_definition.get('questions', {}):
                freq_key = f"{question_id}_freq"
                if freq_key not in current_module_answers:
                    current_module_answers[freq_key] = {}
                unit_val = value
                current_module_answers[freq_key]['unit'] = unit_val
                # +++ ADD THIS LOGGING +++
                log.debug(f"  Processed freq_unit: q_id='{question_id}', unit='{unit_val}'")
                # ++++++++++++++++++++++++

        # Check for notes (e.g., "module_3_notes") - Make sure name matches HTML form
        # Consider a more generic name like 'notes' if possible
        elif key == f"module_{module_id}_notes" or key == 'notes': # Check for both possible names
             notes_val = value.strip()
             current_module_answers['notes'] = notes_val
             # +++ ADD THIS LOGGING +++
             log.debug(f"  Processed notes: key='{key}', value='{notes_val}'")
             # ++++++++++++++++++++++++
        else:
             # +++ ADD THIS LOGGING +++
             log.debug(f"  Skipped unknown form key: '{key}' with value '{value}'") # Log unexpected keys
             # ++++++++++++++++++++++++


    # --- Handle frequency questions where count might determine score (Module 5 logic) ---
    # This logic might still need review later, but let's focus on data capture first
    if module_id == 5:
        log.debug("Applying specific Module 5 frequency logic...") # Added log
        for q_id, q_data in module_definition.get('questions', {}).items():
            if q_data.get('type') == 'frequency': # Use .get()
                # Ensure the base question ID exists even if only frequency was submitted
                if q_id not in current_module_answers:
                     current_module_answers[q_id] = None # Mark for calculation later
                     log.debug(f"  M5 Logic: Set base q_id '{q_id}' to None as it wasn't in form.") # Added log
                # Ensure the _freq key exists if the base question exists
                freq_key = f"{q_id}_freq"
                if freq_key not in current_module_answers:
                    # If base radio was selected but no freq count/unit submitted, add default freq info
                    current_module_answers[freq_key] = {'count': '0', 'unit': ''} # Or appropriate default
                    log.debug(f"  M5 Logic: Added default freq data for q_id '{q_id}' as it was missing.") # Added log


    # --- Update the session ---
    # +++ ADD THIS LOGGING +++
    log.debug(f"Final 'current_module_answers' for module {module_id} BEFORE saving to session: {current_module_answers}")
    # ++++++++++++++++++++++++
    session['module_answers'][module_id_str] = current_module_answers
    session.modified = True # Important!

    # +++ ADD THIS LOGGING +++
    log.debug(f"Session['module_answers']['{module_id_str}'] AFTER saving: {session['module_answers'].get(module_id_str)}")
    log.debug(f"--- Exiting submit for module {module_id} ---") # Added marker
    # ++++++++++++++++++++++++

    # --- Redirect to next step ---
    if module_id < TOTAL_MODULES:
        next_module_id = module_id + 1
        # flash(f"Modul {module_id} gespeichert. Weiter zu Modul {next_module_id}.", "success") # Optional: Keep flash message
        return redirect(url_for('module_page', module_id=next_module_id))
    else:
        # flash("Alle Module abgeschlossen. Ergebnisse werden berechnet.", "success") # Optional: Keep flash message
        return redirect(url_for('calculate'))
# --- Update calculate function ---
@app.route('/calculate')
def calculate():
    """
    Performs the Pflegegrad calculation using the stored answers
    and stores the results in the session. Redirects back to /results.
    """
    log.debug("Entered /calculate route")
    all_answers = session.get('module_answers')

    if not all_answers or not isinstance(all_answers, dict):
        flash("Keine Modulantworten gefunden. Bitte füllen Sie die Module zuerst aus.", "warning")
        log.warning("/calculate: module_answers not found or invalid in session.")
        # Redirect to the start if no answers are found
        return redirect(url_for('module_page', module_id=1))

    try:
        # Call the updated calculate_scores function
        log.debug(f"/calculate: Calling calculations.calculate_scores with keys: {list(all_answers.keys())}")
        results_data = calculations.calculate_scores(all_answers) # Use the imported module
        log.debug(f"/calculate: Received results_data: {results_data}")

        if results_data is None:
            # Handle calculation failure (error logged within calculate_scores)
            flash("Ein Fehler ist bei der Berechnung aufgetreten. Details siehe Server-Log.", "danger")
            log.error("/calculate: calculations.calculate_scores returned None.")
            session.pop('calculation_results', None) # Clear potentially stale results
            # Redirect back to results, which will then likely redirect to module 1
            return redirect(url_for('results'))
        else:
            # Store the entire results dictionary in the session
            session['calculation_results'] = results_data
            session.modified = True
            log.info(f"/calculate: Calculation successful. Stored results in session. Redirecting to /results.")
            return redirect(url_for('results'))

    except Exception as e:
        log.exception(f"/calculate: Unexpected error during calculation: {e}") # Log the full traceback
        flash(f"Ein unerwarteter Fehler ist bei der Berechnung aufgetreten: {e}", "danger")
        session.pop('calculation_results', None) # Clear potentially stale results
        # Redirect back to results, which will then likely redirect to module 1
        return redirect(url_for('results'))


@app.route('/results')
def results():
    """
    Displays the calculation results page.
    """
    log.debug("Entered /results route")
    # Retrieve the results dictionary calculated by /calculate
    results_data = session.get('calculation_results')

    if not results_data:
        log.warning("/results: 'calculation_results' not found in session. Redirecting to /calculate.")
        # If results aren't calculated yet, trigger calculation
        # Check if answers exist first, otherwise start over
        if 'module_answers' not in session or not session['module_answers']:
             flash("Bitte füllen Sie zuerst die Bewertungsmodule aus.", "warning")
             return redirect(url_for('module_page', module_id=1)) # Start from module 1
        else:
             return redirect(url_for('calculate')) # Trigger calculation

    # Clear calculation results from session after retrieving to prevent stale data on refresh?
    # Optional: session.pop('calculation_results', None)
    # If you pop it, refreshing /results will trigger /calculate again.
    # If you don't pop it, refreshing shows the same results until a new calculation is done.

    log.debug(f"/results: Rendering results.html with data: {results_data}")
    # Pass the entire results dictionary to the template under the key 'results'
    return render_template('results.html', results=results_data, module_weights=MODULE_WEIGHTS)

class ReportPDF(FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.alias_nb_pages() # Enable page numbering alias '{nb}'

        # --- Add TTF Fonts (Corrected) ---
        # Add Regular Font
        if os.path.exists(DEJAVU_REGULAR):
            self.add_font("DejaVu", "", DEJAVU_REGULAR) # Removed uni=True
        else:
            current_app.logger.error(f"REQUIRED Font file not found: {DEJAVU_REGULAR}. PDF generation may fail.")
            # Consider raising an error or using a guaranteed core font if essential font missing

        # Add Bold Font
        if os.path.exists(DEJAVU_BOLD):
            self.add_font("DejaVu", "B", DEJAVU_BOLD) # Removed uni=True
        else:
            current_app.logger.warning(f"Font file not found: {DEJAVU_BOLD}. Using Regular for Bold.")
            self.add_font("DejaVu", "B", DEJAVU_REGULAR) # Fallback to regular if bold missing

        # Add Italic Font (Optional but needed if using 'I' style)
        if os.path.exists(DEJAVU_ITALIC):
            self.add_font("DejaVu", "I", DEJAVU_ITALIC) # Removed uni=True
        else:
            current_app.logger.warning(f"Font file not found: {DEJAVU_ITALIC}. Using Regular for Italic.")
            self.add_font("DejaVu", "I", DEJAVU_REGULAR) # Fallback to regular if italic missing

        # Note: Bold-Italic ('BI') is not added. Avoid using it unless you add the font file.

    def header(self):
        self.set_font('DejaVu', 'B', 15)
        # Use new_x, new_y instead of ln=1
        self.cell(0, 10, 'Pflegegrad Management Bericht', border=0,
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        self.line(self.l_margin, self.get_y() + 2, self.w - self.r_margin, self.get_y() + 2)
        self.ln(10)

    def footer(self):
        self.set_y(-18)
        self.set_font('DejaVu', '', 8)
        contact1 = "Optimum Pflegeberatung | Verena Campbell | Verena.Campbell@optimum-pflegeberatung.de"
        contact2 = "Tel: 017384655025"
        self.line(self.l_margin, self.get_y() - 2, self.w - self.r_margin, self.get_y() - 2)
        # Use new_x, new_y instead of ln=1
        self.cell(0, 5, contact1, border=0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        self.cell(0, 5, contact2, border=0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        page_num_text = f'Seite {self.page_no()} / {{nb}}'
        # Use align='C' for centering, ln=0 removed (no explicit position change needed after last element)
        self.cell(0, 5, page_num_text, border=0, align='C')


# --- PDF Generation Route (Revised) ---
@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    """
    Generates a professional PDF report based on session data.
    Includes client info, consultant notes, branding, and uses UTF-8 fonts.
    """
    scores_data = session.get('calculation_results', {})
    answers_data = session.get('module_answers', {})
    client_info = session.get('client_info', {})
    final_notes = session.get('final_notes', '')

    if not scores_data or not answers_data:
        missing_data = []
        if not scores_data: missing_data.append("'calculation_results'")
        if not answers_data: missing_data.append("'module_answers'")
        log.error(f"PDF Generation failed: Missing data in session: {', '.join(missing_data)}")
        flash(f"Sitzungsdaten ({', '.join(missing_data)}) für PDF fehlen. Bitte Berechnung erneut durchführen.", "danger")
        return redirect(url_for('results'))

    try:
        final_total_score = scores_data.get('total_weighted', 0.0)
        pflegegrad = scores_data.get('pflegegrad', 0)
        module_scores = scores_data.get('module_scores', {})
        current_benefits_info = pflegegrad_benefits.get(pflegegrad, {})

        pdf = ReportPDF()
        pdf.set_auto_page_break(auto=True, margin=25)
        pdf.add_page()
        usable_width = pdf.w - pdf.l_margin - pdf.r_margin

        # --- Client Info Section ---
        if client_info:
            pdf.set_font('DejaVu', 'B', 14)
            pdf.cell(0, 10, 'Klienteninformationen', border='B', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L') # Fixed ln=1
            pdf.ln(4)
            pdf.set_font('DejaVu', '', 12)
            client_details = (
                f"Name: {client_info.get('name', 'N/A')}\n"
                f"Adresse: {client_info.get('address', 'N/A')}\n"
                f"Telefon: {client_info.get('phone', 'N/A')}"
            )
            pdf.multi_cell(usable_width, 7, client_details)
            pdf.ln(10)
        else:
             pdf.set_font('DejaVu', 'I', 10) # Using Italic - Requires Italic font to be loaded
             pdf.cell(0, 7, "(Keine Klienteninformationen angegeben)", new_x=XPos.LMARGIN, new_y=YPos.NEXT) # Fixed ln=1
             pdf.ln(10)

        # --- Summary Section ---
        pdf.set_font('DejaVu', 'B', 14)
        pdf.cell(usable_width, 10, "Zusammenfassung", border='B', new_x=XPos.LMARGIN, new_y=YPos.NEXT) # Fixed ln=1
        pdf.ln(4)
        pdf.set_font('DejaVu', '', 12)
        score_text = f"Gesamtpunktzahl (für Pflegegrad): {final_total_score:.2f}"
        pdf.cell(usable_width, 8, score_text, new_x=XPos.LMARGIN, new_y=YPos.NEXT) # Fixed ln=1
        pg_text = f"Ermittelter Pflegegrad: {pflegegrad}" if pflegegrad > 0 else "Ermittelter Pflegegrad: Kein Pflegegrad (unter 12.5 Punkte)"
        pdf.cell(usable_width, 8, pg_text, new_x=XPos.LMARGIN, new_y=YPos.NEXT) # Fixed ln=1
        pdf.ln(8)

        # --- Benefits Display Section ---
        if current_benefits_info and current_benefits_info.get('leistungen'):
             pdf.set_font('DejaVu', 'B', 14)
             benefit_title = f"Wichtige Leistungen bei Pflegegrad {pflegegrad}"
             date_range = current_benefits_info.get('date_range')
             if date_range:
                 benefit_title += f" ({date_range})"
             pdf.cell(usable_width, 10, benefit_title, border='B', new_x=XPos.LMARGIN, new_y=YPos.NEXT) # Fixed ln=1
             pdf.ln(4)
             pdf.set_font('DejaVu', '', 10)
             for item_dict in current_benefits_info.get('leistungen', []):
                 item_name = item_dict.get('name', '')
                 item_value = item_dict.get('value', '')
                 pdf.multi_cell(usable_width, 6, f"• {item_name}: {item_value}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
             pdf.ln(8)

        # --- Detailed Module Results Section ---
        pdf.set_font('DejaVu', 'B', 14)
        pdf.cell(usable_width, 10, "Detailergebnisse nach Modulen", border='B', new_x=XPos.LMARGIN, new_y=YPos.NEXT) # Fixed ln=1
        pdf.ln(4)

        sorted_module_ids = sorted([k for k in module_scores.keys() if k.isdigit()], key=int)

        for module_id_str in sorted_module_ids:
            module_id = int(module_id_str)
            module_info = all_modules.get(module_id)
            module_score_data = module_scores.get(module_id_str, {})
            module_answers = answers_data.get(module_id_str, {})

            # --- Defensive Checks for module_info structure ---
            if not module_info:
                current_app.logger.warning(f"PDF Generation: No module_info found for module ID {module_id}")
                continue # Skip this module

            if not isinstance(module_info, dict):
                 current_app.logger.error(f"PDF Generation Error: module_info for ID {module_id} is a {type(module_info)}, not a dict. Skipping.")
                 pdf.set_font('DejaVu', 'I', 9)
                 pdf.cell(usable_width, 5, f"Fehler: Ungültige Datenstruktur für Modul {module_id}.", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                 pdf.ln(4)
                 continue # Skip this module

            module_questions_data = module_info.get('questions')
            if not isinstance(module_questions_data, dict):
                 current_app.logger.error(f"PDF Generation Error: module_info['questions'] for ID {module_id} is a {type(module_questions_data)}, not a dict. Skipping questions.")
                 module_questions_data = {} # Set to empty dict to avoid further errors in this section

            # --- End Defensive Checks ---

            pdf.set_font('DejaVu', 'B', 12)
            module_name = module_info.get('title', f'Modul {module_id}')
            pdf.cell(usable_width, 8, f"--- {module_name} ---", new_x=XPos.LMARGIN, new_y=YPos.NEXT) # Fixed ln=1
            pdf.set_font('DejaVu', '', 10)

            raw_score = module_score_data.get('raw_score', 0.0)
            weighted_score = module_score_data.get('weighted_score', 0.0)

            pdf.cell(usable_width, 6, f"Rohpunkte: {float(raw_score):.1f}", new_x=XPos.LMARGIN, new_y=YPos.NEXT) # Fixed ln=1

            if module_id_str in ['2', '3']:
                combined_score = scores_data.get('combined_m2_m3_weighted', 0.0)
                contributing_note = ""
                # Simplified check - assumes weighted score is accurate
                if weighted_score == combined_score and combined_score > 0:
                     contributing_note = " (Zählt für Gesamtpunktzahl)"
                elif combined_score > 0:
                     contributing_note = " (Nicht für Gesamtpunktzahl berücksichtigt)"
                pdf.cell(usable_width, 6, f"Gewichtete Punkte: {float(weighted_score):.2f}{contributing_note}", new_x=XPos.LMARGIN, new_y=YPos.NEXT) # Fixed ln=1
            else:
                 pdf.cell(usable_width, 6, f"Gewichtete Punkte: {float(weighted_score):.2f}", new_x=XPos.LMARGIN, new_y=YPos.NEXT) # Fixed ln=1

            pdf.ln(2)
            pdf.set_font('DejaVu', 'B', 10)
            pdf.cell(usable_width, 6, "Antworten:", new_x=XPos.LMARGIN, new_y=YPos.NEXT) # Fixed ln=1
            pdf.set_font('DejaVu', '', 9)

            if isinstance(module_answers, dict) and module_answers:
                q_keys_numeric = sorted([k for k in module_answers if k.replace('.', '', 1).isdigit()], key=lambda k: float(k))

                for q_key in q_keys_numeric:
                    answer_data = module_answers[q_key]
                    # Use the checked module_questions_data
                    question_info = module_questions_data.get(q_key) # Safely get from the (potentially empty) dict
                    q_text = question_info.get('text', f'Frage {q_key}') if isinstance(question_info, dict) else f'Frage {q_key}'

                    if isinstance(answer_data, dict):
                        a_text = answer_data.get('text', 'N/A')
                        a_score = answer_data.get('score', 'N/A')
                        if 'count' in answer_data and 'unit' in answer_data:
                            count = answer_data.get('count', 'N/A')
                            unit = answer_data.get('unit', '').replace('pro ', '')
                            full_text = f"• {q_text}: {count}x {unit} ({a_score} Pkt.)"
                        else:
                            full_text = f"• {q_text}: {a_text} ({a_score} Pkt.)"
                        pdf.multi_cell(usable_width, 5, full_text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                    else:
                         pdf.multi_cell(usable_width, 5, f"• Frage {q_key}: Ungültige Antwortdaten", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            else:
                 pdf.cell(usable_width, 5, "- Keine Antworten für dieses Modul vorhanden.", new_x=XPos.LMARGIN, new_y=YPos.NEXT) # Fixed ln=1

            module_note = module_answers.get('notes', '')
            if module_note:
                pdf.ln(2)
                pdf.set_font('DejaVu', 'B', 10)
                pdf.cell(usable_width, 6, "Notizen:", new_x=XPos.LMARGIN, new_y=YPos.NEXT) # Fixed ln=1
                pdf.set_font('DejaVu', '', 9)
                pdf.multi_cell(usable_width, 5, module_note, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

            pdf.ln(6)

        # --- Final Consultant Notes Section ---
        if final_notes:
             if pdf.get_y() > (pdf.h - 50):
                 pdf.add_page()
             else:
                 pdf.ln(10)
             pdf.set_font('DejaVu', 'B', 14)
             pdf.cell(0, 10, 'Abschließende Notizen des Pflegeberaters', border='B', new_x=XPos.LMARGIN, new_y=YPos.NEXT) # Fixed ln=1
             pdf.ln(4)
             pdf.set_font('DejaVu', '', 12)
             pdf.multi_cell(usable_width, 7, final_notes)
             pdf.ln(10)

        # --- Output the PDF ---
        pdf_output_bytes = pdf.output(dest='S')
        log.info(f"PDF Generated successfully. Size: {len(pdf_output_bytes)} bytes")

        response = make_response(pdf_output_bytes)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=Pflegegrad_Bericht.pdf'
        return response

    except Exception as e:
        log.error(f"Error generating PDF: {e}", exc_info=True)
        flash(f"Ein interner Serverfehler ist bei der PDF-Erstellung aufgetreten: {e}", "danger")
        return redirect(url_for('results'))

# --- Your other routes ---
@app.route('/debug-session')
def debug_session():
    return f"<pre>{session.get('module_answers', 'Session data not found.')}</pre>"

# --- Add routes for Client Info and Final Notes (NEXT STEP) ---

if __name__ == '__main__':
    app.run(debug=True, port=5001)