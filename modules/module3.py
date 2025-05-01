# modules/module3.py
"""
Module 3: Verhaltensweisen und psychische Problemlagen
Weight: Combined with M2 for NBA scoring (15% placeholder)
"""

module3 = {
    'id': 3,
    'title': "Modul 3: Verhaltensweisen und psychische Problemlagen",
    'weight': 0.15, # Placeholder weight, actual calculation combines M2 & M3
    'questions': {
        '3.1': {
            'id': '3.1',
            'text': "Motorisch geprägte Verhaltensauffälligkeiten",
            'explanation': "Bewertet wird das Auftreten von körperlicher Unruhe, ziellosem Umherlaufen, Bewegungsstereotypien.",
            'type': 'radio', # **** CHANGED 'frequency' TO 'radio' ****
            'answers': [
                {"score": 0, "text": "Nie oder sehr selten"}, # Removed option_explanation for consistency
                {"score": 1, "text": "Selten (1-3 Mal pro Woche)"},
                {"score": 3, "text": "Häufig (mehrmals pro Woche bis täglich)"},
                {"score": 5, "text": "Täglich mehrmals"}
            ]
        },
        '3.2': {
            'id': '3.2',
            'text': "Nächtliche Unruhe",
            'explanation': "Bewertet wird nächtliches Umherirren, Aufstehen, Rufen oder andere Störungen der Nachtruhe.",
            'type': 'radio', # **** CHANGED 'frequency' TO 'radio' ****
            'answers': [
                {"score": 0, "text": "Nie oder sehr selten"},
                {"score": 1, "text": "Selten (1-3 Mal pro Woche)"},
                {"score": 3, "text": "Häufig (mehrmals pro Woche bis täglich)"},
                {"score": 5, "text": "Täglich mehrmals"}
            ]
        },
        '3.3': {
            'id': '3.3',
            'text': "Selbstschädigendes und autoaggressives Verhalten",
            'explanation': "Bewertet wird Verhalten wie sich selbst schlagen, kratzen, beißen oder Kopf anschlagen.",
            'type': 'radio', # **** CHANGED 'frequency' TO 'radio' ****
            'answers': [
                {"score": 0, "text": "Nie oder sehr selten"},
                {"score": 1, "text": "Selten (1-3 Mal pro Woche)"},
                {"score": 3, "text": "Häufig (mehrmals pro Woche bis täglich)"},
                {"score": 5, "text": "Täglich mehrmals"}
            ]
        },
        '3.4': {
            'id': '3.4',
            'text': "Beschädigen von Gegenständen",
            'explanation': "Bewertet wird das Zerstören oder Beschädigen von Mobiliar, Kleidung oder anderen Gegenständen.",
            'type': 'radio', # **** CHANGED 'frequency' TO 'radio' ****
            'answers': [
                {"score": 0, "text": "Nie oder sehr selten"},
                {"score": 1, "text": "Selten (1-3 Mal pro Woche)"},
                {"score": 3, "text": "Häufig (mehrmals pro Woche bis täglich)"},
                {"score": 5, "text": "Täglich mehrmals"}
            ]
        },
        '3.5': {
            'id': '3.5',
            'text': "Physisch aggressives Verhalten gegenüber anderen Personen",
            'explanation': "Bewertet wird körperliche Aggression wie Schlagen, Treten, Beißen, Stoßen gegenüber anderen.",
            'type': 'radio', # **** CHANGED 'frequency' TO 'radio' ****
            'answers': [
                {"score": 0, "text": "Nie oder sehr selten"},
                {"score": 1, "text": "Selten (1-3 Mal pro Woche)"},
                {"score": 3, "text": "Häufig (mehrmals pro Woche bis täglich)"},
                {"score": 5, "text": "Täglich mehrmals"}
            ]
        },
        '3.6': {
            'id': '3.6',
            'text': "Verbale Aggression",
            'explanation': "Bewertet wird aggressives verbales Verhalten wie Beschimpfen, Schreien, Fluchen.",
            'type': 'radio', # **** CHANGED 'frequency' TO 'radio' ****
            'answers': [
                {"score": 0, "text": "Nie oder sehr selten"},
                {"score": 1, "text": "Selten (1-3 Mal pro Woche)"},
                {"score": 3, "text": "Häufig (mehrmals pro Woche bis täglich)"},
                {"score": 5, "text": "Täglich mehrmals"}
            ]
        },
        '3.7': {
            'id': '3.7',
            'text': "Andere pflegerelevante vokale Auffälligkeiten",
            'explanation': "Bewertet wird ständiges Rufen, Jammern, Klagen oder Stöhnen ohne direkten Bezug zu Schmerz oder Bedürfnis.",
            'type': 'radio', # **** CHANGED 'frequency' TO 'radio' ****
            'answers': [
                {"score": 0, "text": "Nie oder sehr selten"},
                {"score": 1, "text": "Selten (1-3 Mal pro Woche)"},
                {"score": 3, "text": "Häufig (mehrmals pro Woche bis täglich)"},
                {"score": 5, "text": "Täglich mehrmals"}
            ]
        },
        '3.8': {
            'id': '3.8',
            'text': "Abwehr von pflegerischen oder anderen unterstützenden Maßnahmen",
            'explanation': "Bewertet wird Widerstand oder Abwehr gegenüber notwendiger Hilfe bei Körperpflege, Essen, Mobilisation etc.",
            'type': 'radio', # **** CHANGED 'frequency' TO 'radio' ****
            'answers': [
                {"score": 0, "text": "Nie oder sehr selten"},
                {"score": 1, "text": "Selten (1-3 Mal pro Woche)"},
                {"score": 3, "text": "Häufig (mehrmals pro Woche bis täglich)"},
                {"score": 5, "text": "Täglich mehrmals"}
            ]
        },
        '3.9': {
            'id': '3.9',
            'text': "Wahnvorstellungen",
            'explanation': "Bewertet wird das Äußern von unrealistischen, unkorrigierbaren Überzeugungen (z.B. Verfolgungswahn).",
            'type': 'radio', # **** CHANGED 'frequency' TO 'radio' ****
            'answers': [
                {"score": 0, "text": "Nie oder sehr selten"},
                {"score": 1, "text": "Selten (1-3 Mal pro Woche)"},
                {"score": 3, "text": "Häufig (mehrmals pro Woche bis täglich)"},
                {"score": 5, "text": "Täglich mehrmals"}
            ]
        },
        '3.10': {
             'id': '3.10',
             'text': "Ängste",
             'explanation': "Bewertet wird das Äußern oder Zeigen von Ängsten (z.B. Angst vor Alleinsein, Dunkelheit, bestimmten Situationen).",
             'type': 'radio', # **** CHANGED 'frequency' TO 'radio' ****
             'answers': [
                 {"score": 0, "text": "Nie oder sehr selten"},
                 {"score": 1, "text": "Selten (1-3 Mal pro Woche)"},
                 {"score": 3, "text": "Häufig (mehrmals pro Woche bis täglich)"},
                 {"score": 5, "text": "Täglich mehrmals"}
             ]
         },
         '3.11': {
             'id': '3.11',
             'text': "Antriebslosigkeit bei vorhandener Aktivierungsfähigkeit",
             'explanation': "Bewertet wird mangelnder Antrieb oder Initiative, obwohl die Person körperlich dazu fähig wäre und aktiviert werden kann.",
             'type': 'radio', # **** CHANGED 'frequency' TO 'radio' ****
             'answers': [
                 {"score": 0, "text": "Nie oder sehr selten"},
                 {"score": 1, "text": "Selten (1-3 Mal pro Woche)"},
                 {"score": 3, "text": "Häufig (mehrmals pro Woche bis täglich)"},
                 {"score": 5, "text": "Täglich mehrmals"}
             ]
         },
         '3.12': {
             'id': '3.12',
             'text': "Depressive Stimmungslage",
             'explanation': "Bewertet wird das Vorhandensein von Traurigkeit, Hoffnungslosigkeit, sozialem Rückzug.",
             'type': 'radio', # **** CHANGED 'frequency' TO 'radio' ****
             'answers': [
                 {"score": 0, "text": "Nie oder sehr selten"},
                 {"score": 1, "text": "Selten (1-3 Mal pro Woche)"},
                 {"score": 3, "text": "Häufig (mehrmals pro Woche bis täglich)"},
                 {"score": 5, "text": "Täglich mehrmals"}
             ]
         },
         '3.13': {
             'id': '3.13',
             'text': "Unangemessenes Verhalten in sozialen Situationen",
             'explanation': "Bewertet wird sozial unangepasstes Verhalten wie Distanzlosigkeit, sexuell übergriffiges Verhalten, lautes Schimpfen in der Öffentlichkeit.",
             'type': 'radio', # **** CHANGED 'frequency' TO 'radio' ****
             'answers': [
                 {"score": 0, "text": "Nie oder sehr selten"},
                 {"score": 1, "text": "Selten (1-3 Mal pro Woche)"},
                 {"score": 3, "text": "Häufig (mehrmals pro Woche bis täglich)"},
                 {"score": 5, "text": "Täglich mehrmals"}
             ]
         }
    }
}