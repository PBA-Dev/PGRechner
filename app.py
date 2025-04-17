import os
import json
import logging
from flask import Flask, render_template, request, make_response, url_for, session, redirect, flash, Response, current_app, jsonify
#from werkzeug.exceptions import BadRequest
from fpdf import FPDF
from modules.module1 import module1
from modules.module2 import module2
from modules.module3 import module3
from modules.module4 import module4
from modules.module5 import module5
from modules.module6 import module6
from config.pflegegrad_config import pflegegrad_thresholds

app = Flask(__name__)
# Secret key is needed for session management
# In a real app, use a strong, environment-variable-based secret key
app.secret_key = os.urandom(24) # Generates a random key each time app starts

# Combine all modules (consider using OrderedDict if order matters explicitly)
# Python dictionaries maintain insertion order from 3.7+
all_modules = {
    1: module1,
    2: module2,
    3: module3,
    4: module4,
    5: module5,
    6: module6,
}
TOTAL_MODULES = len(all_modules)

# In app.py
# ... (imports, config) ...

# --- NBA Raw Points to Weighted Points Mapping ---
# Structure: { module_id: [(raw_upper_bound, weighted_points), ...], ... }
# Ranges are checked as: if raw_score <= raw_upper_bound
RAW_TO_WEIGHTED_MAPPING = {
    '1': [ # Modul 1: Mobilität
        (1, 0.0),
        (3, 2.5),
        (5, 5.0),
        (9, 7.5),
        (15, 10.0) # Max raw 15
    ],
    '2': [ # Modul 2: Kognitive und kommunikative Fähigkeiten
        (1, 0.0),
        (5, 3.75),
        (10, 7.5),
        (16, 11.25),
        (33, 15.0) # Max raw 33
    ],
    '3': [ # Modul 3: Verhaltensweisen und psychische Problemlagen
        (0, 0.0),   # Explicitly 0 raw points = 0 weighted
        (2, 3.75),  # 1-2 raw points
        (4, 7.5),   # 3-4 raw points
        (6, 11.25), # 5-6 raw points
        (65, 15.0)  # 7-65 raw points (Max raw 65)
    ],
    '4': [ # Modul 4: Selbstversorgung
        (2, 0.0),
        (7, 10.0),
        (18, 20.0),
        (36, 30.0),
        (54, 40.0) # Max raw 54
    ],
    '5': [ # Modul 5: Umgang mit krankheits-/therapiebedingten Anforderungen
        (0, 0.0),
        (1, 5.0),
        (3, 10.0),
        (5, 15.0),
        (15, 20.0) # Max raw 15
    ],
    '6': [ # Modul 6: Gestaltung des Alltagslebens und sozialer Kontakte
        (0, 0.0),
        (3, 3.75),
        (6, 7.5),
        (11, 11.25),
        (18, 15.0) # Max raw 18
    ]
}

# ... (rest of app setup: all_modules, TOTAL_MODULES, pflegegrad_thresholds) ...

# In app.py
# ... (imports, config, RAW_TO_WEIGHTED_MAPPING) ...

def _get_weighted_score_from_raw(module_id_str, raw_score):
    """Looks up the weighted score based on the raw score for a given module."""
    mapping = RAW_TO_WEIGHTED_MAPPING.get(module_id_str)
    if mapping is None:
        return 0.0 # Module not found in mapping

    # Ensure raw_score is a number (float for comparison)
    try:
        raw_score = float(raw_score)
    except (ValueError, TypeError):
        return 0.0 # Invalid raw score

    # Iterate through the sorted mapping (lowest upper bound first)
    for upper_bound, weighted_points in mapping:
        if raw_score <= upper_bound:
            return float(weighted_points) # Return as float

    # If raw_score exceeds the highest upper bound (shouldn't happen with valid data)
    # Return the highest possible weighted score for that module as a fallback
    return float(mapping[-1][1]) if mapping else 0.0

# ... (rest of app setup) ...

# ... (other imports) ...

# In app.py

# --- Helper Function ---
def _calculate_current_score(answers_dict, all_modules_config):
    """Calculates the estimated FINAL NBA score based on current answers using range mapping."""
    if not answers_dict:
        return 0.0

    module_scores_raw = {}
    module_scores_weighted = {} # Store weighted scores per module

    # 1. Calculate raw scores for answered modules
    for module_id_str, module_answers in answers_dict.items():
        if not module_answers: continue

        module_id = int(module_id_str)
        current_module = all_modules_config.get(module_id)
        if not current_module: continue

        module_total_raw = 0.0
        for q_idx_str, answer_data in module_answers.items():
            if answer_data is not None:
                try:
                    module_total_raw += float(answer_data.get('score', 0))
                except (ValueError, TypeError):
                    pass # Ignore non-numeric scores if they somehow occur

        module_scores_raw[module_id_str] = module_total_raw

        # 2. Map raw score to weighted score for this module
        module_scores_weighted[module_id_str] = _get_weighted_score_from_raw(
            module_id_str, module_total_raw
        )

    # --- Apply NBA Final Score Calculation Logic ---
    weighted_m1 = module_scores_weighted.get('1', 0.0)
    weighted_m2 = module_scores_weighted.get('2', 0.0)
    weighted_m3 = module_scores_weighted.get('3', 0.0)
    weighted_m4 = module_scores_weighted.get('4', 0.0)
    weighted_m5 = module_scores_weighted.get('5', 0.0)
    weighted_m6 = module_scores_weighted.get('6', 0.0)

    # 3. Determine higher WEIGHTED score between M2 and M3
    higher_weighted_score_m2_m3 = max(weighted_m2, weighted_m3)

    # 4. Sum the weighted points that contribute
    current_final_score_estimate = (
        weighted_m1 +
        higher_weighted_score_m2_m3 +
        weighted_m4 +
        weighted_m5 +
        weighted_m6
    )

    # Return the rounded final estimated score
    return round(current_final_score_estimate, 2)

# --- Routes ---
# ... (intro route) ...
# ... (module_page route - no changes needed here, it calls the corrected helper) ...

@app.route('/')
def intro():
    """Displays the introduction page."""
    # Clear any previous session data at the start
    session.pop('answers', None)
    session.pop('results', None)
    return render_template('intro.html')

# In app.py

# ... (helper function above) ...

# In app.py

# ... (imports, helper function, intro route) ...

# In app.py

# ... (imports, helper function, intro route) ...

@app.route('/module/<int:module_id>', methods=['GET', 'POST'])
def module_page(module_id):
    """Displays questions for a specific module and handles submission."""

    # --- Initial Checks ---
    if module_id < 1 or module_id > TOTAL_MODULES:
        flash("Ungültiges Modul.", "error")
        return redirect(url_for('intro'))

    # --- Define current_module EARLY ---
    current_module = all_modules.get(module_id)
    if not current_module:
        # This check should ideally happen right after getting the module
        flash(f"Modul {module_id} nicht gefunden.", "error")
        return redirect(url_for('intro'))

    # --- Session and Score Setup ---
    if 'answers' not in session:
        session['answers'] = {}

    current_answers_in_session = session.get('answers', {})
    # Calculate score based on session data *before* POST processing
    current_estimated_score = _calculate_current_score(current_answers_in_session, all_modules)
    max_score = 100.0

    # --- POST Request Handling ---
    if request.method == 'POST':
        module_answers = {}
        all_questions_answered = True

        # Loop through questions (using the 'current_module' defined above)
        for q_idx, question in enumerate(current_module['questions']):
            # ... (logic to get score_str, handle None, store in module_answers) ...
            answer_key = f"module_{module_id}_question_{q_idx}"
            score_str = request.form.get(answer_key)

            if score_str is None:
                all_questions_answered = False
                module_answers[str(q_idx)] = None
            else:
                 try:
                    score = int(score_str)
                    option_found = False
                    for option in question['options']:
                        if option['score'] == score:
                            answer_text = option['text']
                            option_found = True
                            break
                    if not option_found:
                        score = 0
                        answer_text = "Ungültige Auswahl"

                    module_answers[str(q_idx)] = {
                        'question': question['question'],
                        'score': score,
                        'answer_text': answer_text
                    }
                 except ValueError:
                    all_questions_answered = False
                    module_answers[str(q_idx)] = None


        session['answers'][str(module_id)] = module_answers
        session.modified = True

        # --- Validation Check ---
        if not all_questions_answered:
             flash("Bitte beantworten Sie alle Fragen, bevor Sie fortfahren.", "warning")
             current_answers_for_template = session['answers'].get(str(module_id), {})
             # Recalculate score needed for re-rendering
             current_estimated_score = _calculate_current_score(session.get('answers', {}), all_modules)
             # Render the SAME module page again
             return render_template('module_page.html',
                                    # 'current_module' MUST be defined by this point
                                    module=current_module,
                                    module_id=module_id,
                                    total_modules=TOTAL_MODULES,
                                    current_answers=current_answers_for_template,
                                    current_estimated_score=current_estimated_score,
                                    pflegegrad_thresholds=pflegegrad_thresholds,
                                    max_score=max_score) # Error occurred here

        # --- Redirect on Success ---
        if module_id < TOTAL_MODULES:
            next_module_id = module_id + 1
            return redirect(url_for('module_page', module_id=next_module_id))
        else:
            return redirect(url_for('calculate'))

    # --- GET Request Handling ---
    # 'current_module' is already defined from above
    current_answers_for_template = session['answers'].get(str(module_id), {})
    # Score calculation for GET is also done above
    return render_template('module_page.html',
                           module=current_module,
                           module_id=module_id,
                           total_modules=TOTAL_MODULES,
                           current_answers=current_answers_for_template,
                           current_estimated_score=current_estimated_score,
                           pflegegrad_thresholds=pflegegrad_thresholds,
                           max_score=max_score)

# ... (rest of app.py) ...# ... (calculate route) ...
# ... (generate_pdf route) ...
# ... (if __name__ == '__main__':) ...
# In app.py

# ... (imports, config, RAW_TO_WEIGHTED_MAPPING, helpers, intro, module_page routes) ...

@app.route('/calculate')
def calculate():
    """Calculates the final NBA score and determines the Pflegegrad using range mapping."""
    if 'answers' not in session or not session['answers']:
        flash("Keine Antworten vorhanden, um den Pflegegrad zu berechnen.", "warning")
        return redirect(url_for('intro'))

    # --- Calculate Raw Scores for all modules ---
    module_scores_raw = {}
    for module_id_str, module_answers in session.get('answers', {}).items():
        if not module_answers: continue

        module_id = int(module_id_str)
        current_module = all_modules.get(module_id)
        if not current_module: continue

        module_total_raw = 0.0
        for q_idx_str, answer_data in module_answers.items():
             if answer_data is not None:
                try:
                    module_total_raw += float(answer_data.get('score', 0))
                except (ValueError, TypeError):
                    pass

        module_scores_raw[module_id_str] = module_total_raw

    # --- Determine Weighted Scores using Mapping ---
    weighted_scores = {}
    for module_id_str, raw_score in module_scores_raw.items():
        weighted_scores[module_id_str] = _get_weighted_score_from_raw(
            module_id_str, raw_score
        )

    # --- Apply Final Calculation Logic ---
    weighted_m1 = weighted_scores.get('1', 0.0)
    weighted_m2 = weighted_scores.get('2', 0.0)
    weighted_m3 = weighted_scores.get('3', 0.0)
    weighted_m4 = weighted_scores.get('4', 0.0)
    weighted_m5 = weighted_scores.get('5', 0.0)
    weighted_m6 = weighted_scores.get('6', 0.0)

    # Determine which WEIGHTED score (M2 or M3) contributes
    higher_weighted_score_m2_m3 = max(weighted_m2, weighted_m3)
    # Determine which module ID provided the higher weighted score
    which_module_contributed_m2_m3 = 2 if weighted_m2 >= weighted_m3 else 3

    # Calculate final total score by summing the contributing weighted points
    final_total_score = (
        weighted_m1 +
        higher_weighted_score_m2_m3 +
        weighted_m4 +
        weighted_m5 +
        weighted_m6
    )

    # --- Determine Pflegegrad based on the FINAL score ---
    determined_pflegegrad = 0
    # Use the existing pflegegrad_thresholds dictionary
    sorted_thresholds = sorted(pflegegrad_thresholds.items())
    for grade, (lower_bound, upper_bound) in sorted_thresholds:
        lower = float(lower_bound)
        upper = float(upper_bound) if upper_bound != float('inf') else float('inf')

        # Check if score falls within the range [lower, upper]
        # Use >= lower and < upper for standard ranges, handle PG 5 separately
        if final_total_score >= lower:
            if grade == 5: # PG 5 is 90 and above
                determined_pflegegrad = 5
                break
            elif final_total_score < upper:
                 # Check for PG 0 explicitly (score >= 0 but < 12.5)
                 if grade == 0:
                     pg1_lower_bound = float(pflegegrad_thresholds.get(1, [12.5, 27])[0])
                     if final_total_score < pg1_lower_bound:
                         determined_pflegegrad = 0
                         break
                     else:
                         continue # Score is >= PG1 lower bound, check higher grades
                 else:
                    determined_pflegegrad = grade # Found PG 1-4
                    break
        elif grade == 0 and final_total_score < lower: # Handle scores below 0 just in case
             determined_pflegegrad = 0
             break


    # --- Prepare data for the template ---
    result_data = {
        'answers': session.get('answers', {}),
        'module_scores_raw': module_scores_raw, # Raw scores per module
        'module_scores_weighted': weighted_scores, # Weighted scores per module
        'final_total_score': round(final_total_score, 2), # The final sum
        'pflegegrad': determined_pflegegrad,
        'which_module_contributed_m2_m3': which_module_contributed_m2_m3
    }

    # Clear session answers
    session.pop('answers', None)
    session.modified = True

    # Render the result page
    return render_template('result.html',
                           result=result_data,
                           modules=all_modules,
                           pflegegrad_thresholds=pflegegrad_thresholds,
                           max_score=100.0) # Max score for progress bar remains 100

# ... (generate_pdf route) ...


@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    """
    Generates a PDF document based on the calculation results provided in the request body.
    Expects JSON data containing detailed results, final score, and care grade.
    """
    data = None
    try:
        # Attempt to parse JSON data from the request body.
        # silent=True prevents an immediate exception if parsing fails or content-type is wrong.
        data = request.get_json(silent=True)

        # Check if JSON parsing failed or returned no data
        if data is None:
            # Log the raw request data for debugging if parsing failed
            raw_data = request.data.decode('utf-8', errors='ignore') # Decode safely
            current_app.logger.error(f"Invalid or empty JSON received for PDF. Raw data received: '{raw_data}'")
            # Return a clear error response to the client
            return jsonify({"error": "Invalid or empty JSON data received. Ensure 'Content-Type: application/json' header is set and body is valid JSON."}), 400 # Bad Request

        # Log the successfully parsed data (optional, but helpful for debugging)
        current_app.logger.info(f"Successfully parsed JSON data for PDF generation: {json.dumps(data)}")

        # --- Extract data safely using .get() with defaults ---
        # detailed_results is expected to be a dictionary already parsed by get_json()
        detailed_results = data.get('detailed_results', {})
        final_total_score_str = data.get('final_total_score', '0.0')
        pflegegrad_str = data.get('pflegegrad', '0')

        # --- Validate and Convert Extracted Data ---
        try:
            final_total_score = float(final_total_score_str)
        except (ValueError, TypeError):
            current_app.logger.warning(f"Invalid final_total_score format received: '{final_total_score_str}'. Defaulting to 0.0.")
            final_total_score = 0.0
            # Optionally flash a message, but often API errors are just returned
            # flash("Ungültiger Gesamtpunktwert für PDF erhalten.", "warning")

        try:
            pflegegrad = int(pflegegrad_str)
        except (ValueError, TypeError):
            current_app.logger.warning(f"Invalid pflegegrad format received: '{pflegegrad_str}'. Defaulting to 0.")
            pflegegrad = 0
            # flash("Ungültiger Pflegegrad für PDF erhalten.", "warning")

        # --- Validate detailed_results structure (basic check) ---
        if not isinstance(detailed_results, dict):
             current_app.logger.error(f"Expected 'detailed_results' to be a dictionary, but got type {type(detailed_results)}. Value: {detailed_results}")
             # Use an empty dict as a fallback to prevent further errors
             detailed_results = {}
             flash("Fehler beim Lesen der Detailergebnisse für PDF (ungültiges Format).", "error")


        # --- PDF Generation Logic ---
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12) # Use a font known to support necessary characters if possible, otherwise handle encoding

        # --- Title ---
        pdf.set_font("Arial", 'B', 16)
        # Encode safely for FPDF (latin-1 is common, replace unsupported chars)
        pdf.multi_cell(0, 10, "Pflegegradrechner - Ergebnisbericht".encode('latin-1', 'replace').decode('latin-1'), align='C', ln=1)
        pdf.ln(10)

        # --- Summary ---
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "Zusammenfassung".encode('latin-1', 'replace').decode('latin-1'), ln=1)
        pdf.set_font("Arial", size=12)
        score_text = f"Gesamtpunktzahl (für Pflegegrad): {final_total_score:.2f}"
        pdf.multi_cell(0, 8, score_text.encode('latin-1', 'replace').decode('latin-1')) # Use multi_cell for score too
        pg_text = f"Ermittelter Pflegegrad: {pflegegrad}" if pflegegrad > 0 else "Ermittelter Pflegegrad: Kein Pflegegrad (unter 12.5 Punkte)"
        pdf.multi_cell(0, 8, pg_text.encode('latin-1', 'replace').decode('latin-1')) # Use multi_cell here too
        pdf.ln(5)

        # --- Detailed Results (using data parsed from JSON) ---
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "Detailergebnisse nach Modulen".encode('latin-1', 'replace').decode('latin-1'), ln=1)
        pdf.set_font("Arial", size=10)

        # Access data within the parsed detailed_results dictionary
        module_answers_all = detailed_results.get('answers', {})
        module_scores_raw = detailed_results.get('module_scores_raw', {})
        module_scores_weighted = detailed_results.get('module_scores_weighted', {})
        which_module_contributed = detailed_results.get('which_module_contributed_m2_m3')

        # Log data being used for PDF generation loop
        current_app.logger.info("--- Preparing to loop through modules for PDF ---")
        current_app.logger.info(f"Detailed Results Data Keys: {list(detailed_results.keys())}")
        current_app.logger.info(f"Module Answers Keys: {list(module_answers_all.keys())}")

        # Check if module_answers_all is actually a dictionary before iterating
        if isinstance(module_answers_all, dict):
            # Iterate through modules based on the keys in the answers
            for module_id_str in sorted(module_answers_all.keys(), key=int):
                current_app.logger.info(f"Processing Module ID: {module_id_str} for PDF")

                module_id = int(module_id_str)
                module_info = all_modules.get(module_id)
                module_answers = module_answers_all.get(module_id_str, {}) # Should be a dict

                if not module_info:
                    current_app.logger.warning(f"Module info not found for ID: {module_id_str}, skipping in PDF.")
                    continue

                pdf.set_font("Arial", 'B', 11)
                module_name = module_info.get('name', f'Modul {module_id}')
                pdf.cell(0, 8, f"--- {module_name.encode('latin-1', 'replace').decode('latin-1')} ---", ln=1)
                pdf.set_font("Arial", size=10)

                raw_score = module_scores_raw.get(module_id_str, 0.0)
                weighted_score = module_scores_weighted.get(module_id_str, 0.0)

                pdf.cell(0, 6, f"Rohpunkte: {raw_score:.1f}".encode('latin-1', 'replace').decode('latin-1'), ln=1)
                pdf.cell(0, 6, f"Gewichtete Punkte (aus Tabelle): {weighted_score}".encode('latin-1', 'replace').decode('latin-1'), ln=1)

                # Add M2/M3 contribution note
                if module_id_str == '2' or module_id_str == '3':
                    note_text = ""
                    if which_module_contributed is not None and module_id == which_module_contributed:
                        note_text = "(Dieser Wert zählt für die Gesamtpunktzahl)"
                    else:
                        note_text = "(Nicht für Gesamtpunktzahl berücksichtigt)"

                    if note_text:
                        pdf.set_font("Arial", 'I', 9)
                        pdf.cell(0, 5, note_text.encode('latin-1', 'replace').decode('latin-1'), ln=1)
                        pdf.set_font("Arial", size=10)

                pdf.ln(2)
                pdf.set_font("Arial", 'B', 10)
                pdf.cell(0, 6, "Antworten:".encode('latin-1', 'replace').decode('latin-1'), ln=1)
                pdf.set_font("Arial", size=9)

                # Check if module_answers is a dictionary before iterating
                if isinstance(module_answers, dict) and module_answers:
                    for q_idx_str, answer_data in sorted(module_answers.items(), key=lambda item: int(item[0])):
                        if isinstance(answer_data, dict): # Ensure answer_data is a dict
                            q_text = answer_data.get('question', f'Frage {int(q_idx_str)+1}')
                            a_text = answer_data.get('answer_text', 'N/A')
                            a_score = answer_data.get('score', 'N/A')
                            full_text = f"- {q_text}: {a_text} ({a_score} Rohpunkte)"
                            pdf.multi_cell(0, 5, full_text.encode('latin-1', 'replace').decode('latin-1'))
                        else:
                            # Log unexpected answer_data format
                            current_app.logger.warning(f"Unexpected answer_data format for M{module_id_str} Q{q_idx_str}: {answer_data}")
                            pdf.multi_cell(0, 5, f"- Frage {int(q_idx_str)+1}: Ungültige Antwortdaten".encode('latin-1', 'replace').decode('latin-1'))
                elif not module_answers:
                     pdf.cell(0, 5, "- Keine Antworten für dieses Modul vorhanden.".encode('latin-1', 'replace').decode('latin-1'), ln=1)
                else:
                    # Log unexpected module_answers format
                    current_app.logger.warning(f"Unexpected module_answers format for M{module_id_str}: {module_answers}")
                    pdf.cell(0, 5, "- Ungültige Antwortdaten für dieses Modul.".encode('latin-1', 'replace').decode('latin-1'), ln=1)


                pdf.ln(4)
                current_app.logger.info(f"Finished processing Module ID: {module_id_str} for PDF")
        else:
            # Log if module_answers_all is not a dictionary
            current_app.logger.error(f"Expected 'answers' within detailed_results to be a dictionary, but got {type(module_answers_all)}. Skipping detailed answers in PDF.")
            pdf.set_font("Arial", 'I', 10) # Italic note
            pdf.multi_cell(0, 6, "Fehler: Detaillierte Antworten konnten nicht geladen werden (ungültiges Datenformat).".encode('latin-1', 'replace').decode('latin-1'))


        # --- Output the PDF ---
        pdf_output_bytes = bytes(pdf.output())

        return Response(
            pdf_output_bytes,
            mimetype='application/pdf',
            headers={
                'Content-Disposition': 'attachment;filename=pflegegrad_results.pdf',
                'Content-Type': 'application/pdf' # Content-Type is technically redundant here but doesn't hurt
            }
        )

    except Exception as e:
        # Log the error including traceback
        current_app.logger.error(f"Error generating PDF: {e}", exc_info=True)
        # Flash a user-friendly message (might not be visible if it's an API call)
        flash(f"Ein Fehler ist beim Erstellen des PDFs aufgetreten: {e}", "error")
        # Return a server error response
        return jsonify({"error": f"An internal server error occurred during PDF generation: {e}"}), 500


# ... (rest of app.py, including if __name__ == '__main__':) ...
    

if __name__ == '__main__':
    # Use a more specific host and port if needed, e.g., host='0.0.0.0' for external access
    app.run(debug=True, port=5001) # Changed port to 5001 to avoid potential conflicts