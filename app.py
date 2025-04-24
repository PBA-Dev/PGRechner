import os
from flask import Flask, render_template, request, make_response, url_for, session, redirect, flash, Response, current_app, jsonify
from fpdf import FPDF, XPos, YPos
from fpdf.enums import XPos, YPos
from modules.module1 import module1
from modules.module2 import module2
from modules.module3 import module3
from modules.module4 import module4
from modules.module5 import module5
from modules.module6 import module6
from config.pflegegrad_config import pflegegrad_thresholds
from config.benefits_data import pflegegrad_benefits
from utils.calculations import  calculate_scores

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
    module_id_str = str(module_id)
    if module_id not in all_modules:
        flash("Ungültiges Modul.", "error")
        return redirect(url_for('intro'))

    module_data = all_modules[module_id]
    current_answers = session.get('module_answers', {}).get(module_id_str, {})

    # --- START: ADD DEBUG PRINT ---
    print(f"\n--- DEBUG Submit Start M{module_id_str} ---")
    print(f"DEBUG M{module_id_str}: Initial current_answers: {current_answers}")
    # --- END: ADD DEBUG PRINT ---
    # --- THIS IS THE NEW CODE BLOCK ---
    if module_id == 5:
        # --- Handle Module 5 (Frequency and Standard) ---
        for part in module_data.get('parts', []):
            for question in part.get('questions', []):
                question_key = question['id'] # Use the specific ID like '5.1.1'

                if question.get('type') == 'frequency':
                    count_str = request.form.get(f'freq_count_{question_key}')
                    unit = request.form.get(f'freq_unit_{question_key}')

                    count = 0
                    try:
                        if count_str:
                           count = float(count_str)
                           if count < 0: count = 0
                    except (ValueError, TypeError):
                        count = 0

                    current_answers[question_key] = {
                        'count': count,
                        'unit': unit if unit else ''
                    }
                    # Add text description (optional)
                    current_answers[question_key]['text'] = f"{count}x pro {unit}" if count > 0 and unit else "Entfällt/Selbständig"

                elif question.get('type') in ['radio', 'standard']: # Check for EITHER 'radio' OR 'standard'
                    question_key = question['id'] # e.g., '5.5.1'

                    # Assume the HTML input uses name="<question_id>", e.g., name="5.5.1"
                    selected_option_index_str = request.form.get(question_key) # Use the question ID directly as the key

                    if selected_option_index_str is not None and selected_option_index_str.strip() != '':
                        try:
                            selected_option_index = int(selected_option_index_str)
                            options = question.get('options', [])
                            if 0 <= selected_option_index < len(options):
                                selected_option = options[selected_option_index]
                                # Save the data using the question_key (e.g., '5.5.1')
                                current_answers[question_key] = {
                                    # 'option_index': selected_option_index, # You can uncomment this if you need the index later
                                    'text': selected_option.get('text', 'N/A'),
                                    'score': selected_option.get('score', 0)
                                }
                                print(f"DEBUG: Saved answer for {question_key}: {current_answers[question_key]}") # Add debug print
                            else:
                                 print(f"DEBUG: Invalid index {selected_option_index} for {question_key}")
                        except (ValueError, TypeError):
                             print(f"DEBUG: Invalid value '{selected_option_index_str}' for {question_key}")
                             pass # Ignore if index is not a valid integer
                    else:
                        print(f"DEBUG: No answer submitted for {question_key}")
                        # Optionally save a default 'not answered' state if needed
                        # current_answers[question_key] = {'text': 'Nicht beantwortet', 'score': 0}
                # else: handle other types if they exist

    else:
        # --- Handle Standard Modules (1, 2, 3, 4, 6) ---
        for question_index, question in enumerate(module_data.get('questions', [])):
            question_index_str = str(question_index)
            answer_key = f'answer_{module_id_str}_{question_index_str}'
            selected_option_index_str = request.form.get(answer_key)

            if selected_option_index_str is not None:
                try:
                    selected_option_index = int(selected_option_index_str)
                    options = question.get('options', [])
                    if 0 <= selected_option_index < len(options):
                        selected_option = options[selected_option_index]
                        current_answers[question_index_str] = {
                            'option_index': selected_option_index,
                            'text': selected_option.get('text', ''),
                            'score': selected_option.get('score', 0)
                        }
                except ValueError:
                    pass
    # --- END OF NEW CODE BLOCK ---

    # --- Store Notes --- (Keep your existing logic here)
    notes_key = f'module_{module_id_str}_notes'
    notes_text = request.form.get(notes_key, '').strip()
    # --- START: ADD DEBUG PRINTS for Notes ---
    print(f"DEBUG M{module_id_str}: Notes Key Checked: '{notes_key}'")
    print(f"DEBUG M{module_id_str}: Notes Text Retrieved: '{notes_text}'")
    # --- END: ADD DEBUG PRINTS for Notes ---
    if notes_text:
        current_answers['notes'] = notes_text # Add notes to the temporary dict

    # Mark module as visited (Add this to the temporary dict)
    current_answers['visited'] = True

    # --- Update session data --- (Update the session with the temporary dict)
    if 'module_answers' not in session:
        session['module_answers'] = {}
    # Replace the entire entry for this module with the new answers
    session['module_answers'][module_id_str] = current_answers
    session.modified = True # Ensure session is saved

    # --- Determine next step --- (Keep your existing logic here)
    next_module_id = module_id + 1
    print(f"DEBUG Submit Check: module_id={module_id}, next_module_id={next_module_id}, TOTAL_MODULES={TOTAL_MODULES}")
    if next_module_id > TOTAL_MODULES:
        return redirect(url_for('calculate'))
    else:
        # Redirect to the GET endpoint for the next module
        return redirect(url_for('module_page', module_id=next_module_id))

# --- Update calculate function ---
@app.route('/calculate')
def calculate():
    """
    Triggers the calculation of all scores and the Pflegegrad.
    Delegates the actual calculation to utils.calculations.calculate_scores.
    Stores the results in the session and redirects to the results page.
    """
    # Use 'answers' as the session key consistently
    if 'module_answers' not in session or not session['module_answers']:
        flash("Bitte füllen Sie zuerst die Module aus.", "warning")
        # Redirect to the first module page or an intro page
        return redirect(url_for('module_page', module_id=1)) # Or your intro route

    all_answers_from_session = session.get('module_answers', {})

    # Call the single function from utils/calculations.py to do ALL calculations
    try:
        calculated_scores_dict = calculate_scores(all_answers_from_session)
    except Exception as e:
        # Log the error for debugging
        print(f"ERROR during calculation: {e}")
        flash("Ein Fehler ist bei der Berechnung aufgetreten. Bitte versuchen Sie es erneut.", "danger")
        # Redirect back to the last module or start page
        # Find the last answered module if possible, otherwise default
        last_module = max([int(k) for k in all_answers_from_session.keys() if k.isdigit()] or [0])
        if last_module > 0:
             return redirect(url_for('module_page', module_id=last_module))
        else:
             return redirect(url_for('module_page', module_id=1)) # Or intro

    # Store the complete results dictionary in the session
    session['scores'] = calculated_scores_dict
    session.modified = True # Mark session as modified

    print("DEBUG: Calculation complete via calculate_scores, redirecting to results.")
    # Redirect to the route that will display the results
    return redirect(url_for('results'))

# --- Your /results Route (handles displaying the calculated scores) ---
@app.route('/results')
def results():
    """Displays the final results and Pflegegrad."""
    if 'scores' not in session:
        flash("Berechnungsergebnisse nicht gefunden. Bitte füllen Sie zuerst die Module aus.", "warning")
        # Redirect to calculate, which will handle missing answers
        return redirect(url_for('calculate'))

    # Get the calculated scores and original answers from the session
    scores_data = session.get('scores', {})
    answers_data = session.get('module_answers', {}) # Needed to show the user's answers

    # Extract key results for easier access in the template (optional)
    final_score = scores_data.get('total_weighted', 0.0)
    pflegegrad = scores_data.get('pflegegrad', 0)

    # --- Fetch Benefits Data (This logic belongs here, not in /calculate) ---
    # Import your benefits data structure
    # from data.benefits import pflegegrad_benefits # Example import
    # Define or import pflegegrad_benefits = { ... }
    # benefits_for_pg = pflegegrad_benefits.get(pflegegrad, {})
    # current_benefits = benefits_for_pg # Add logic for periods if needed

    # --- Aggregate Notes (This logic belongs here) ---
    aggregated_notes = {
        mid: data.get('notes', '')
        for mid, data in answers_data.items()
        if isinstance(data, dict) and data.get('notes')
    }


    #print("-" * 40) # Separator for clarity
    #print(f"DEBUG Results Route: Data being passed to template:")
    #print(f"  results (scores_data): {scores_data}")
    #print(f"  answers (answers_data): {answers_data}")
    #print(f"  all_modules keys: {list(all_modules.keys())}") # Check if modules loaded
    #print(f"  notes: {aggregated_notes}")
    #print("-" * 40) # Separator

    # Render the results template, passing all necessary data
    return render_template(
        'results.html', # Make sure your template is named results.html
        results=scores_data, # Pass the whole scores dictionary
        answers=answers_data, # Pass the original answers
        all_modules=all_modules, # Pass module definitions for displaying question text
        notes=aggregated_notes,
        # benefits=current_benefits # Pass benefits data
        pflegegrad=pflegegrad # Pass pflegegrad for convenience
    )

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
    scores_data = session.get('scores', {})
    answers_data = session.get('module_answers', {})
    client_info = session.get('client_info', {})
    final_notes = session.get('final_notes', '')

    if not scores_data or not answers_data:
         current_app.logger.error("PDF Generation failed: Missing scores or answers data in session.")
         return jsonify({"error": "Sitzungsdaten für PDF fehlen. Bitte Berechnung erneut durchführen."}), 400

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

            raw_score = module_score_data.get('raw', 0.0)
            weighted_score = module_score_data.get('weighted', 0.0)

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
        pdf_output_bytes = bytes(pdf.output())
        current_app.logger.info(f"PDF Generated successfully. Type: {type(pdf_output_bytes)}")
        return Response(
            pdf_output_bytes,
            mimetype='application/pdf',
            headers={'Content-Disposition': 'attachment;filename=Pflegegrad_Bericht.pdf'}
        )

    except Exception as e:
        current_app.logger.error(f"Error generating PDF: {e}", exc_info=True)
        return jsonify({"error": f"Ein interner Serverfehler ist bei der PDF-Erstellung aufgetreten: {e}"}), 500

# --- Your other routes ---


# --- Add routes for Client Info and Final Notes (NEXT STEP) ---

if __name__ == '__main__':
    app.run(debug=True, port=5001)