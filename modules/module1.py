# modules/module1.py

module1 = {
    'id': 1,
    'title': 'Modul 1: Mobilität', # Changed 'name' to 'title' for consistency
    'weight': 10, # Weight in percent for final score calculation
    'questions': {  # Changed from list [] to dictionary {}
        '1.1': {    # Key is the question ID string '1.1'
            'id': '1.1', # Optional: keep internal id if needed elsewhere
            'text': 'Positionswechsel im Bett',
            'explanation': 'Fähigkeit, sich im Bett selbständig zu drehen und aufzurichten.',
            'type': 'radio', # Added type for potential future use/consistency
            'answers': [ # Changed 'options' to 'answers' for consistency
                {'text': 'Selbständig', 'score': 0},
                {'text': 'Überwiegend selbständig', 'score': 1},
                {'text': 'Überwiegend unselbständig', 'score': 2},
                {'text': 'Unselbständig', 'score': 3}
            ]
        },
        '1.2': {    # Key is the question ID string '1.2'
            'id': '1.2',
            'text': 'Halten einer stabilen Sitzposition',
            'explanation': 'Fähigkeit, ohne oder mit nur geringer Unterstützung aufrecht zu sitzen.',
            'type': 'radio',
            'answers': [ # Changed 'options' to 'answers'
                {'text': 'Selbständig', 'score': 0},
                {'text': 'Überwiegend selbständig', 'score': 1},
                {'text': 'Überwiegend unselbständig', 'score': 2},
                {'text': 'Unselbständig', 'score': 3}
            ]
        },
        '1.3': {    # Key is the question ID string '1.3'
            'id': '1.3',
            'text': 'Umsetzen',
            'explanation': 'Fähigkeit, z.B. vom Bett in den Rollstuhl oder auf einen Stuhl zu wechseln.',
            'type': 'radio',
            'answers': [ # Changed 'options' to 'answers'
                {'text': 'Selbständig', 'score': 0},
                {'text': 'Überwiegend selbständig', 'score': 1},
                {'text': 'Überwiegend unselbständig', 'score': 2},
                {'text': 'Unselbständig', 'score': 3}
            ]
        },
        '1.4': {    # Key is the question ID string '1.4'
            'id': '1.4',
            'text': 'Fortbewegen innerhalb des Wohnbereichs',
            'explanation': 'Fähigkeit, sich in der Wohnung (auch mit Hilfsmitteln wie Rollator) fortzubewegen.',
            'type': 'radio',
            'answers': [ # Changed 'options' to 'answers'
                {'text': 'Selbständig', 'score': 0},
                {'text': 'Überwiegend selbständig', 'score': 1},
                {'text': 'Überwiegend unselbständig', 'score': 2},
                {'text': 'Unselbständig', 'score': 3}
            ]
        },
        '1.5': {    # Key is the question ID string '1.5'
            'id': '1.5',
            'text': 'Treppensteigen',
            'explanation': 'Fähigkeit, eine Treppe (mind. eine Etage) auf- und abzusteigen.',
            'type': 'radio',
            'answers': [ # Changed 'options' to 'answers'
                {'text': 'Selbständig', 'score': 0},
                {'text': 'Überwiegend selbständig', 'score': 1},
                {'text': 'Überwiegend unselbständig', 'score': 2},
                {'text': 'Unselbständig', 'score': 3}
            ]
        }
    } # End of questions dictionary
} # End of module1 dictionary