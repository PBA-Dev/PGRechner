# modules/module6.py
"""
Module 6: Gestaltung des Alltagslebens und sozialer Kontakte
Weight: 15% (0.15)
"""

module6 = {
    'id': 6,
    'title': "Modul 6: Gestaltung des Alltagslebens und sozialer Kontakte", # Changed 'name' to 'title'
    'weight': 0.15,
    'questions': { # Changed from list [] to dictionary {}
        '6.1': { # Key is the question ID string '6.1'
            'id': '6.1', # Added id key
            'text': "Gestaltung des Tagesablaufs und Anpassung an Veränderungen",
            'explanation': "Bewertet wird die Fähigkeit, den eigenen Tagesablauf nach persönlichen Vorlieben zu gestalten und sich auf Änderungen einzustellen.",
            'type': 'radio', # Added type
            'answers': [ # Changed 'options' to 'answers'
                {"score": 0, "text": "Selbstständig"}, # Removed option_explanation
                {"score": 1, "text": "Überwiegend selbstständig"},
                {"score": 2, "text": "Überwiegend unselbstständig"},
                {"score": 3, "text": "Unselbstständig"}
            ]
        },
        '6.2': { # Key is the question ID string '6.2'
            'id': '6.2',
            'text': "Ruhen und Schlafen",
            'explanation': "Bewertet wird die Fähigkeit, Ruhephasen und den Nachtschlaf nach eigenem Bedürfnis zu gestalten (z.B. zu Bett gehen, aufstehen).",
            'type': 'radio',
            'answers': [ # Changed 'options' to 'answers'
                {"score": 0, "text": "Selbstständig"},
                {"score": 1, "text": "Überwiegend selbstständig"},
                {"score": 2, "text": "Überwiegend unselbstständig"},
                {"score": 3, "text": "Unselbstständig"}
            ]
        },
        '6.3': { # Key is the question ID string '6.3'
            'id': '6.3',
            'text': "Sich beschäftigen",
            'explanation': "Bewertet wird die Fähigkeit, sich selbstständig mit Dingen zu beschäftigen, die von persönlichem Interesse sind.",
            'type': 'radio',
            'answers': [ # Changed 'options' to 'answers'
                {"score": 0, "text": "Selbstständig"},
                {"score": 1, "text": "Überwiegend selbstständig"},
                {"score": 2, "text": "Überwiegend unselbstständig"},
                {"score": 3, "text": "Unselbstständig"}
            ]
        },
        '6.4': { # Key is the question ID string '6.4'
            'id': '6.4',
            'text': "Vornehmen von in die Zukunft gerichteten Planungen",
            'explanation': "Bewertet wird die Fähigkeit, zukünftige Aktivitäten oder Ereignisse (z.B. Arzttermine, Besuche, Einkäufe) zu planen.",
            'type': 'radio',
            'answers': [ # Changed 'options' to 'answers'
                {"score": 0, "text": "Selbstständig"},
                {"score": 1, "text": "Überwiegend selbstständig"},
                {"score": 2, "text": "Überwiegend unselbstständig"},
                {"score": 3, "text": "Unselbstständig"}
            ]
        },
        '6.5': { # Key is the question ID string '6.5'
            'id': '6.5',
            'text': "Interaktion mit Personen im direkten Kontakt",
            'explanation': "Bewertet wird die Fähigkeit, im direkten Kontakt mit bekannten oder unbekannten Personen angemessen zu interagieren.",
            'type': 'radio',
            'answers': [ # Changed 'options' to 'answers'
                {"score": 0, "text": "Selbstständig"},
                {"score": 1, "text": "Überwiegend selbstständig"},
                {"score": 2, "text": "Überwiegend unselbstständig"},
                {"score": 3, "text": "Unselbstständig"}
            ]
        },
        '6.6': { # Key is the question ID string '6.6'
            'id': '6.6',
            'text': "Kontaktpflege zu Personen außerhalb des direkten Umfelds",
            'explanation': "Bewertet wird die Fähigkeit, Kontakte zu Angehörigen, Freunden oder Bekannten aufrechtzuerhalten (z.B. Telefonieren, Briefe schreiben, Besuche empfangen/machen).",
            'type': 'radio',
            'answers': [ # Changed 'options' to 'answers'
                {"score": 0, "text": "Selbstständig"},
                {"score": 1, "text": "Überwiegend selbstständig"},
                {"score": 2, "text": "Überwiegend unselbstständig"},
                {"score": 3, "text": "Unselbstständig"}
            ]
        }
    } # End of questions dictionary
} # End of module6 dictionary