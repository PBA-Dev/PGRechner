# config/pflegegrad_config.py

"""
Pflegegrad configuration, weights, and thresholds
"""

# Defines the mapping from total weighted score ranges to Pflegegrad
# The key is a tuple (min_score, max_score), value is the Pflegegrad (int)
# Note: max_score is exclusive in the check (score < max_score)
SCORE_TO_PFLEGEGRAD = {
    (0, 12.5): 0,      # Score >= 0 and < 12.5
    (12.5, 27): 1,     # Score >= 12.5 and < 27
    (27, 47.5): 2,     # Score >= 27 and < 47.5
    (47.5, 70): 3,     # Score >= 47.5 and < 70
    (70, 90): 4,      # Score >= 70 and < 90
    (90, 100.1): 5     # Score >= 90 and <= 100 (using 100.1 makes < check work for 100)
}

# Defines the weighting factor for each module's raw score
MODULE_WEIGHTS = {
    1: 0.10,  # Modul 1: Mobilität
    2: 0.15,  # Modul 2: Kognitive und kommunikative Fähigkeiten (Weight applied to max(M2, M3))
    3: 0.15,  # Modul 3: Verhaltensweisen und psychische Problemlagen (Weight applied to max(M2, M3))
    4: 0.20,  # Modul 4: Selbstversorgung
    5: 0.15,  # Modul 5: Bewältigung von und selbständiger Umgang mit krankheits- oder therapiebedingten Anforderungen und Belastungen (Placeholder - review NBA rules for integration)
    6: 0.15,  # Modul 6: Gestaltung des Alltagslebens und sozialer Kontakte
}

# Defines maximum possible raw points for each module (optional, based on NBA guidelines)
# If a module's calculated raw score exceeds this cap, it will be capped.
# Leave empty or comment out if no caps are needed.
MODULE_POINT_CAPS = {
    # Example caps (adjust based on official NBA documents):
    # 1: 18, # Max points for Module 1
    # 2: 27, # Max points for Module 2
    # 3: 15, # Max points for Module 3
    # 4: 40, # Max points for Module 4
    # 5: 20, # Max points for Module 5
    # 6: 24, # Max points for Module 6
}

# You can add other configuration constants here if needed