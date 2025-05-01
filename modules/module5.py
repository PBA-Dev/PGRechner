# modules/module5.py

module5 = {
    'id': 5,
    'title': 'Modul 5: Bewältigung von und selbständiger Umgang mit krankheits- oder therapiebedingten Anforderungen und Belastungen', # Changed 'name' to 'title'
    'weight': 20, # Weight in percent for final score calculation
    # The 'parts' structure is removed, questions are now top-level
    'questions': { # Top-level dictionary for all questions
        # --- Questions from Part 5.1 ---
        '5.1.1': {
            'id': '5.1.1',
            'text': 'Medikation',
            'explanation': 'Regelmäßige Medikamenteneinnahme.',
            'type': 'frequency',
            'answers': [{'text': 'Entfällt'}, {'text': 'Selbständig'}], # Changed 'options' to 'answers'
            'frequency_units': ['pro Tag', 'pro Woche', 'pro Monat']
            # Scoring logic based on frequency needed later
        },
        '5.1.2': {
            'id': '5.1.2',
            'text': 'Injektionen (subcutan und intramuskulär)',
            'explanation': 'Verabreichung von Injektionen.',
            'type': 'frequency',
            'answers': [{'text': 'Entfällt'}, {'text': 'Selbständig'}], # Changed 'options' to 'answers'
            'frequency_units': ['pro Tag', 'pro Woche', 'pro Monat']
        },
        '5.1.3': {
            'id': '5.1.3',
            'text': 'Versorgung intravenöser Zugänge (Port)',
            'explanation': 'Pflege und Nutzung von IV-Zugängen.',
            'type': 'frequency',
            'answers': [{'text': 'Entfällt'}, {'text': 'Selbständig'}], # Changed 'options' to 'answers'
            'frequency_units': ['pro Tag', 'pro Woche', 'pro Monat']
        },
        '5.1.4': {
            'id': '5.1.4',
            'text': 'Absaugen und Sauerstoffgabe',
            'explanation': 'Notwendigkeit von Absaugung oder Sauerstoff.',
            'type': 'frequency',
            'answers': [{'text': 'Entfällt'}, {'text': 'Selbständig'}], # Changed 'options' to 'answers'
            'frequency_units': ['pro Tag', 'pro Woche', 'pro Monat']
        },
        '5.1.5': {
            'id': '5.1.5',
            'text': 'Einreibungen oder Kälte- und Wärmeanwendungen',
            'explanation': 'Anwendung von Salben, Cremes, Kälte-/Wärmepackungen.',
            'type': 'frequency',
            'answers': [{'text': 'Entfällt'}, {'text': 'Selbständig'}], # Changed 'options' to 'answers'
            'frequency_units': ['pro Tag', 'pro Woche', 'pro Monat']
        },
        '5.1.6': {
            'id': '5.1.6',
            'text': 'Messung und Deutung von Körperzuständen',
            'explanation': 'Blutzucker-, Blutdruckmessung etc.',
            'type': 'frequency',
            'answers': [{'text': 'Entfällt'}, {'text': 'Selbständig'}], # Changed 'options' to 'answers'
            'frequency_units': ['pro Tag', 'pro Woche', 'pro Monat']
        },
        '5.1.7': {
            'id': '5.1.7',
            'text': 'Körpernahe Hilfsmittel',
            'explanation': 'Umgang mit Prothesen, Orthesen, Kompressionsstrümpfen etc.',
            'type': 'frequency',
            'answers': [{'text': 'Entfällt'}, {'text': 'Selbständig'}], # Changed 'options' to 'answers'
            'frequency_units': ['pro Tag', 'pro Woche', 'pro Monat']
        },
        # --- Questions from Part 5.2 ---
        '5.2.1': {
            'id': '5.2.1',
            'text': 'Verbandswechsel und Wundversorgung',
            'explanation': 'Versorgung von Wunden, Anlegen von Verbänden.',
            'type': 'frequency',
            'answers': [{'text': 'Entfällt'}, {'text': 'Selbständig'}], # Changed 'options' to 'answers'
            'frequency_units': ['pro Tag', 'pro Woche', 'pro Monat']
        },
        '5.2.2': {
            'id': '5.2.2',
            'text': 'Versorgung mit Stoma',
            'explanation': 'Pflege und Wechsel von Stomabeuteln.',
            'type': 'frequency',
            'answers': [{'text': 'Entfällt'}, {'text': 'Selbständig'}], # Changed 'options' to 'answers'
            'frequency_units': ['pro Tag', 'pro Woche', 'pro Monat']
        },
        '5.2.3': {
            'id': '5.2.3',
            'text': 'Regelmäßige Einmalkatheterisierung und Nutzung von Abführmethoden',
            'explanation': 'Durchführung von Katheterisierung oder Abführmaßnahmen.',
            'type': 'frequency',
            'answers': [{'text': 'Entfällt'}, {'text': 'Selbständig'}], # Changed 'options' to 'answers'
            'frequency_units': ['pro Tag', 'pro Woche', 'pro Monat']
        },
        '5.2.4': {
            'id': '5.2.4',
            'text': 'Therapiemaßnahmen in der häuslichen Umgebung',
            'explanation': 'Durchführung von z.B. Physiotherapie, Ergotherapie zu Hause.',
            'type': 'frequency',
            'answers': [{'text': 'Entfällt'}, {'text': 'Selbständig'}], # Changed 'options' to 'answers'
            'frequency_units': ['pro Tag', 'pro Woche', 'pro Monat']
        },
        # --- Questions from Part 5.3 ---
        '5.3.1': {
            'id': '5.3.1',
            'text': 'Zeit- und technikintensive Maßnahmen in häuslicher Umgebung',
            'explanation': 'z.B. Beatmung, Dialyse.',
            'type': 'frequency',
            'answers': [{'text': 'Entfällt'}, {'text': 'Selbständig'}], # Changed 'options' to 'answers'
            'frequency_units': ['pro Tag', 'pro Woche', 'pro Monat'] # Check units needed
        },
        # --- Questions from Part 5.4 ---
        '5.4.1': {
            'id': '5.4.1',
            'text': 'Arztbesuche',
            'explanation': 'Häufigkeit von Arztbesuchen.',
            'type': 'frequency',
            'answers': [{'text': 'Entfällt'}, {'text': 'Selbständig'}], # Changed 'options' to 'answers'
            'frequency_units': ['pro Woche', 'pro Monat'] # Units from doc
        },
        '5.4.2': {
            'id': '5.4.2',
            'text': 'Besuch anderer medizinischer oder therapeutischer Einrichtungen (bis zu drei Stunden)',
            'explanation': 'Termine bei Therapeuten, Sanitätshaus etc.',
            'type': 'frequency',
            'answers': [{'text': 'Entfällt'}, {'text': 'Selbständig'}], # Changed 'options' to 'answers'
            'frequency_units': ['pro Woche', 'pro Monat']
        },
        '5.4.3': {
            'id': '5.4.3',
            'text': 'Zeitlich ausgedehnte Besuche anderer medizinischer und therapeutischer Einrichtungen (länger als drei Stunden)',
            'explanation': 'Längere Termine, z.B. Tagesklinik.',
            'type': 'frequency',
            'answers': [{'text': 'Entfällt'}, {'text': 'Selbständig'}], # Changed 'options' to 'answers'
            'frequency_units': ['pro Woche', 'pro Monat']
        },
        # --- Questions from Part 5.5 ---
        '5.5.1': {
            'id': '5.5.1',
            'text': 'Einhaltung einer Diät und anderer krankheits- oder therapiebedingter Verhaltensvorschriften',
            'type': 'radio', # This one is radio button based
            'explanation': '', # Add explanation if available
            'answers': [ # Changed 'options' to 'answers'
                {'text': 'Entfällt/Selbständig', 'score': 0},
                {'text': 'Überwiegend selbständig', 'score': 1},
                {'text': 'Überwiegend unselbständig', 'score': 2},
                {'text': 'Unselbständig', 'score': 3}
            ]
        }
    } # End of top-level questions dictionary
    # Add function here later to calculate total raw score based on frequencies
} # End of module5 dictionary