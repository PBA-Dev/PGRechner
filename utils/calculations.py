import logging
from config.pflegegrad_config import SCORE_TO_PFLEGEGRAD, MODULE_WEIGHTS, MODULE_POINT_CAPS

# Configure logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

# --- Constants ---
MODULE_WEIGHTS = { # Defined in pflegegrad_config.py
     1: 0.10,
     2: 0.15, # Combined weight for M2+M3
     3: 0.15, # Combined weight for M2+M3
     4: 0.20,
     5: 0.15, # Placeholder - M5 is handled differently
     6: 0.15,
 }

SCORE_TO_PFLEGEGRAD = {
    90.0: 5,
    70.0: 4,
    47.5: 3,
    27.0: 2,
    12.5: 1
    # Grade 0 is handled if score is below 12.5
}


def map_frequency_to_score(count, unit, question_id):
    """
    Maps frequency count and unit to a score (0, 1, 3, 5) based on NBA rules.
    THIS IS A PLACEHOLDER - NEEDS ACTUAL NBA LOGIC.

    Args:
        count (int): The frequency count (e.g., 0, 1, 2, ...).
        unit (str): The frequency unit (e.g., 'pro Tag', 'pro Woche', 'pro Monat').
        question_id (str): The ID of the question (e.g., '5.1.1'), as rules might differ.

    Returns:
        int: The corresponding score (0, 1, 3, or 5).
    """
    # --- !!! IMPORTANT: Replace this placeholder logic with actual NBA rules !!! ---
    # This example assumes simple thresholds, which is likely incorrect.
    # The real rules depend on the specific question and the exact frequency definitions.

    if count == 0:
        return 0

    # Example placeholder logic (adjust based on actual rules)
    if unit == 'pro Tag':
        if count >= 3: # Example: 3+ times a day = 5 points
            return 5
        elif count >= 1: # Example: 1-2 times a day = 3 points
            return 3
        else: # Should not happen if count > 0, but as fallback
             return 1 # Or 0 depending on rules
    elif unit == 'pro Woche':
        if count >= 5: # Example: 5+ times a week = 5 points? (Check rules)
            return 5
        elif count >= 3: # Example: 3-4 times a week = 3 points?
            return 3
        elif count >= 1: # Example: 1-2 times a week = 1 point?
            return 1
        else:
            return 0
    elif unit == 'pro Monat':
         if count >= 5: # Example: 5+ times a month = 3 points? (Check rules)
             return 3
         elif count >= 1: # Example: 1-4 times a month = 1 point?
             return 1
         else:
             return 0
    else: # Fallback for unknown units or if unit is empty
        # Maybe map based on count alone if unit is missing? Check rules.
        if count >= 5: return 5
        if count >= 3: return 3
        if count >= 1: return 1
        return 0
    # --- End of Placeholder Logic ---


def calculate_module_5_score_official(module_5_answers):
    """
    Calculates the raw score for Module 5 based on the official NBA guidelines.
    Reads the new dictionary format including frequency data.

    Args:
        module_5_answers (dict): Dictionary containing answers for Module 5.
                                 Example: {'5.1.1': None, '5.1.1_freq': {'count': '2', 'unit': 'pro Tag'}, '5.5.1': '1', ...}

    Returns:
        float: The calculated raw score for Module 5.
    """
    total_score = 0.0
    log.debug(f"M5 Calc (Official): Input answers: {module_5_answers}")

    if not isinstance(module_5_answers, dict):
        log.error("M5 Calc Error: Input answers is not a dictionary.")
        return 0.0

    processed_freq_questions = set()

    for key, value in module_5_answers.items():
        # Skip notes and frequency data entries themselves
        if key == 'notes' or key.endswith('_freq'):
            continue

        question_id = key
        score_value = value # Can be score string ("0", "1", etc.) or None

        # Check if it's a standard radio question (score is directly provided)
        if score_value is not None:
            try:
                score = float(score_value)
                total_score += score
                log.debug(f"M5 Calc: Added score {score} for standard question {question_id}")
            except (ValueError, TypeError):
                log.warning(f"M5 Calc: Invalid score value '{score_value}' for question {question_id}. Skipping.")

        # Check if it's a frequency question (score is None, needs calculation)
        elif score_value is None:
            freq_key = f"{question_id}_freq"
            freq_data = module_5_answers.get(freq_key)

            if isinstance(freq_data, dict):
                try:
                    count_str = freq_data.get('count', '0')
                    count = int(count_str) if count_str.isdigit() else 0
                    unit = freq_data.get('unit', '')

                    # Map frequency to score using the (placeholder) function
                    points = map_frequency_to_score(count, unit, question_id)
                    total_score += points
                    processed_freq_questions.add(question_id)
                    log.debug(f"M5 Calc: Added score {points} for frequency question {question_id} (Count: {count}, Unit: '{unit}')")
                except Exception as e:
                    log.error(f"M5 Calc: Error processing frequency data for {question_id}: {e}")
            else:
                log.warning(f"M5 Calc: Missing or invalid frequency data ({freq_key}) for question {question_id} where score was None. Assuming 0 points.")

    # Optional: Add checks for frequency questions that might not have been processed
    # (e.g., if a freq question definition exists but wasn't in module_5_answers)

    log.debug(f"M5 Calc: Final raw score: {total_score}")
    return total_score


def calculate_scores(all_answers):
    """
    Calculates raw scores for each module, applies weights, and determines the total weighted score.
    Reads the new dictionary format from session['module_answers'].

    Args:
        all_answers (dict): The dictionary containing answers for all modules.
                            Example: {'1': {'1.1': '3', 'notes': '...'}, '2': {...}, ...}

    Returns:
        dict: A dictionary containing raw scores, weighted scores, total weighted score,
              and potentially the calculated Pflegegrad. Returns None on critical error.
              Example: {'raw_scores': {1: 10.0, 2: 5.0, ...},
                        'weighted_scores': {1: 1.0, 2: 0.75, ...},
                        'total_weighted_score': 65.5,
                        'pflegegrad': 3}
    """
    if not isinstance(all_answers, dict):
        log.error("Calculate Scores Error: Input 'all_answers' is not a dictionary.")
        return None

    log.debug(f"DEBUG Calc Scores: Input all_answers keys: {list(all_answers.keys())}")

    raw_scores = {}
    weighted_scores = {}
    total_weighted_score = 0.0

    # --- Calculate Raw Scores for Modules 1, 2, 3, 4, 6 ---
    for module_id in [1, 2, 3, 4, 6]:
        module_id_str = str(module_id)
        module_score = 0.0
        module_answers = all_answers.get(module_id_str)

        if isinstance(module_answers, dict):
            for key, value in module_answers.items():
                # Check if key is likely a question ID and value is a score string
                # Simple check: key contains a dot and value is a digit string
                if '.' in key and isinstance(value, str) and value.isdigit():
                    try:
                        score = float(value)
                        module_score += score
                    except ValueError:
                        log.warning(f"Calc M{module_id}: Invalid score value '{value}' for key '{key}'. Skipping.")
                # Add more robust key checking if needed (e.g., using regex or checking against module definition)

            # Apply point caps if defined
            cap = MODULE_POINT_CAPS.get(module_id)
            if cap is not None and module_score > cap:
                log.debug(f"Calc M{module_id}: Applying point cap. Score {module_score} capped to {cap}")
                module_score = cap

            raw_scores[module_id] = round(module_score, 2)
            log.debug(f"DEBUG Calc Scores: Module {module_id} Raw Score: {raw_scores[module_id]:.2f}")

        else:
            log.warning(f"Calculate Scores Warning: No valid answer dictionary found for Module {module_id}. Setting raw score to 0.")
            raw_scores[module_id] = 0.0


    # --- Calculate Raw Score for Module 5 ---
    module_5_answers = all_answers.get('5')
    if isinstance(module_5_answers, dict):
        raw_scores[5] = round(calculate_module_5_score_official(module_5_answers), 2)
        # Apply point cap for M5 if defined
        cap = MODULE_POINT_CAPS.get(5)
        if cap is not None and raw_scores[5] > cap:
             log.debug(f"Calc M5: Applying point cap. Score {raw_scores[5]} capped to {cap}")
             raw_scores[5] = cap
        log.debug(f"DEBUG Calc Scores: Module 5 Raw Score: {raw_scores[5]:.2f}")
    else:
        log.warning("Calculate Scores Warning: No valid answer dictionary found for Module 5. Setting raw score to 0.")
        raw_scores[5] = 0.0


    # --- Combine Scores for M2 and M3 before weighting ---
    # According to NBA, M2 and M3 are combined, and the higher score determines the points for this combined area.
    score_m2 = raw_scores.get(2, 0.0)
    score_m3 = raw_scores.get(3, 0.0)
    combined_m2_m3_score = max(score_m2, score_m3)
    log.debug(f"DEBUG Calc Scores: Combined M2/M3 score (using max): {combined_m2_m3_score:.2f} (M2: {score_m2}, M3: {score_m3})")

    # --- Calculate Weighted Scores ---
    try:
        # Module 1
        weighted_scores[1] = raw_scores.get(1, 0.0) * MODULE_WEIGHTS[1]
        total_weighted_score += weighted_scores[1]

        # Combined Module 2/3
        # Use the weight defined for M2 (or M3, should be the same)
        weighted_scores[23] = combined_m2_m3_score * MODULE_WEIGHTS[2] # Using M2's weight for the combined score
        total_weighted_score += weighted_scores[23]

        # Module 4
        weighted_scores[4] = raw_scores.get(4, 0.0) * MODULE_WEIGHTS[4]
        total_weighted_score += weighted_scores[4]

        # Module 5 - Handled differently, often involves selecting highest score from M5 or M1/M4 etc.
        # Placeholder: Simple weighting (adjust based on actual NBA rules for incorporating M5)
        # The official calculation might involve comparing M5 score with others.
        # For now, just apply its weight directly for demonstration.
        weighted_scores[5] = raw_scores.get(5, 0.0) * MODULE_WEIGHTS[5]
        total_weighted_score += weighted_scores[5] # Adjust this based on rules!

        # Module 6
        weighted_scores[6] = raw_scores.get(6, 0.0) * MODULE_WEIGHTS[6]
        total_weighted_score += weighted_scores[6]

    except KeyError as e:
        log.error(f"Calculate Scores Error: Missing weight in MODULE_WEIGHTS for key {e}.")
        return None
    except Exception as e:
        log.error(f"Calculate Scores Error during weighting: {e}")
        return None


    # --- Final Results ---
    final_total_score = round(total_weighted_score, 2)
    log.debug(f"DEBUG Calc Scores: Final Total Weighted Score: {final_total_score:.2f}")

    # Determine Pflegegrad
    pflegegrad = determine_pflegegrad(final_total_score)
    log.debug(f"DEBUG Calc Scores: Determined Pflegegrad: {pflegegrad}")

    results = {
        'raw_scores': raw_scores,
        'weighted_scores': weighted_scores, # Contains combined M2/M3 score under key 23
        'total_weighted_score': final_total_score,
        'pflegegrad': pflegegrad,
        'combined_m2_m3_raw': combined_m2_m3_score # Add combined raw score for display if needed
    }
    return results


def determine_pflegegrad(total_weighted_score):
    """Determines the Pflegegrad based on the total weighted score."""
    log.debug(f"DEBUG Determine PG: Input score: {total_weighted_score}")
    if not SCORE_TO_PFLEGEGRAD:
        log.error("SCORE_TO_PFLEGEGRAD not loaded or empty. Cannot determine Pflegegrad.")
        return 0 # Default to 0 if config is missing

    # Iterate through thresholds (keys of the dict) sorted descending
    # The keys are the *minimum* score required for that grade
    for score_threshold, pg in sorted(SCORE_TO_PFLEGEGRAD.items(), reverse=True):
        # !!! REMOVE the old unpacking line like: min_score, max_score = score_threshold !!!

        # Correct comparison: Check if the score meets or exceeds the threshold
        if total_weighted_score >= score_threshold:
            log.info(f"DEBUG Determine PG: Score {total_weighted_score} >= threshold {score_threshold} -> PG {pg}")
            return pg # Return the corresponding Pflegegrad

    # If the score is below the lowest threshold (e.g., 12.5)
    log.info(f"DEBUG Determine PG: Score {total_weighted_score} is below lowest threshold -> PG 0")
    return 0 # Default to Pflegegrad 0

def get_total_weighted_score(results):
    """
    Safely retrieves the total weighted score from the results dictionary.
    """
    if isinstance(results, dict):
        return results.get('total_weighted_score', 0.0)
    return 0.0

# Example usage (for testing purposes)
if __name__ == '__main__':
    # Example test data mimicking session structure
    test_answers = {
        '1': {'1.1': '3', '1.2': '1', '1.3': '0', '1.4': '1', '1.5': '3', '1.6': '0', '1.7': '1', '1.8': '1', '1.9': '0', '1.10': '1', 'notes': 'M1 notes'},
        '2': {'2.1': '1', '2.2': '3', '2.3': '0', 'notes': 'M2 notes'},
        '3': {'3.1': '5', '3.2': '3', '3.3': '1', '3.4': '0', '3.5': '1', '3.6': '0', '3.7': '1', '3.8': '0', '3.9': '1', '3.10': '0', '3.11': '1', '3.12': '0', '3.13': '1', 'notes': 'M3 notes'},
        '4': {'4.1': '1', '4.2': '1', '4.3': '3', '4.4': '0', '4.5': '1', '4.6': '0', '4.7': '1', '4.8': '3', '4.9': '0', '4.10': '1', '4.11': '0', '4.12': '1', '4.13': '0', '4.14': '1', '4.15': '0', '4.16': '1', 'notes': 'M4 notes'},
        '5': {'5.1.1': None, '5.1.1_freq': {'count': '2', 'unit': 'pro Tag'}, '5.1.2': None, '5.1.2_freq': {'count': '5', 'unit': 'pro Woche'}, '5.1.3': None, '5.1.3_freq': {'count': '1', 'unit': 'pro Monat'}, '5.1.4': None, '5.1.4_freq': {'count': '0', 'unit': 'pro Tag'}, '5.5.1': '1', 'notes': 'M5 notes'}, # Example M5
        '6': {'6.1': '1', '6.2': '0', '6.3': '1', '6.4': '0', '6.5': '1', '6.6': '0', '6.7': '1', '6.8': '0', 'notes': 'M6 notes'}
    }

    # --- !!! IMPORTANT: Define MODULE_POINT_CAPS if needed for testing !!! ---
    MODULE_POINT_CAPS = {
    1: 10,  # Example cap for Module 1
    2: 15,  # Example cap for Module 2
    3: 15,  # Example cap for Module 3
    4: 40,  # Example cap for Module 4
    5: 20,  # Example cap for Module 5
    6: 15   # !!! ADD THIS LINE (adjust value if needed) !!!
}

    calculation_results = calculate_scores(test_answers)

    if calculation_results:
        print("\n--- Calculation Results ---")
        print(f"Raw Scores: {calculation_results.get('raw_scores')}")
        print(f"Weighted Scores: {calculation_results.get('weighted_scores')}")
        print(f"Total Weighted Score: {calculation_results.get('total_weighted_score')}")
        print(f"Determined Pflegegrad: {calculation_results.get('pflegegrad')}")
        print(f"Combined M2/M3 Raw Score: {calculation_results.get('combined_m2_m3_raw')}")
    else:
        print("\nCalculation failed.")