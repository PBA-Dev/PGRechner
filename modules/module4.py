# modules/module4.py

module4 = {
    'id': 4,
    'title': 'Modul 4: Selbstversorgung', # Changed 'name' to 'title'
    'weight': 40, # Weight in percent for final score calculation
    'questions': { # Changed from list [] to dictionary {}
        '4.1': { # Key is the question ID string '4.1'
            'id': '4.1',
            'text': 'Waschen des vorderen Oberkörpers',
            'explanation': 'Beinhaltet das Waschen von Händen, Gesicht, Hals, Armen, Achselhöhlen und vorderem Oberkörper.',
            'type': 'radio', # Added type
            'answers': [ # Changed 'options' to 'answers'
                {'text': 'Selbständig', 'score': 0},
                {'text': 'Überwiegend selbständig', 'score': 1},
                {'text': 'Überwiegend unselbständig', 'score': 2},
                {'text': 'Unselbständig', 'score': 3}
            ]
        },
        '4.2': { # Key is the question ID string '4.2'
            'id': '4.2',
            'text': 'Körperpflege im Bereich des Kopfes',
            'explanation': 'Beinhaltet Kämmen, Zahnpflege/Prothesenreinigung, Rasieren.',
            'type': 'radio',
            'answers': [ # Changed 'options' to 'answers'
                {'text': 'Selbständig', 'score': 0},
                {'text': 'Überwiegend selbständig', 'score': 1},
                {'text': 'Überwiegend unselbständig', 'score': 2},
                {'text': 'Unselbständig', 'score': 3}
            ]
        },
        '4.3': { # Key is the question ID string '4.3'
            'id': '4.3',
            'text': 'Waschen des Intimbereichs',
            'explanation': 'Beinhaltet das Waschen des Intimbereichs und das Abtrocknen.',
            'type': 'radio',
            'answers': [ # Changed 'options' to 'answers'
                {'text': 'Selbständig', 'score': 0},
                {'text': 'Überwiegend selbständig', 'score': 1},
                {'text': 'Überwiegend unselbständig', 'score': 2},
                {'text': 'Unselbständig', 'score': 3}
            ]
        },
        '4.4': { # Key is the question ID string '4.4'
            'id': '4.4',
            'text': 'Duschen und Baden einschließlich Waschen der Haare',
            'explanation': 'Umfasst Ganzkörperwäsche in Dusche oder Badewanne, einschließlich Haare waschen und Abtrocknen.',
            'type': 'radio',
            'answers': [ # Changed 'options' to 'answers'
                {'text': 'Selbständig', 'score': 0},
                {'text': 'Überwiegend selbständig', 'score': 1},
                {'text': 'Überwiegend unselbständig', 'score': 2},
                {'text': 'Unselbständig', 'score': 3}
            ]
        },
        '4.5': { # Key is the question ID string '4.5'
            'id': '4.5',
            'text': 'An- und Auskleiden des Oberkörpers',
            'explanation': 'Beinhaltet das An- und Ausziehen von Hemd, Bluse, Pullover, Unterhemd, BH etc.',
            'type': 'radio',
            'answers': [ # Changed 'options' to 'answers'
                {'text': 'Selbständig', 'score': 0},
                {'text': 'Überwiegend selbständig', 'score': 1},
                {'text': 'Überwiegend unselbständig', 'score': 2},
                {'text': 'Unselbständig', 'score': 3}
            ]
        },
        '4.6': { # Key is the question ID string '4.6'
            'id': '4.6',
            'text': 'An- und Auskleiden des Unterkörpers',
            'explanation': 'Beinhaltet das An- und Ausziehen von Hose, Rock, Unterhose, Strümpfen, Schuhen.',
            'type': 'radio',
            'answers': [ # Changed 'options' to 'answers'
                {'text': 'Selbständig', 'score': 0},
                {'text': 'Überwiegend selbständig', 'score': 1},
                {'text': 'Überwiegend unselbständig', 'score': 2},
                {'text': 'Unselbständig', 'score': 3}
            ]
        },
        '4.7': { # Key is the question ID string '4.7'
            'id': '4.7',
            'text': 'Mundgerechtes Zubereiten der Nahrung und Eingießen von Getränken',
            'explanation': 'Beinhaltet das Zerkleinern von Speisen, Öffnen von Verpackungen, Eingießen von Getränken.',
            'type': 'radio',
            'answers': [ # Changed 'options' to 'answers'
                {'text': 'Selbständig', 'score': 0},
                {'text': 'Überwiegend selbständig', 'score': 1},
                {'text': 'Überwiegend unselbständig', 'score': 2},
                {'text': 'Unselbständig', 'score': 3}
            ]
        },
        # --- Start of second part ---
        '4.8': { # Key is the question ID string '4.8'
            'id': '4.8',
            'text': 'Essen',
            'explanation': 'Beinhaltet das Führen des Essens zum Mund, Abbeißen, Kauen, Schlucken.',
            'type': 'radio',
            'answers': [ # Changed 'options' to 'answers'
                {'text': 'Selbständig', 'score': 0},
                {'text': 'Überwiegend selbständig', 'score': 3}, # Note different scoring
                {'text': 'Überwiegend unselbständig', 'score': 6}, # Note different scoring
                {'text': 'Unselbständig', 'score': 9}             # Note different scoring
            ]
        },
        '4.9': { # Key is the question ID string '4.9'
            'id': '4.9',
            'text': 'Trinken',
            'explanation': 'Beinhaltet das Ergreifen des Trinkgefäßes, Führen zum Mund, Trinken.',
            'type': 'radio',
            'answers': [ # Changed 'options' to 'answers'
                {'text': 'Selbständig', 'score': 0},
                {'text': 'Überwiegend selbständig', 'score': 2}, # Note different scoring
                {'text': 'Überwiegend unselbständig', 'score': 4}, # Note different scoring
                {'text': 'Unselbständig', 'score': 6}             # Note different scoring
            ]
        },
        '4.10': { # Key is the question ID string '4.10'
             'id': '4.10',
             'text': 'Benutzen einer Toilette oder eines Toilettenstuhls',
             'explanation': 'Umfasst Hinsetzen, Aufstehen, Sitzen während der Blasen-/Darmentleerung, Intimhygiene, Richten der Kleidung.',
             'type': 'radio',
             'answers': [ # Changed 'options' to 'answers'
                 {'text': 'Selbständig', 'score': 0},
                 {'text': 'Überwiegend selbständig', 'score': 2}, # Note different scoring
                 {'text': 'Überwiegend unselbständig', 'score': 4}, # Note different scoring
                 {'text': 'Unselbständig', 'score': 6}             # Note different scoring
             ]
         },
         '4.11': { # Key is the question ID string '4.11'
             'id': '4.11',
             'text': 'Bewältigen der Folgen einer Harninkontinenz und Umgang mit Dauerkatheter und Urostoma',
             'explanation': 'Beinhaltet das Wechseln von Inkontinenzmaterial, Umgang mit Katheter/Urostoma, Entsorgung.',
             'type': 'radio',
             'answers': [ # Changed 'options' to 'answers'
                 {'text': 'Selbständig', 'score': 0},
                 {'text': 'Überwiegend selbständig', 'score': 1},
                 {'text': 'Überwiegend unselbständig', 'score': 2},
                 {'text': 'Unselbständig', 'score': 3}
             ]
         },
         '4.12': { # Key is the question ID string '4.12'
             'id': '4.12',
             'text': 'Bewältigen der Folgen einer Stuhlinkontinenz und Umgang mit Stoma',
             'explanation': 'Beinhaltet das Wechseln von Inkontinenzmaterial, Umgang mit Stoma, Entsorgung.',
             'type': 'radio',
             'answers': [ # Changed 'options' to 'answers'
                 {'text': 'Selbständig', 'score': 0},
                 {'text': 'Überwiegend selbständig', 'score': 1},
                 {'text': 'Überwiegend unselbständig', 'score': 2},
                 {'text': 'Unselbständig', 'score': 3}
             ]
         },
         '4.13': { # Key is the question ID string '4.13'
             'id': '4.13',
             'text': 'Ernährung parenteral oder über Sonde',
             'explanation': 'Bewertung der Notwendigkeit künstlicher Ernährung.',
             'type': 'radio', # Assuming radio type despite different options
             'answers': [ # Changed 'options' to 'answers'
                 {'text': 'Keine, nicht täglich, nicht auf Dauer', 'score': 0},
                 {'text': 'Täglich, zusätzlich zu oraler Nahrung', 'score': 6}, # Score needs verification
                 {'text': 'Ausschließlich oder nahezu ausschließlich', 'score': 3} # Score needs verification
                 # NOTE: The exact scoring (0, 6, 3?) needs verification against official NBA guidelines.
             ]
         }
        # --- End of second part ---
    } # End of questions dictionary
} # End of module4 dictionary