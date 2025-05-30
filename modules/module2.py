# modules/module2.py
"""
Module 2: Kognitive und kommunikative Fähigkeiten
Weight: Combined with M3 for NBA scoring (15% placeholder)
"""

module2 = {
    'id': 2,
    'title': "Modul 2: Kognitive und kommunikative Fähigkeiten", # Changed 'name' to 'title'
    'weight': 0.15, # Placeholder weight, actual calculation combines M2 & M3
    'questions': { # Changed from list [] to dictionary {}
        '2.1': { # Key is the question ID string '2.1'
            'id': '2.1', # Added id key from text
            'text': "Erkennen von Personen aus dem näheren Umfeld",
            'explanation': "Bewertet wird die Fähigkeit, vertraute Personen (Angehörige, Pflegekräfte) zu erkennen.",
            'type': 'radio', # Added type
            'answers': [ # Changed 'options' to 'answers'
                {"score": 0, "text": "Fähigkeit vorhanden", "option_explanation": "Person erkennt vertraute Personen sicher."},
                {"score": 1, "text": "Fähigkeit größtenteils vorhanden", "option_explanation": "Person erkennt die meisten vertrauten Personen, manchmal unsicher oder verzögert."},
                {"score": 2, "text": "Fähigkeit in geringem Maße vorhanden", "option_explanation": "Person erkennt nur wenige vertraute Personen oder ist häufig unsicher."},
                {"score": 3, "text": "Fähigkeit nicht vorhanden", "option_explanation": "Person erkennt vertraute Personen nicht."}
            ]
        },
        '2.2': { # Key is the question ID string '2.2'
            'id': '2.2',
            'text': "Örtliche Orientierung",
            'explanation': "Bewertet wird die Fähigkeit, sich in der räumlichen Umgebung (Wohnung, Einrichtung) zurechtzufinden.",
            'type': 'radio',
            'answers': [ # Changed 'options' to 'answers'
                {"score": 0, "text": "Fähigkeit vorhanden", "option_explanation": "Person ist sicher orientiert bezüglich des Aufenthaltsortes (z.B. Zuhause, Krankenhaus)."},
                {"score": 1, "text": "Fähigkeit größtenteils vorhanden", "option_explanation": "Person ist meist orientiert, manchmal unsicher über den genauen Ort oder Stockwerk."},
                {"score": 2, "text": "Fähigkeit in geringem Maße vorhanden", "option_explanation": "Person ist häufig desorientiert, findet sich nur in sehr vertrauter Umgebung zurecht."},
                {"score": 3, "text": "Fähigkeit nicht vorhanden", "option_explanation": "Person weiß nicht, wo sie sich befindet."}
            ]
        },
        '2.3': { # Key is the question ID string '2.3'
            'id': '2.3',
            'text': "Zeitliche Orientierung",
            'explanation': "Bewertet wird das Wissen über Datum, Wochentag, Tageszeit oder Jahreszeit.",
            'type': 'radio',
            'answers': [ # Changed 'options' to 'answers'
                {"score": 0, "text": "Fähigkeit vorhanden", "option_explanation": "Person ist sicher zur Zeit orientiert (Datum, Tag, Tageszeit)."},
                {"score": 1, "text": "Fähigkeit größtenteils vorhanden", "option_explanation": "Person ist meist orientiert, macht aber Fehler (z.B. Datum, Wochentag)."},
                {"score": 2, "text": "Fähigkeit in geringem Maße vorhanden", "option_explanation": "Person hat nur grobe Zeitvorstellungen (z.B. Tageszeit, Jahreszeit)."},
                {"score": 3, "text": "Fähigkeit nicht vorhanden", "option_explanation": "Person hat keine Vorstellung von der Zeit."}
            ]
        },
        '2.4': { # Key is the question ID string '2.4'
            'id': '2.4',
            'text': "Erinnerung an wesentliche Ereignisse oder Beobachtungen",
            'explanation': "Bewertet wird die Fähigkeit, sich an kurz zurückliegende Ereignisse zu erinnern (Kurzzeitgedächtnis).",
            'type': 'radio',
            'answers': [ # Changed 'options' to 'answers'
                {"score": 0, "text": "Fähigkeit vorhanden", "option_explanation": "Person kann sich an Ereignisse der letzten Stunden/Tage erinnern."},
                {"score": 1, "text": "Fähigkeit größtenteils vorhanden", "option_explanation": "Person erinnert sich an das meiste, vergisst aber Details oder benötigt Gedächtnisstützen."},
                {"score": 2, "text": "Fähigkeit in geringem Maße vorhanden", "option_explanation": "Person erinnert sich nur bruchstückhaft oder an sehr markante Ereignisse."},
                {"score": 3, "text": "Fähigkeit nicht vorhanden", "option_explanation": "Person kann sich nicht an kurz zurückliegende Ereignisse erinnern."}
            ]
        },
        '2.5': { # Key is the question ID string '2.5'
            'id': '2.5',
            'text': "Steuern von mehrschrittigen Alltagshandlungen",
            'explanation': "Bewertet wird die Fähigkeit, Handlungen mit mehreren Schritten zu planen und durchzuführen (z.B. Tisch decken, Kaffee kochen).",
            'type': 'radio',
            'answers': [ # Changed 'options' to 'answers'
                {"score": 0, "text": "Fähigkeit vorhanden", "option_explanation": "Person kann komplexe Handlungen selbstständig planen und durchführen."},
                {"score": 1, "text": "Fähigkeit größtenteils vorhanden", "option_explanation": "Person kann Handlungen meist durchführen, benötigt aber gelegentlich Anleitung oder Korrektur."},
                {"score": 2, "text": "Fähigkeit in geringem Maße vorhanden", "option_explanation": "Person kann nur einfache Teilschritte durchführen oder benötigt ständige Anleitung."},
                {"score": 3, "text": "Fähigkeit nicht vorhanden", "option_explanation": "Person kann auch mit Anleitung keine mehrschrittigen Handlungen durchführen."}
            ]
        },
        '2.6': { # Key is the question ID string '2.6'
            'id': '2.6',
            'text': "Treffen von Entscheidungen im Alltagsleben",
            'explanation': "Bewertet wird die Fähigkeit, einfache Alltagsentscheidungen zu treffen (z.B. Kleiderwahl, Essensauswahl).",
            'type': 'radio',
            'answers': [ # Changed 'options' to 'answers'
                {"score": 0, "text": "Fähigkeit vorhanden", "option_explanation": "Person kann Entscheidungen selbstständig treffen."},
                {"score": 1, "text": "Fähigkeit größtenteils vorhanden", "option_explanation": "Person kann meist Entscheidungen treffen, benötigt aber manchmal Unterstützung oder Bestätigung."},
                {"score": 2, "text": "Fähigkeit in geringem Maße vorhanden", "option_explanation": "Person kann nur bei sehr einfachen Alternativen wählen oder überlässt Entscheidungen oft anderen."},
                {"score": 3, "text": "Fähigkeit nicht vorhanden", "option_explanation": "Person kann keine Entscheidungen treffen."}
            ]
        },
        '2.7': { # Key is the question ID string '2.7'
            'id': '2.7',
            'text': "Verstehen von Sachverhalten und Informationen",
            'explanation': "Bewertet wird die Fähigkeit, Informationen und Erklärungen zu verstehen.",
            'type': 'radio',
            'answers': [ # Changed 'options' to 'answers'
                {"score": 0, "text": "Fähigkeit vorhanden", "option_explanation": "Person versteht komplexe Informationen und Erklärungen."},
                {"score": 1, "text": "Fähigkeit größtenteils vorhanden", "option_explanation": "Person versteht meistens, benötigt aber manchmal einfachere Erklärungen oder Wiederholungen."},
                {"score": 2, "text": "Fähigkeit in geringem Maße vorhanden", "option_explanation": "Person versteht nur sehr einfache Informationen oder Aufforderungen."},
                {"score": 3, "text": "Fähigkeit nicht vorhanden", "option_explanation": "Person versteht auch einfache Informationen nicht."}
            ]
        },
        '2.8': { # Key is the question ID string '2.8'
            'id': '2.8',
            'text': "Erkennen von Risiken und Gefahren",
            'explanation': "Bewertet wird die Fähigkeit, alltägliche Risiken (z.B. heiße Herdplatte, Stolperfallen) zu erkennen und angemessen zu reagieren.",
            'type': 'radio',
            'answers': [ # Changed 'options' to 'answers'
                {"score": 0, "text": "Fähigkeit vorhanden", "option_explanation": "Person erkennt Risiken und handelt entsprechend."},
                {"score": 1, "text": "Fähigkeit größtenteils vorhanden", "option_explanation": "Person erkennt die meisten Risiken, benötigt aber manchmal Hinweise."},
                {"score": 2, "text": "Fähigkeit in geringem Maße vorhanden", "option_explanation": "Person erkennt nur offensichtliche Risiken oder reagiert unangemessen."},
                {"score": 3, "text": "Fähigkeit nicht vorhanden", "option_explanation": "Person erkennt keine Risiken."}
            ]
        },
        '2.9': { # Key is the question ID string '2.9'
            'id': '2.9',
            'text': "Mitteilen von elementaren Bedürfnissen",
            'explanation': "Bewertet wird die Fähigkeit, grundlegende Bedürfnisse (Hunger, Durst, Schmerz) verbal oder nonverbal mitzuteilen.",
            'type': 'radio',
            'answers': [ # Changed 'options' to 'answers'
                {"score": 0, "text": "Fähigkeit vorhanden", "option_explanation": "Person kann Bedürfnisse klar und zeitgerecht mitteilen."},
                {"score": 1, "text": "Fähigkeit größtenteils vorhanden", "option_explanation": "Person kann Bedürfnisse meist mitteilen, manchmal undeutlich oder verzögert."},
                {"score": 2, "text": "Fähigkeit in geringem Maße vorhanden", "option_explanation": "Person kann Bedürfnisse nur selten oder schwer verständlich mitteilen."},
                {"score": 3, "text": "Fähigkeit nicht vorhanden", "option_explanation": "Person kann Bedürfnisse nicht mitteilen."}
            ]
        },
        '2.10': { # Key is the question ID string '2.10'
             'id': '2.10',
             'text': "Verstehen von Aufforderungen",
             'explanation': "Bewertet wird die Fähigkeit, verbale Aufforderungen zu verstehen und darauf zu reagieren.",
             'type': 'radio',
             'answers': [ # Changed 'options' to 'answers'
                 {"score": 0, "text": "Fähigkeit vorhanden", "option_explanation": "Person versteht auch komplexere Aufforderungen."},
                 {"score": 1, "text": "Fähigkeit größtenteils vorhanden", "option_explanation": "Person versteht meistens, benötigt aber manchmal einfachere Formulierungen oder Gesten."},
                 {"score": 2, "text": "Fähigkeit in geringem Maße vorhanden", "option_explanation": "Person versteht nur sehr einfache, kurze Aufforderungen."},
                 {"score": 3, "text": "Fähigkeit nicht vorhanden", "option_explanation": "Person versteht keine Aufforderungen."}
             ]
         },
         '2.11': { # Key is the question ID string '2.11'
             'id': '2.11',
             'text': "Beteiligen an einem Gespräch",
             'explanation': "Bewertet wird die Fähigkeit, sich an einem Gespräch zu beteiligen, zuzuhören und eigene Beiträge zu machen.",
             'type': 'radio',
             'answers': [ # Changed 'options' to 'answers'
                 {"score": 0, "text": "Fähigkeit vorhanden", "option_explanation": "Person kann sich aktiv und themenbezogen an Gesprächen beteiligen."},
                 {"score": 1, "text": "Fähigkeit größtenteils vorhanden", "option_explanation": "Person beteiligt sich meist, schweift aber manchmal ab oder benötigt Anregung."},
                 {"score": 2, "text": "Fähigkeit in geringem Maße vorhanden", "option_explanation": "Person beteiligt sich nur auf direkte Ansprache oder mit sehr kurzen Beiträgen."},
                 {"score": 3, "text": "Fähigkeit nicht vorhanden", "option_explanation": "Person beteiligt sich nicht an Gesprächen."}
             ]
         }
        # Add more questions here if needed, following the pattern 'X.Y': { ... }
    } # End of questions dictionary
} # End of module2 dictionary