# utils/calculations.py
import math

# --- Weighted Score Mapping Tables ---
# Ensure these tables match the official NBA guidelines exactly.
# The Module 5 table here might differ from standard NBA (check source).
weighted_score_mapping_tables = {
    # ... other modules ...
    '1': [
        (0, 0),          # 0 bis 1 Punkte -> 0
        (2, 2.5),        # 2 bis 3 Punkte -> 2.5
        (4, 5.0),        # 4 bis 5 Punkte -> 5.0
        (6, 7.5),        # 6 bis 9 Punkte -> 7.5
        (10, 10.0)       # 10 bis 15 Punkte -> 10.0
    ],
    
    '2': [
        (0, 0),          # 0 bis 1 Punkte -> 0 gewichtet
        (2, 3.75),       # 2 bis 5 Punkte -> 3.75 gewichtet
        # Add other steps if needed from full BRi, up to:
        (17, 15),         # 17 bis 33 Punkte -> 15 gewichtet (Max)
        # Note: The provided text snippet might be incomplete for mid-ranges.
        # We are using the key thresholds given. Add intermediate steps if known.
        # For now, any score >= 17 gets 15. Scores between 5 and 17 need clarification
        # from the full document if precise intermediate steps are required,
        # otherwise map_raw_to_weighted_score will use the last valid step (3.75).
        # Let's assume for now:
        (6, 7.5),        # Placeholder - Adjust if official table differs
        (10, 11.25),     # Placeholder - Adjust if official table differs
    ],
    # --- UPDATE THIS ENTRY FOR MODULE 3 ---
    '3': [
        (0, 0),          # keine Punkte -> 0 gewichtet
        (1, 3.75),       # 1 bis 2 Punkte -> 3.75 gewichtet
        (3, 7.5),        # 3 bis 4 Punkte -> 7.5 gewichtet
        (5, 11.25),      # 5 bis 6 Punkte -> 11.25 gewichtet
        (7, 15)          # 7 bis 65 Punkte -> 15 gewichtet (Max)
    ],
    # --- END UPDATE FOR MODULE 3 ---
    '4': [
        (0, 0),          # 0 bis 2 Punkte -> 0
        (3, 10),         # 3 bis 7 Punkte -> 10
        (8, 20),         # 8 bis 18 Punkte -> 20
        # --- PLACEHOLDERS - REPLACE IF YOU HAVE THE FULL TABLE ---
        (19, 30),        # Assuming 19-36 -> 30 (Example placeholder)
        # --- END PLACEHOLDERS ---
        (37, 40)         # 37 bis 54 Punkte -> 40
    ],
    # --- UPDATE THIS ENTRY FOR MODULE 5 ---
    '5': [
        (0, 0),
        (1, 5),          # 1 Punkt -> 5 gewichtet
        (2, 10),         # 2 bis 3 Punkte -> 10 gewichtet
        (4, 15),         # 4 bis 5 Punkte -> 15 gewichtet
        (6, 20)          # 6 bis 15 Punkte -> 20 gewichtet
    ],
    # --- END UPDATE FOR MODULE 5 ---
    # --- UPDATE THIS ENTRY FOR MODULE 6 ---
    '6': [
        (0, 0),          # keine Punkte -> 0
        (1, 3.75),       # 1 bis 3 Punkte -> 3.75
        (4, 7.5),        # 4 bis 6 Punkte -> 7.5
        (7, 11.25),      # 7 bis 11 Punkte -> 11.25
        (12, 15)         # 12 bis 18 Punkte -> 15
    ],
    # --- END UPDATE FOR MODULE 6 ---
    # ... potentially other modules if you have them ...
}

# --- Helper Functions ---

def map_score_to_points(score, ranges):
    """Helper function to map a score to points based on ranges (used internally in M5)."""
    # Ensure score is treated as a number for comparison
    try:
        numeric_score = float(score)
        for lower_bound, points in reversed(ranges): # Check from highest threshold down
            if numeric_score >= lower_bound:
                return float(points) # Return as float
    except (ValueError, TypeError):
        pass # If score is not a valid number, fall through to return 0
    return 0.0 # Default to 0.0 if no range matches or score is invalid

def map_raw_to_weighted_score(raw_score, mapping_table):
    """Maps a raw score to a weighted score using the provided table."""
    # Ensure raw_score is a number
    try:
        current_raw_score = float(raw_score)
    except (ValueError, TypeError):
        return 0.0 # Return 0.0 if raw_score is not a valid number

    weighted_score = 0.0
    # Iterate from highest threshold down to find the correct score
    for threshold, score_points in reversed(mapping_table):
        if current_raw_score >= threshold:
            weighted_score = score_points
            break # Found the correct bracket
    return float(weighted_score) # Ensure return is float

def calculate_pflegegrad(total_weighted_score):
    """Determines the Pflegegrad based on the total weighted score."""
    try:
        score = float(total_weighted_score)
    except (ValueError, TypeError):
        return "N/A" # Or 0 or specific error indicator

    if score >= 90: return 5
    elif score >= 70: return 4
    elif score >= 47.5: return 3
    elif score >= 27: return 2
    elif score >= 12.5: return 1
    else: return 0 # Kein Pflegegrad

def get_score(module_answers, question_key, default=0.0):
    """
    Safely retrieves the 'score' for a specific question key from a module's
    answer dictionary. Handles missing questions or missing 'score' keys.
    Returns score as float.
    """
    # Ensure question_key is treated as a string if your session keys are strings
    question_answer = module_answers.get(str(question_key), {})
    # Check if question_answer is a dictionary before getting 'score'
    if isinstance(question_answer, dict):
        score = question_answer.get('score', default)
        # Ensure score is numeric, default if not
        try:
            return float(score) if score is not None else float(default)
        except (ValueError, TypeError):
            return float(default)
    # If the stored answer wasn't a dictionary (e.g., for older modules maybe?), return default
    return float(default)

# --- Module 5 Calculation ---
import math # Make sure to import math at the top of your utils/calculations.py file

# You might already have this helper function defined outside calculate_module5_raw_score.
# If so, you don't need to redefine it inside. Ensure it's accessible.
# If it's ONLY defined inside the old function, keep this definition here.
def get_value(data, key, value_type='score', default=0):
    """Helper to safely get count or score."""
    item = data.get(str(key), {}) # Ensure key is string
    val = item.get(value_type, default)
    try:
        if value_type in ['score', 'count']: return float(val) if val is not None else float(default)
        return val
    except (ValueError, TypeError): return float(default) if value_type in ['score', 'count'] else default

# You might already have this helper function defined outside calculate_module5_raw_score.
# If so, you don't need to redefine it inside. Ensure it's accessible.
# If it's ONLY defined inside the old function, keep this definition here.
def get_freq_data(data, key):
    """Helper to get frequency data robustly."""
    item = data.get(str(key), {}) # Ensure key is string
    # Use the accessible get_value function
    count = get_value(data, key, 'count', 0)
    unit = item.get('unit', '').lower().strip()
    return count, unit

def calculate_module5_raw_score(answers):
    """
    Calculates the raw score for Module 5 based on official NBA guidelines (BRi).
    The final raw score is capped at 15.
    """
    print(f"DEBUG M5 Calc (Official): Input answers: {answers}")
    epsilon = 0.0001 # Small value for float comparisons

    # --- Part 1 (Kriterien 4.5.1 bis 4.5.7) ---
    part1_keys = [f'5.1.{i}' for i in range(1, 8)]
    daily_sum_p1, weekly_sum_p1, monthly_sum_p1 = 0.0, 0.0, 0.0
    for key in part1_keys:
        if key in answers:
            count, unit = get_freq_data(answers, key)
            if count > epsilon:
                if unit == 'pro tag': daily_sum_p1 += count
                elif unit == 'pro woche': weekly_sum_p1 += count
                elif unit == 'pro monat': monthly_sum_p1 += count
    # Rounding to 4 decimal places as per footnote 13 (applied to average)
    avg_per_day_p1 = round(daily_sum_p1 + (weekly_sum_p1 / 7.0) + (monthly_sum_p1 / 30.0), 4)

    points_part1 = 0.0
    if avg_per_day_p1 >= (8.0 + epsilon): points_part1 = 3.0 # mehr als achtmal täglich (>8)
    elif avg_per_day_p1 >= (3.0 + epsilon): points_part1 = 2.0 # mehr als dreimal bis maximal achtmal täglich (>3 to 8)
    elif avg_per_day_p1 >= (1.0 - epsilon): points_part1 = 1.0 # mindestens ein- bis maximal dreimal täglich (1 to 3)
    # else 0 points (implicitly)

    print(f"DEBUG M5 Part 1 (1-7): Avg={avg_per_day_p1:.4f}, Points={points_part1}")

    # --- Part 2 (Kriterien 4.5.8 bis 4.5.11) ---
    part2_keys = [f'5.2.{i}' for i in range(1, 5)] # Keys 5.2.1 to 5.2.4
    daily_sum_p2, weekly_sum_p2, monthly_sum_p2 = 0.0, 0.0, 0.0
    for key in part2_keys:
        if key in answers:
            count, unit = get_freq_data(answers, key)
            if count > epsilon:
                if unit == 'pro tag': daily_sum_p2 += count
                elif unit == 'pro woche': weekly_sum_p2 += count
                elif unit == 'pro monat': monthly_sum_p2 += count
    # Rounding to 4 decimal places as per footnote 13 (applied to average)
    avg_per_day_p2 = round(daily_sum_p2 + (weekly_sum_p2 / 7.0) + (monthly_sum_p2 / 30.0), 4)

    points_part2 = 0.0
    # Approx daily equivalent for 1/week is 1/7 = 0.142857...
    min_weekly_avg = 1.0 / 7.0
    if avg_per_day_p2 >= (3.0 - epsilon): points_part2 = 3.0 # mindestens dreimal täglich (>=3)
    elif avg_per_day_p2 >= (1.0 - epsilon): points_part2 = 2.0 # ein- bis unter dreimal täglich (1 to <3)
    elif avg_per_day_p2 >= (min_weekly_avg - epsilon): points_part2 = 1.0 # ein- bis mehrmals wöchentlich (>=1/wk to <1/day)
    # else 0 points (implicitly)

    print(f"DEBUG M5 Part 2 (8-11): Avg={avg_per_day_p2:.4f}, Points={points_part2}")

    # --- Part 3/4 (Kriterien 4.5.12 bis 4.5.15 + K) ---
    # Calculate base points according to official multipliers
    epsilon = 1e-6 # Small value for float comparisons
    base_points_p3_4 = 0.0

    # 4.5.12 (Zeitintensive) - Key 5.3.1 (assuming only one key for this)
    count, unit = get_freq_data(answers, '5.3.1')
    if count > epsilon:
        if unit == 'pro tag': base_points_p3_4 += count * 60.0
        elif unit == 'pro woche': base_points_p3_4 += count * 4.3
        elif unit == 'pro monat': base_points_p3_4 += count * 2.0

    # 4.5.13 (Arztbesuche) - Key 5.4.1
    count, unit = get_freq_data(answers, '5.4.1')
    if count > epsilon:
        if unit == 'pro woche': base_points_p3_4 += count * 4.3
        elif unit == 'pro monat': base_points_p3_4 += count * 2.0

    # 4.5.14 (Besuche < 3h) - Key 5.4.2
    count, unit = get_freq_data(answers, '5.4.2')
    if count > epsilon:
        if unit == 'pro woche': base_points_p3_4 += count * 4.3
        elif unit == 'pro monat': base_points_p3_4 += count * 2.0

    # 4.5.15 (Besuche > 3h) - Key 5.4.3
    count, unit = get_freq_data(answers, '5.4.3')
    if count > epsilon:
        if unit == 'pro woche': base_points_p3_4 += count * 4.3
        elif unit == 'pro monat': base_points_p3_4 += count * 1.0

    # 4.5.K (Frühförderung) - Add if you implement this, e.g., key '5.4.K'
    # count, unit = get_freq_data(answers, '5.4.K')
    # if count > epsilon:
    #     if unit == 'pro woche': base_points_p3_4 += count * 4.3
    #     elif unit == 'pro monat': base_points_p3_4 += count * 1.0

    # --- Map sum of base points to final points for this section ---
    points_part3_4 = 0.0
    if base_points_p3_4 >= (60.0 - epsilon):
        points_part3_4 = 6.0
    elif base_points_p3_4 >= (12.9 - epsilon): # Check for 3 points
        points_part3_4 = 3.0
    elif base_points_p3_4 >= (8.6 - epsilon):  # Check for 2 points
        points_part3_4 = 2.0
    elif base_points_p3_4 >= (4.3 - epsilon):  # Check for 1 point
        points_part3_4 = 1.0
    # else 0 points (implicitly) - Note: BRi doesn't specify points 2-5 for this section

    print(f"DEBUG M5 Part 3/4 (12-15+K): BasePointsSum={base_points_p3_4:.4f}, FinalPoints={points_part3_4:.1f}")

    # --- Part 5 (Kriterium 4.5.16) ---
    # Use the accessible get_value function
    points_part5 = get_value(answers, '5.5.1', 'score', 0)
    print(f"DEBUG M5 Part 5 (16): Points={points_part5}")

    # --- Final Raw Score Calculation for Module 5 (Official: SUM of parts) ---
    total_raw_score = points_part1 + points_part2 + points_part3_4 + points_part5

    # --- Apply the cap for Module 5 raw score (Max raw score for M5 is 15) ---
    # Although the official text implies the sum could exceed 15 (e.g., 3+3+6+3=15),
    # the weighted score table only goes up to 15 raw points. We'll cap at 15.
    final_raw_score = min(total_raw_score, 15.0)

    print(f"DEBUG M5 Final: P1={points_part1}, P2={points_part2}, P3/4={points_part3_4}, P5={points_part5}, TotalRaw={total_raw_score:.2f}, FinalRaw(Capped)={final_raw_score:.2f}")
    return final_raw_score
# --- End Module 5 Calculation ---


# --- Overall Score Calculation ---
def calculate_scores(all_answers):
    """
    Calculates raw scores, weighted scores, total score, and Pflegegrad
    based on the answers provided for all modules.
    'all_answers' is expected to be a dict like:
    { '1': { '0': {'score': 1, 'text': '...'}, '1': {...}, 'notes': '...', 'visited': True }, '2': {...}, ... }
    """
    print(f"DEBUG Calc Scores: Input all_answers keys: {list(all_answers.keys())}")
    results = {} # Final dictionary to return
    raw_scores = {} # Store raw scores per module
    weighted_scores = {} # Store weighted scores per module

    # --- Calculate Raw Scores for Modules 1, 2, 3, 4, 6 ---
    for module_id in [1, 2, 3, 4, 6]:
        module_id_str = str(module_id)
        module_answers = all_answers.get(module_id_str, {}) # Get answers for this module
        current_raw_score = 0.0
        # Iterate through the keys in this module's answers
        for question_key in module_answers.keys():
            # IMPORTANT: Only sum scores from keys that represent questions
            # Assuming question keys are stored as strings '0', '1', '2', etc.
            # Filter out keys like 'notes', 'visited', etc.
            if question_key.isdigit(): # Check if the key is a digit string
                # Use the TOP-LEVEL get_score function
                current_raw_score += get_score(module_answers, question_key, 0.0)

        raw_scores[module_id_str] = current_raw_score
        print(f"DEBUG Calc Scores: Module {module_id_str} Raw Score: {current_raw_score:.2f}")

    # --- Calculate Raw Score for Module 5 ---
    module5_answers = all_answers.get('5', {})
    # Check if module 5 has answers before calculating
    if module5_answers:
        raw_scores['5'] = calculate_module5_raw_score(module5_answers)
    else:
        raw_scores['5'] = 0.0 # Default if no answers for M5
    print(f"DEBUG Calc Scores: Module 5 Raw Score: {raw_scores['5']:.2f}")

    # --- Map Raw Scores to Weighted Scores ---
    for module_id_str, raw_score in raw_scores.items():
        if module_id_str in weighted_score_mapping_tables:
            mapping_table = weighted_score_mapping_tables[module_id_str]
            # Ensure raw_score is capped before mapping if necessary (M5 cap is inside its function)
            current_weighted = map_raw_to_weighted_score(raw_score, mapping_table)
            weighted_scores[module_id_str] = current_weighted
            print(f"DEBUG Calc Scores: Module {module_id_str} Weighted Score: {current_weighted:.2f}")
        else:
             # Should not happen with current tables, but good practice
             weighted_scores[module_id_str] = 0.0
             print(f"DEBUG Calc Scores: WARNING - No mapping table found for Module {module_id_str}")

    # --- Handle Special Case: Combine Modules 2 and 3 ---
    # Use the weighted scores already calculated
    weighted_m2 = weighted_scores.get('2', 0.0)
    weighted_m3 = weighted_scores.get('3', 0.0)
    # The higher weighted score between M2 and M3 contributes to the total
    combined_m2_m3_weighted = max(weighted_m2, weighted_m3)
    print(f"DEBUG Calc Scores: Combined M2/M3 Weighted (Max of {weighted_m2:.2f}, {weighted_m3:.2f}): {combined_m2_m3_weighted:.2f}")

    # --- Calculate Total Weighted Score ---
    # Sum weighted scores from M1, M4, M5, M6, and the combined M2/M3 score
    total_weighted = (
        weighted_scores.get('1', 0.0) +
        combined_m2_m3_weighted +
        weighted_scores.get('4', 0.0) +
        weighted_scores.get('5', 0.0) +
        weighted_scores.get('6', 0.0)
    )
    print(f"DEBUG Calc Scores: Total Weighted Score: {total_weighted:.2f}")

    # --- Determine Pflegegrad ---
    pflegegrad = calculate_pflegegrad(total_weighted)
    print(f"DEBUG Calc Scores: Calculated Pflegegrad: {pflegegrad}")

    # --- Structure Final Results ---
    # Store results in the format expected by the /results route template
    results = {
        'module_scores': {}, # Store individual module raw/weighted scores
        'total_weighted': round(total_weighted, 2),
        'pflegegrad': pflegegrad,
        'combined_m2_m3_weighted': round(combined_m2_m3_weighted, 2) # Store this for potential display
    }

    # Populate individual module scores
    for mod_id_str in raw_scores.keys():
        results['module_scores'][mod_id_str] = {
            'raw': round(raw_scores.get(mod_id_str, 0.0), 2),
            'weighted': round(weighted_scores.get(mod_id_str, 0.0), 2)
        }

    # Add the combined M2/M3 weighted score explicitly if needed for display logic
    # results['module_scores']['2_3_combined_weighted'] = round(combined_m2_m3_weighted, 2)

    print(f"DEBUG Calc Scores: Final results dictionary: {results}")
    return results
# --- End Overall Score Calculation ---