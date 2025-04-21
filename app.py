import os
import json
import logging
import math # Needed for ceiling if using strict < comparison
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

# Corrected mapping tables based on NBA-Punkts.rtf
# Note: M2 and M3 are handled separately in the calculate function
weighted_score_mapping_tables = {
    # Module 1: Mobilität (10%)
    1: [(0, 0.0), (2, 2.5), (4, 5.0), (6, 7.5), (10, 10.0)],
    # Module 4: Selbstversorgung (40%)
    4: [(0, 0.0), (3, 10.0), (8, 20.0), (19, 30.0), (37, 40.0)],
    # Module 5: Umgang mit krankheits-/therapiebedingten Anforderungen (20%)
    # Note: The RTF document seems to have slightly different ranges than the original doc.
    # Using RTF ranges: 0=0, 1=5, 2-3=10, 4-5=15, 6-15=20
    5: [(0, 0.0), (1, 5.0), (2, 10.0), (4, 15.0), (6, 20.0)],
    # Module 6: Gestaltung des Alltagslebens und sozialer Kontakte (15%)
    6: [(0, 0.0), (1, 3.75), (4, 7.5), (7, 11.25), (12, 15.0)]
}

# Special mapping table for the combined Modules 2 & 3 score (15%)
# Input is the MAX(raw_score_m2, raw_score_m3)
weighted_score_mapping_m2_m3 = [
    (0, 0.0), (2, 3.75), (6, 7.5), (11, 11.25), (17, 15.0)
]

def map_raw_to_weighted_score(mapping_table, raw_score):
    """Maps raw score to weighted score using a specific mapping table."""
    weighted_score = 0.0
    try:
        # Ensure raw_score is a number, default to 0 if not
        raw_score = float(raw_score)
    except (ValueError, TypeError):
         # Log this potential issue
         current_app.logger.warning(f"Invalid raw_score type for weighted score mapping: {raw_score}")
         raw_score = 0.0

    # Iterate through the table (sorted by raw score threshold)
    for table_raw, table_weighted in mapping_table:
        if raw_score >= table_raw:
            weighted_score = table_weighted
        else:
            # Since the table is sorted, we can stop early
            break
    return float(weighted_score)

def calculate_frequency_score(count, unit):
    """Calculates a raw score based on frequency of need."""
    try:
        count = int(count)
        if count < 0: count = 0
    except (ValueError, TypeError):
        count = 0

    if count == 0: return 0

    unit = str(unit).lower()
    if 'tag' in unit or 'day' in unit: return 3
    elif 'woche' in unit or 'week' in unit: return 2
    elif 'monat' in unit or 'month' in unit: return 1
    else: return 0

# --- Helper Function for Module 5 ---
# --- UPDATED Helper Function for Module 5 ---
def calculate_module5_raw_score(module5_answers):
    """Calculates the raw score for Module 5 based on detailed rules, using keys from module5.py."""
    print(f"DEBUG: calculate_module5_raw_score received: {module5_answers}") # Keep for debugging

    # Helper to safely get count and unit using the correct keys
    def get_freq_data(answers, key):
        data = answers.get(key, {}) # Use the key directly (e.g., '5.1.1')
        count = 0
        try:
            # Expecting 'count' and 'unit' keys from module_page_submit
            count = float(data.get('count', 0))
        except (ValueError, TypeError):
            count = 0
        unit = data.get('unit', '').lower().replace('pro ', '') # Get unit, ensure lowercase, remove "pro "
        return count, unit

    # --- Part 1: Items 5.1.1 - 5.1.7 (Medikation to Hilfsmittel) ---
    daily_sum_p1 = 0.0
    weekly_sum_p1 = 0.0
    monthly_sum_p1 = 0.0
    # *** USE CORRECT KEYS FROM module5.py ***
    part1_keys = [f'5.1.{i}' for i in range(1, 8)] # Keys 5.1.1 to 5.1.7

    for key in part1_keys:
        count, unit = get_freq_data(module5_answers, key)
        if unit == 'tag':
            daily_sum_p1 += count
        elif unit == 'woche':
            weekly_sum_p1 += count
        elif unit == 'monat':
            monthly_sum_p1 += count

    avg_per_day_p1 = round(daily_sum_p1 + (weekly_sum_p1 / 7.0) + (monthly_sum_p1 / 30.0), 4)

    points_part1 = 0
    if avg_per_day_p1 >= 1 and avg_per_day_p1 <= 3:
        points_part1 = 1
    elif avg_per_day_p1 > 3 and avg_per_day_p1 <= 8:
        points_part1 = 2
    elif avg_per_day_p1 > 8:
        points_part1 = 3
    print(f"DEBUG M5 Part 1: avg={avg_per_day_p1}, points={points_part1}") # Keep for debugging

    # --- Part 2: Items 5.2.1 - 5.2.4 (Verband to Therapiemaßnahmen) ---
    daily_sum_p2 = 0.0
    weekly_sum_p2 = 0.0
    monthly_sum_p2 = 0.0
    # *** USE CORRECT KEYS FROM module5.py ***
    part2_keys = [f'5.2.{i}' for i in range(1, 5)] # Keys 5.2.1 to 5.2.4

    for key in part2_keys:
        count, unit = get_freq_data(module5_answers, key)
        if unit == 'tag':
            daily_sum_p2 += count
        elif unit == 'woche':
            weekly_sum_p2 += count
        elif unit == 'monat':
            monthly_sum_p2 += count

    avg_per_day_p2 = round(daily_sum_p2 + (weekly_sum_p2 / 7.0) + (monthly_sum_p2 / 30.0), 4)

    points_part2 = 0
    if avg_per_day_p2 >= (1.0/7.0) and avg_per_day_p2 < 1.0:
        points_part2 = 1
    elif avg_per_day_p2 >= 1.0 and avg_per_day_p2 < 3.0:
        points_part2 = 2
    elif avg_per_day_p2 >= 3.0:
        points_part2 = 3
    print(f"DEBUG M5 Part 2: avg={avg_per_day_p2}, points={points_part2}") # Keep for debugging


    # --- Part 3: Items 5.3.1 (Intensiv), 5.4.1-5.4.3 (Besuche) ---
    # Mapping document logic to module5.py keys:
    # Doc 4.5.12 (Intensive) -> module5.py '5.3.1'
    # Doc 4.5.15 (Extended Visits) -> module5.py '5.4.3'
    # Doc 4.5.13 (Regular Visits) -> module5.py '5.4.1'
    # Doc 4.5.14 (Other Visits <=3h) -> module5.py '5.4.2'
    # Doc 4.5.K (Early Support) -> Not present in module5.py, ignore for now.
    intermediate_sum_part3 = 0.0

    # Item 5.3.1 (Intensive)
    count, unit = get_freq_data(module5_answers, '5.3.1')
    if unit == 'tag': intermediate_sum_part3 += 60.0
    elif unit == 'woche': intermediate_sum_part3 += count * 8.6
    elif unit == 'monat': intermediate_sum_part3 += count * 2.0

    # Item 5.4.3 (Extended Visits >3h)
    count, unit = get_freq_data(module5_answers, '5.4.3')
    if unit == 'woche': intermediate_sum_part3 += count * 8.6
    elif unit == 'monat': intermediate_sum_part3 += count * 2.0

    # Items 5.4.1 (Arzt) and 5.4.2 (Other <=3h)
    for key in ['5.4.1', '5.4.2']:
         count, unit = get_freq_data(module5_answers, key)
         if unit == 'woche': intermediate_sum_part3 += count * 4.3
         elif unit == 'monat': intermediate_sum_part3 += count * 1.0

    intermediate_sum_part3 = round(intermediate_sum_part3, 4)

    points_part3 = 0
    if intermediate_sum_part3 >= 4.3 and intermediate_sum_part3 < 60.0:
         points_part3 = 1
    elif intermediate_sum_part3 >= 60.0:
         points_part3 = 6
    print(f"DEBUG M5 Part 3: sum={intermediate_sum_part3}, points={points_part3}") # Keep for debugging

    # --- Part 4: Item 5.5.1 (Diät) ---
    # *** USE CORRECT KEY FROM module5.py ***
    answer_data_p4 = module5_answers.get('5.5.1', {})
    points_part4 = 0
    try:
        # Get score directly as saved by module_page_submit
        points_part4 = int(answer_data_p4.get('score', 0))
        if points_part4 not in [0, 1, 2, 3]: points_part4 = 0
    except (ValueError, TypeError):
        points_part4 = 0
    print(f"DEBUG M5 Part 4: points={points_part4}") # Keep for debugging

    # --- Final Raw Score ---
    raw_score_m5 = points_part1 + points_part2 + points_part3 + points_part4
    print(f"DEBUG M5 Final Raw: {raw_score_m5}") # Keep for debugging

    return raw_score_m5
# ... (rest of app setup) ...

# ... (other imports) ...

# --- Routes ---

@app.route('/')
def intro():
    """Displays the introduction page."""
    # Clear any previous session data at the start
    session.pop('answers', None)
    session.pop('results', None)
    return render_template('intro.html')


# --- Add Helper Function for Module 5 Frequency Scoring ---
def calculate_frequency_score(count, unit):
    """
    Calculates a raw score based on frequency of need.
    Adjust this logic based on official NBA guidelines if needed.
    """
    try:
        # Ensure count is a non-negative integer
        count = int(count)
        if count < 0:
            count = 0
    except (ValueError, TypeError):
        count = 0 # Treat invalid input as 0

    if count == 0:
        return 0 # No need or self-sufficient

    # Determine score based on unit (assuming count > 0)
    unit = str(unit).lower() # Normalize unit
    if 'tag' in unit or 'day' in unit:
        return 3 # Daily need
    elif 'woche' in unit or 'week' in unit:
        return 2 # Weekly need
    elif 'monat' in unit or 'month' in unit:
        return 1 # Monthly need
    else:
        return 0 # Unknown unit or frequency not applicable

# --- Update module_page_submit function ---
# --- Route for DISPLAYING module page (GET requests) ---
@app.route('/module/<int:module_id>', methods=['GET'], endpoint='module_page') # Explicit endpoint name
def module_page(module_id):
    if module_id not in all_modules or module_id < 1 or module_id > TOTAL_MODULES:
        flash("Ungültiges Modul angefordert.", "error")
        # Redirect to intro or the first module if session exists
        if 'module_answers' in session and session['module_answers']:
             first_answered = min(int(k) for k in session['module_answers'].keys() if k.isdigit())
             return redirect(url_for('module_page', module_id=first_answered))
        return redirect(url_for('intro'))

    module_data = all_modules[module_id]
    module_id_str = str(module_id)

    # Get current answers for this module to pre-fill form
    current_answers = session.get('module_answers', {}).get(module_id_str, {})

    # --- Calculate Estimated Score for Progress Bar ---
# --- Calculate Estimated Score for Progress Bar ---
    current_estimated_score = 0.0
    temp_module_scores_raw = {}      # Store raw scores per module
    temp_module_scores_weighted = {} # Store weighted scores (for M1, M4, M5, M6 directly)

    # Recalculate based on all answered modules in the session
    all_session_answers = session.get('module_answers', {})
    for mid_str, answers in all_session_answers.items():
        try:
            mid = int(mid_str)
            if mid not in all_modules: continue # Skip if module ID isn't valid
        except ValueError:
            continue # Skip if module ID isn't an integer

        # 1. Calculate Raw Score for the current module
        raw_score = 0.0
        for q_key, answer_data in answers.items():
            # Ensure answer_data is a dict and has a 'score' key
            if isinstance(answer_data, dict) and 'score' in answer_data:
                try:
                    raw_score += float(answer_data.get('score', 0))
                except (ValueError, TypeError):
                    pass # Ignore if score is not a number

        temp_module_scores_raw[mid_str] = raw_score # Store the calculated raw score

        # 2. Determine Correct Mapping Table and Calculate Weighted Score (for display/temp storage)
        mapping_table_to_use = None
        weighted_score = 0.0

        # --- MODIFICATION START ---
        if mid in weighted_score_mapping_tables: # Handles M1, M4, M5, M6
            mapping_table_to_use = weighted_score_mapping_tables[mid]

            # *** IMPORTANT: Cap Module 5 raw score BEFORE mapping ***
            if mid == 5:
                raw_score_for_mapping = min(raw_score, 15) # Use capped score for M5 mapping
            else:
                raw_score_for_mapping = raw_score

            if mapping_table_to_use:
                weighted_score = map_raw_to_weighted_score(mapping_table_to_use, raw_score_for_mapping)

        elif mid == 2 or mid == 3:
            # For M2/M3, we store the raw score. The weighted score is calculated
            # *after* the loop using the max raw score and the combined table.
            # We can store 0 temporarily in the weighted dict for these.
            weighted_score = 0.0 # Placeholder - will be calculated correctly below

        else:
            # Should not happen for modules 1-6, but good practice
            weighted_score = 0.0

        temp_module_scores_weighted[mid_str] = weighted_score # Store the calculated weighted score (or placeholder for M2/M3)
        # --- MODIFICATION END ---


    # --- Corrected Estimated Total Calculation (After the loop) ---
    # Get weighted scores for modules calculated directly
    m1_s = temp_module_scores_weighted.get('1', 0.0)
    m4_s = temp_module_scores_weighted.get('4', 0.0)
    m5_s = temp_module_scores_weighted.get('5', 0.0) # This used the capped raw score
    m6_s = temp_module_scores_weighted.get('6', 0.0)

    # Calculate combined M2/M3 score correctly
    raw_m2 = temp_module_scores_raw.get('2', 0.0)
    raw_m3 = temp_module_scores_raw.get('3', 0.0)
    max_raw_m2_m3 = max(raw_m2, raw_m3)

    # Use the correct combined mapping table and the MAX raw score
    m2_m3_s = map_raw_to_weighted_score(weighted_score_mapping_m2_m3, max_raw_m2_m3)

    # Determine which module contributed more to the MAX raw score (for info/display if needed)
    temp_which_module_contributed_m2_m3 = None
    if raw_m2 > raw_m3:
        temp_which_module_contributed_m2_m3 = 2
    elif raw_m3 > raw_m2:
        temp_which_module_contributed_m2_m3 = 3
    elif raw_m2 > 0: # If they are equal and non-zero
        temp_which_module_contributed_m2_m3 = '2 & 3' # Or just 2 or 3

    # Sum the final weighted scores
    current_estimated_score = m1_s + m2_m3_s + m4_s + m5_s + m6_s
    # --- End Corrected Estimated Score Calculation ---

    # Define max_score for the progress bar (adjust if needed)
    max_score = 100

    return render_template(
        'module_page.html',
        module=module_data,
        module_id=module_id,
        TOTAL_MODULES=TOTAL_MODULES, # Pass TOTAL_MODULES
        current_answers=current_answers, # Pass current answers for pre-filling
        # Pass data needed for progress bar
        current_estimated_score=current_estimated_score,
        max_score=max_score,
        pflegegrad_thresholds=pflegegrad_thresholds,
        all_modules=all_modules # Pass all_modules if needed by template logic
    )


# --- Route for HANDLING module submission (POST requests) ---
@app.route('/module/<int:module_id>/submit', methods=['POST'])
def module_page_submit(module_id):
    module_id_str = str(module_id)
    if module_id not in all_modules:
        flash("Ungültiges Modul.", "error")
        return redirect(url_for('intro'))

    module_data = all_modules[module_id]
    current_answers = {} # *** Use a temporary dictionary ***

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

                elif question.get('type') == 'standard':
                    answer_key = f'answer_{module_id_str}_{question_key}'
                    selected_option_index_str = request.form.get(answer_key)

                    if selected_option_index_str is not None:
                        try:
                            selected_option_index = int(selected_option_index_str)
                            options = question.get('options', [])
                            if 0 <= selected_option_index < len(options):
                                selected_option = options[selected_option_index]
                                current_answers[question_key] = {
                                    'option_index': selected_option_index,
                                    'text': selected_option.get('text', ''),
                                    'score': selected_option.get('score', 0)
                                }
                        except ValueError:
                            pass
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
    if next_module_id > TOTAL_MODULES:
        return redirect(url_for('calculate'))
    else:
        # Redirect to the GET endpoint for the next module
        return redirect(url_for('module_page', module_id=next_module_id))

# --- Update calculate function ---
@app.route('/calculate')
def calculate():
    if 'module_answers' not in session or not session['module_answers']:
        flash("Bitte füllen Sie zuerst die Module aus.", "warning")
        return redirect(url_for('intro'))

    all_answers = session.get('module_answers', {})
    module_scores_raw = {} # To store raw scores for ALL modules
    all_detailed_answers = {} # To store text and score for results page/PDF

    # --- Calculate Raw Scores (M1-4, M6) and Collect Detailed Answers ---
    # This loop handles the standard summation for modules other than 5
    for module_id_str, answers in all_answers.items():
        try:
            module_id = int(module_id_str)
            if module_id not in all_modules: continue
            if module_id == 5: continue # Skip Module 5 raw score calculation here
        except ValueError:
            continue

        module_data = all_modules[module_id]
        current_module_raw_score = 0.0
        current_detailed_answers = {}

        # Iterate through stored answers, excluding notes/visited
        for q_key, answer_data in answers.items():
            if q_key not in ['notes', 'visited'] and isinstance(answer_data, dict):
                try:
                    # Standard summation for M1, M2, M3, M4, M6
                    current_module_raw_score += float(answer_data.get('score', 0))
                except (ValueError, TypeError):
                    pass # Ignore non-numeric scores
                # Store details for display
                current_detailed_answers[q_key] = answer_data

        # Store raw score for M1, M2, M3, M4, M6
        module_scores_raw[module_id_str] = current_module_raw_score
        all_detailed_answers[module_id_str] = current_detailed_answers # Store details

    # --- Calculate Module 5 Raw Score using the specific helper function ---
    m5_answers = all_answers.get('5', {}) # Get M5 specific answers from session
    # Ensure detailed answers for M5 are also collected if not done above
    if '5' not in all_detailed_answers and '5' in all_answers:
         all_detailed_answers['5'] = {
             k: v for k, v in all_answers['5'].items() if k not in ['notes', 'visited']
         }
    # Calculate the specific M5 raw score
    raw_score_m5 = calculate_module5_raw_score(m5_answers)
    module_scores_raw['5'] = raw_score_m5 # Add M5 raw score to the dictionary

    # --- Map Raw Scores to Weighted Scores ---
    module_scores_weighted = {} # Initialize dictionary for weighted scores

    # Loop through ALL calculated RAW scores (M1-6)
    for module_id_str, raw_score in module_scores_raw.items():
        try:
            module_id = int(module_id_str)
        except ValueError:
            module_scores_weighted[module_id_str] = 0.0
            continue

        weighted_score = 0.0 # Default weighted score

        if module_id in [1, 4, 6]: # Modules 1, 4, 6 (Use standard mapping)
            if module_id in weighted_score_mapping_tables:
                mapping_table_to_use = weighted_score_mapping_tables[module_id]
                # Use the standard mapping function
                weighted_score = map_raw_to_weighted_score(mapping_table_to_use, raw_score)

        elif module_id == 5: # Module 5 (Use NEW direct mapping based on calculated raw_score_m5)
            # Apply the specific M5 final mapping from the text
            # Note: 'raw_score' here IS the correctly calculated raw_score_m5
            if raw_score == 1:
                weighted_score = 5.0
            elif 2 <= raw_score <= 3:
                weighted_score = 10.0
            elif 4 <= raw_score <= 5:
                weighted_score = 15.0
            elif 6 <= raw_score <= 15: # Max raw seems to be 15
                weighted_score = 20.0
            # else: weighted_score remains 0.0 for raw_score == 0

        elif module_id in [2, 3]: # Modules 2 and 3 (placeholder)
            weighted_score = 0.0 # Actual combined score calculated after loop

        else: # Unexpected module ID
            weighted_score = 0.0

        # Store the calculated weighted score (or placeholder for M2/M3)
        module_scores_weighted[module_id_str] = weighted_score

    # --- Calculate Final Total Score ---
    # 1. Calculate combined M2/M3 weighted score
    raw_m2 = module_scores_raw.get('2', 0.0)
    raw_m3 = module_scores_raw.get('3', 0.0)
    max_raw_m2_m3 = max(raw_m2, raw_m3)
    # Use the M2/M3 combined mapping table and the standard mapping function
    weighted_m2_m3 = map_raw_to_weighted_score(weighted_score_mapping_m2_m3, max_raw_m2_m3)

    # 2. Determine which raw score contributed to M2/M3 max (for info)
    which_module_contributed_m2_m3 = None
    if raw_m2 > raw_m3:
        which_module_contributed_m2_m3 = 2
    elif raw_m3 > raw_m2:
        which_module_contributed_m2_m3 = 3
    elif raw_m2 > 0: # Equal and non-zero
        which_module_contributed_m2_m3 = '2 & 3' # Or just 2 or 3

    # 3. Sum final scores
    final_total_score = (
        module_scores_weighted.get('1', 0.0) +
        weighted_m2_m3 +  # Use the correctly calculated combined score
        module_scores_weighted.get('4', 0.0) +
        module_scores_weighted.get('5', 0.0) + # Uses the NEW correctly calculated M5 weighted score
        module_scores_weighted.get('6', 0.0)
    )
    # --- End Final Score Calculation ---

    # --- Determine Pflegegrad ---
    pflegegrad = 0
    # Ensure thresholds are sorted correctly if not already guaranteed
    sorted_thresholds = sorted(pflegegrad_thresholds.items(), key=lambda item: item[1]['min_points'])
    for grad, threshold in sorted_thresholds:
        # Use round() for comparison to avoid floating point issues, or use a small epsilon
        if round(final_total_score, 2) >= threshold['min_points']:
            pflegegrad = grad
        else:
            # Since sorted, we can stop once a threshold is not met
            break # Exit loop early

    # --- Aggregate Notes ---
    aggregated_notes = {
        mid: data.get('notes', '')
        for mid, data in all_answers.items()
        if data.get('notes')
    }

    # --- Get Benefits Data ---
    from datetime import date
    today = date.today()
    # Determine period based on date - adjust cutoff as needed
    current_period_key = "period_2" if today >= date(today.year, 7, 1) else "period_1"
    # Fallback if period key doesn't exist for some reason
    benefits_for_pg = pflegegrad_benefits.get(pflegegrad, {})
    benefits = benefits_for_pg.get(current_period_key)
    if not benefits: # If current period missing, try the other one
        fallback_period = "period_1" if current_period_key == "period_2" else "period_2"
        benefits = benefits_for_pg.get(fallback_period, {})

    # --- Prepare results for template ---
    results = {
        'final_total_score': round(final_total_score, 2),
        'pflegegrad': pflegegrad,
        'module_scores_raw': module_scores_raw, # Contains CORRECT M5 raw score now
        'module_scores_weighted': module_scores_weighted, # Contains CORRECT M5 weighted score now & 0.0 for M2/M3
        'weighted_m2_m3': round(weighted_m2_m3, 2), # Pass the combined M2/M3 score explicitly
        'which_module_contributed_m2_m3': which_module_contributed_m2_m3,
        'answers': all_detailed_answers, # Pass detailed answers for display/PDF
        'notes': aggregated_notes,       # Pass aggregated notes
        'benefits': benefits             # Pass benefits data
    }

    session['results'] = results # Keep storing in session if needed elsewhere

    # Pass necessary variables to the template
    return render_template(
        'result.html',
        results=results,
        all_modules=all_modules, # Pass module definitions if needed by template
        pflegegrad_thresholds=pflegegrad_thresholds # Pass thresholds if needed by template
        # Add TOTAL_MODULES=TOTAL_MODULES if needed
    )
# Ensure pflegegrad_thresholds is defined or imported correctly before this route
# pflegegrad_thresholds = { ... }

pflegegrad_thresholds = {
    1: {'min_points': 12.5, 'max_points': 26.9},
    2: {'min_points': 27, 'max_points': 47.4},
    3: {'min_points': 47.5, 'max_points': 69.9},
    4: {'min_points': 70, 'max_points': 89.9},
    5: {'min_points': 90, 'max_points': 100}
}
# ... (generate_pdf route) ...


# d:\Users\SSH\OneDrive\1_-_SunState_Health,_LLC\.-Optimum_Pflege\ProgFold\PGRechner\PGRechner\app.py
# ... (imports and other code remain the same) ...

# --- PDF Generation Route ---
# d:\Users\SSH\OneDrive\1_-_SunState_Health,_LLC\.-Optimum_Pflege\ProgFold\PGRechner\PGRechner\app.py

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

        module_answers_all = detailed_results.get('answers', {})
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