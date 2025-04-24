import os
from flask import Flask, render_template, request, make_response, url_for, session, redirect, flash, Response, current_app, jsonify
from fpdf import FPDF
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


# --- Routes ---

@app.route('/')
def intro():
    """Displays the introduction page."""
    # Clear any previous session data at the start
    session.pop('answers', None)
    session.pop('results', None)
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
    current_answers = session.get('answers', {}).get(module_id_str, {})
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


    print("-" * 40) # Separator for clarity
    print(f"DEBUG Results Route: Data being passed to template:")
    print(f"  results (scores_data): {scores_data}")
    print(f"  answers (answers_data): {answers_data}")
    print(f"  all_modules keys: {list(all_modules.keys())}") # Check if modules loaded
    print(f"  notes: {aggregated_notes}")
    print("-" * 40) # Separator

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

# --- PDF Generation Route ---
@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    """
    Generates a PDF document based on the calculation results provided in the request body.
    Handles M5 frequency, notes, benefits. Uses updated FPDF2 syntax.
    Includes type checking for pdf.output() result.
    """
    data = None
    try:
        data = request.get_json(silent=True)
        if data is None:
            raw_data = request.data.decode('utf-8', errors='ignore')
            current_app.logger.error(f"Invalid or empty JSON received for PDF. Raw data received: '{raw_data}'")
            return jsonify({"error": "Invalid or empty JSON data received."}), 400

        current_app.logger.info(f"Successfully parsed JSON data for PDF generation. Keys: {list(data.keys())}")

        # --- Extract data safely ---
        detailed_results = data.get('detailed_results', {})
        final_total_score = float(data.get('final_total_score', 0.0))
        pflegegrad = int(data.get('pflegegrad', 0))
        benefits_data = data.get('benefits', {})
        notes_data = data.get('notes', {}) # Aggregated notes { '1': 'note', ... }

        # --- PDF Generation Logic ---
        pdf = FPDF()
        pdf.add_page()
        usable_width = pdf.w - pdf.l_margin - pdf.r_margin
        pdf.set_font("Arial", size=12) # Using core font

        # --- Title ---
        pdf.set_font("Arial", 'B', 16)
        pdf.multi_cell(usable_width, 10, "Pflegegradrechner - Ergebnisbericht".encode('latin-1', 'replace').decode('latin-1'),
                       align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(10)

        # --- Summary ---
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(usable_width, 10, "Zusammenfassung".encode('latin-1', 'replace').decode('latin-1'),
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("Arial", size=12)
        score_text = f"Gesamtpunktzahl (fuer Pflegegrad): {final_total_score:.2f}"
        pdf.cell(usable_width, 8, score_text.encode('latin-1', 'replace').decode('latin-1'),
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pg_text = f"Ermittelter Pflegegrad: {pflegegrad}" if pflegegrad > 0 else "Ermittelter Pflegegrad: Kein Pflegegrad (unter 12.5 Punkte)"
        pdf.cell(usable_width, 8, pg_text.encode('latin-1', 'replace').decode('latin-1'),
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(5)

        # --- Benefits Display ---
        if benefits_data and benefits_data.get('leistungen'):
             pdf.set_font("Arial", 'B', 12)
             benefit_title = f"Wichtige Leistungen bei Pflegegrad {pflegegrad}"
             date_range = benefits_data.get('date_range')
             if date_range:
                 benefit_title += f" ({date_range})"
             pdf.cell(usable_width, 10, benefit_title.encode('latin-1', 'replace').decode('latin-1'),
                      new_x=XPos.LMARGIN, new_y=YPos.NEXT)
             pdf.set_font("Arial", size=10)
             for item_dict in benefits_data.get('leistungen', []):
                 item_name = item_dict.get('name', '')
                 item_value = item_dict.get('value', '')
                 pdf.multi_cell(usable_width, 6, f"- {item_name}: {item_value}".encode('latin-1', 'replace').decode('latin-1'),
                                new_x=XPos.LMARGIN, new_y=YPos.NEXT)
             pdf.ln(5)

        # --- Detailed Results ---
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(usable_width, 10, "Detailergebnisse nach Modulen".encode('latin-1', 'replace').decode('latin-1'),
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        module_answers_all = detailed_results.get('module_answers', {})
        module_scores_raw = detailed_results.get('module_scores_raw', {})
        module_scores_weighted = detailed_results.get('module_scores_weighted', {})
        which_module_contributed = detailed_results.get('which_module_contributed_m2_m3')

        if isinstance(module_answers_all, dict):
            for module_id_str in sorted(module_answers_all.keys(), key=lambda x: int(x) if x.isdigit() else 999):
                if not module_id_str.isdigit(): continue

                module_id = int(module_id_str)
                module_info = all_modules.get(module_id)
                module_answers = module_answers_all.get(module_id_str, {})

                if not module_info: continue

                pdf.set_font("Arial", 'B', 11)
                module_name = module_info.get('name', f'Modul {module_id}')
                pdf.cell(usable_width, 8, f"--- {module_name.encode('latin-1', 'replace').decode('latin-1')} ---",
                         new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                pdf.set_font("Arial", size=10)

                raw_score = module_scores_raw.get(module_id_str, 0.0)
                weighted_score = module_scores_weighted.get(module_id_str, 0.0)

                pdf.cell(usable_width, 6, f"Rohpunkte: {float(raw_score):.1f}".encode('latin-1', 'replace').decode('latin-1'),
                         new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                pdf.cell(usable_width, 6, f"Gewichtete Punkte: {float(weighted_score):.2f}".encode('latin-1', 'replace').decode('latin-1'),
                         new_x=XPos.LMARGIN, new_y=YPos.NEXT)

                if module_id_str in ['2', '3']:
                    note_text = "(Nicht fuer Gesamtpunktzahl beruecksichtigt)"
                    if which_module_contributed is not None and module_id == which_module_contributed:
                        note_text = "(Dieser Wert zaehlt fuer die Gesamtpunktzahl)"
                    pdf.set_font("Arial", 'I', 9)
                    pdf.cell(usable_width, 5, note_text.encode('latin-1', 'replace').decode('latin-1'),
                             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                    pdf.set_font("Arial", size=10)

                pdf.ln(2)
                pdf.set_font("Arial", 'B', 10)
                pdf.cell(usable_width, 6, "Antworten:".encode('latin-1', 'replace').decode('latin-1'),
                         new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                pdf.set_font("Arial", size=9)

                if isinstance(module_answers, dict) and module_answers:
                    try:
                        sorted_q_keys = sorted(module_answers.keys(), key=lambda k: int(k) if k.isdigit() else float('inf'))
                    except ValueError:
                         sorted_q_keys = sorted(module_answers.keys())

                    for q_key in sorted_q_keys:
                        if q_key == 'notes': continue

                        answer_data = module_answers[q_key]
                        if isinstance(answer_data, dict):
                            q_text = answer_data.get('question', f'Frage {q_key}')
                            a_text = answer_data.get('answer_text', 'N/A')
                            a_score = answer_data.get('score', 'N/A')

                            if answer_data.get('type') == 'frequency':
                                count = answer_data.get('count', 'N/A')
                                unit = answer_data.get('unit', 'N/A')
                                full_text = f"- {q_text}: {count}x pro {unit} ({a_score} Rohpunkte)"
                            else:
                                full_text = f"- {q_text}: {a_text} ({a_score} Rohpunkte)"

                            pdf.multi_cell(usable_width, 5, full_text.encode('latin-1', 'replace').decode('latin-1'),
                                           new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                        else:
                             pdf.multi_cell(usable_width, 5, f"- Frage {q_key}: Ungültige Antwortdaten".encode('latin-1', 'replace').decode('latin-1'),
                                            new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                else:
                     pdf.cell(usable_width, 5, "- Keine Antworten fuer dieses Modul vorhanden.".encode('latin-1', 'replace').decode('latin-1'),
                              new_x=XPos.LMARGIN, new_y=YPos.NEXT)

                # Display Notes for Module
                module_note = notes_data.get(module_id_str, '')
                if module_note:
                    pdf.ln(2)
                    pdf.set_font("Arial", 'B', 10)
                    pdf.cell(usable_width, 6, "Notizen:".encode('latin-1', 'replace').decode('latin-1'),
                             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                    pdf.set_font("Arial", size=9)
                    pdf.multi_cell(usable_width, 5, module_note.encode('latin-1', 'replace').decode('latin-1'),
                                   new_x=XPos.LMARGIN, new_y=YPos.NEXT)

                pdf.ln(4)
        else:
            pdf.set_font("Arial", 'I', 10)
            pdf.multi_cell(usable_width, 6, "Fehler: Detaillierte Antworten konnten nicht geladen werden.".encode('latin-1', 'replace').decode('latin-1'),
                           new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # --- Output the PDF ---
        # pdf.output() should return bytes. Add checks and conversion.
        pdf_data = pdf.output()
        current_app.logger.info(f"Type returned by pdf.output(): {type(pdf_data)}") # Log the type

        # Ensure it's bytes before returning
        if isinstance(pdf_data, bytes):
            pdf_output_bytes = pdf_data
        elif isinstance(pdf_data, bytearray):
             pdf_output_bytes = bytes(pdf_data) # Convert bytearray to bytes
        else:
            # This case should ideally not happen with modern fpdf2
            current_app.logger.error(f"pdf.output() returned unexpected type: {type(pdf_data)}. Attempting encoding.")
            # Fallback: try encoding if it's somehow a string (less likely)
            try:
                pdf_output_bytes = str(pdf_data).encode('latin-1', 'replace')
            except Exception as enc_err:
                 current_app.logger.error(f"Fallback encoding failed: {enc_err}", exc_info=True)
                 # Raise an error that will be caught by the outer try/except
                 raise ValueError("Failed to get PDF output as bytes")

        # Log the type *after* potential conversion
        current_app.logger.info(f"Type being passed to Response: {type(pdf_output_bytes)}")

        return Response(
            pdf_output_bytes, # Pass the verified/converted bytes
            mimetype='application/pdf',
            headers={'Content-Disposition': 'attachment;filename=pflegegrad_results.pdf'}
        )

    except Exception as e:
        current_app.logger.error(f"Error generating PDF: {e}", exc_info=True)
        return jsonify({"error": f"An internal server error occurred during PDF generation: {e}"}), 500

# ... (rest of app.py, including if __name__ == '__main__':) ...
# ... (rest of app.py, including if __name__ == '__main__':) ...

if __name__ == '__main__':
    app.run(debug=True, port=5001)