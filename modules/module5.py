"""
Module 5: Bewältigung von und selbstständiger Umgang mit krankheits- oder
          therapiebedingten Anforderungen und Belastungen
Weight: 20% (0.2)
"""

module5 = {
    "name": "Modul 5: Bewältigung von krankheits- oder therapiebedingten Anforderungen",
    "weight": 0.2,
    "questions": [
        # --- Bereich: Medikation ---
        {
            "question": "5.1 Umgang mit Medikamenten",
            "explanation": "Bewertet wird die Fähigkeit, ärztlich verordnete Medikamente selbstständig und zuverlässig einzunehmen (Stellen, Dosieren, Anwenden).",
            "options": [
                {"score": 0, "text": "Selbstständig", "option_explanation": "Person kann Medikamente ohne personelle Hilfe oder nur mit Erinnerung einnehmen."},
                {"score": 1, "text": "Überwiegend selbstständig/Hilfe beim Richten/Aufsicht", "option_explanation": "Medikamente müssen gerichtet oder die Einnahme beaufsichtigt werden."},
                {"score": 2, "text": "Überwiegend unselbstständig/Hilfe bei Einnahme", "option_explanation": "Medikamente müssen (teilweise) verabreicht werden."},
                {"score": 3, "text": "Unselbstständig", "option_explanation": "Medikamente müssen vollständig von anderen verabreicht werden."}
                # Scoring often relates to *who* performs the action (person, lay helper, professional)
            ]
        },
        # --- Bereich: Injektionen, Blutzuckermessung ---
        {
            "question": "5.2 Blutzuckermessung und Insulingabe",
            "explanation": "Bewertet wird die Fähigkeit zur selbstständigen Blutzuckermessung und/oder subkutanen Insulininjektion.",
            "options": [
                {"score": 0, "text": "Selbstständig/Nicht relevant", "option_explanation": "Person kann dies selbstständig durchführen oder benötigt es nicht."},
                {"score": 1, "text": "Überwiegend selbstständig/Anleitung/Aufsicht", "option_explanation": "Person benötigt Anleitung, Aufsicht oder geringe Hilfe."},
                {"score": 2, "text": "Überwiegend unselbstständig/Teilweise Übernahme", "option_explanation": "Messung/Injektion muss teilweise übernommen werden."},
                {"score": 3, "text": "Unselbstständig", "option_explanation": "Messung/Injektion muss vollständig von anderen durchgeführt werden."}
            ]
        },
        # --- Bereich: Verbandwechsel, Wundversorgung ---
        {
            "question": "5.3 Versorgung von Wunden oder Drainagen",
            "explanation": "Bewertet wird die Fähigkeit zur selbstständigen Versorgung von Wunden (z.B. Verbandwechsel) oder Drainagen.",
            "options": [
                {"score": 0, "text": "Selbstständig/Nicht relevant", "option_explanation": "Person kann dies selbstständig durchführen oder benötigt es nicht."},
                {"score": 1, "text": "Überwiegend selbstständig/Anleitung/Aufsicht", "option_explanation": "Person benötigt Anleitung, Aufsicht oder geringe Hilfe."},
                {"score": 2, "text": "Überwiegend unselbstständig/Teilweise Übernahme", "option_explanation": "Versorgung muss teilweise übernommen werden."},
                {"score": 3, "text": "Unselbstständig", "option_explanation": "Versorgung muss vollständig von anderen durchgeführt werden."}
            ]
        },
         {
            "question": "5.4 Versorgung von Stomata (Tracheostoma, Uro-/Enterostoma)",
            "explanation": "Bewertet wird die Fähigkeit zur selbstständigen Versorgung künstlicher Körperöffnungen (Reinigung, Materialwechsel).",
            "options": [
                {"score": 0, "text": "Selbstständig/Nicht relevant", "option_explanation": "Person kann dies selbstständig durchführen oder benötigt es nicht."},
                {"score": 1, "text": "Überwiegend selbstständig/Anleitung/Aufsicht", "option_explanation": "Person benötigt Anleitung, Aufsicht oder geringe Hilfe."},
                {"score": 2, "text": "Überwiegend unselbstständig/Teilweise Übernahme", "option_explanation": "Versorgung muss teilweise übernommen werden."},
                {"score": 3, "text": "Unselbstständig", "option_explanation": "Versorgung muss vollständig von anderen durchgeführt werden."}
            ]
        },
        # --- Bereich: Therapiemaßnahmen ---
        {
            "question": "5.5 Regelmäßige Einreibungen oder Kälte-/Wärmeanwendungen",
            "explanation": "Bewertet wird die Fähigkeit zur selbstständigen Durchführung ärztlich verordneter Einreibungen oder Kälte-/Wärmeanwendungen.",
            "options": [
                {"score": 0, "text": "Selbstständig/Nicht relevant", "option_explanation": "Person kann dies selbstständig durchführen oder benötigt es nicht."},
                {"score": 1, "text": "Überwiegend selbstständig/Anleitung/Aufsicht", "option_explanation": "Person benötigt Anleitung, Aufsicht oder geringe Hilfe."},
                {"score": 2, "text": "Überwiegend unselbstständig/Teilweise Übernahme", "option_explanation": "Anwendung muss teilweise übernommen werden."},
                {"score": 3, "text": "Unselbstständig", "option_explanation": "Anwendung muss vollständig von anderen durchgeführt werden."}
            ]
        },
        {
            "question": "5.6 Messung von Körperzuständen (z.B. Blutdruck, Puls)",
            "explanation": "Bewertet wird die Fähigkeit zur selbstständigen Messung und Dokumentation von Vitalzeichen oder anderen Körperzuständen.",
            "options": [
                {"score": 0, "text": "Selbstständig/Nicht relevant", "option_explanation": "Person kann dies selbstständig durchführen oder benötigt es nicht."},
                {"score": 1, "text": "Überwiegend selbstständig/Anleitung/Aufsicht", "option_explanation": "Person benötigt Anleitung, Aufsicht oder geringe Hilfe."},
                {"score": 2, "text": "Überwiegend unselbstständig/Teilweise Übernahme", "option_explanation": "Messung/Dokumentation muss teilweise übernommen werden."},
                {"score": 3, "text": "Unselbstständig", "option_explanation": "Messung/Dokumentation muss vollständig von anderen durchgeführt werden."}
            ]
        },
        {
            "question": "5.7 Körperbezogene Therapien (z.B. Inhalation, Absaugen)",
            "explanation": "Bewertet wird die Fähigkeit zur selbstständigen Durchführung spezifischer körperbezogener Therapien.",
            "options": [
                {"score": 0, "text": "Selbstständig/Nicht relevant", "option_explanation": "Person kann dies selbstständig durchführen oder benötigt es nicht."},
                {"score": 1, "text": "Überwiegend selbstständig/Anleitung/Aufsicht", "option_explanation": "Person benötigt Anleitung, Aufsicht oder geringe Hilfe."},
                {"score": 2, "text": "Überwiegend unselbstständig/Teilweise Übernahme", "option_explanation": "Therapie muss teilweise übernommen werden."},
                {"score": 3, "text": "Unselbstständig", "option_explanation": "Therapie muss vollständig von anderen durchgeführt werden."}
            ]
        },
        # --- Bereich: Arztbesuche, Organisation ---
        {
            "question": "5.8 Zeit- und technikintensive Maßnahmen im häuslichen Bereich",
            "explanation": "Bewertet wird der Aufwand für spezielle Maßnahmen wie z.B. Beatmung, Dialyse im häuslichen Umfeld.",
            "options": [
                {"score": 0, "text": "Nicht relevant/Kein oder geringer Aufwand", "option_explanation": "Keine solchen Maßnahmen oder nur geringer, seltener Aufwand."},
                # Scoring here often depends on frequency/duration (e.g., täglich <1h, 1-3h, >3h)
                # Simplified for now:
                {"score": 1, "text": "Mäßiger Aufwand", "option_explanation": "Regelmäßiger, aber zeitlich begrenzter Aufwand."},
                {"score": 2, "text": "Hoher Aufwand", "option_explanation": "Täglicher, zeitintensiver Aufwand."},
                {"score": 3, "text": "Sehr hoher Aufwand", "option_explanation": "Sehr zeitintensive oder komplexe Maßnahmen."}
            ]
        },
        {
            "question": "5.9 Arztbesuche",
            "explanation": "Bewertet wird die Häufigkeit von Arztbesuchen (außer Haus) aufgrund der Erkrankung/Behinderung.",
            "options": [
                # Scoring based on frequency
                {"score": 0, "text": "Nicht relevant/Keine oder seltene Besuche", "option_explanation": "Keine oder weniger als 1x pro Monat."},
                {"score": 1, "text": "Regelmäßig (1-3 Mal pro Monat)", "option_explanation": "Durchschnittlich 1-3 Arztbesuche pro Monat."},
                {"score": 2, "text": "Häufig (wöchentlich)", "option_explanation": "Durchschnittlich wöchentliche Arztbesuche."},
                {"score": 3, "text": "Sehr häufig (mehrmals wöchentlich)", "option_explanation": "Mehrere Arztbesuche pro Woche erforderlich."}
            ]
        },
        {
            "question": "5.10 Besuch anderer medizinischer oder therapeutischer Einrichtungen",
            "explanation": "Bewertet wird die Häufigkeit von Besuchen bei Therapeuten (Physio-, Ergo-, Logo-), Dialyse, etc. (außer Haus).",
            "options": [
                {"score": 0, "text": "Nicht relevant/Keine oder seltene Besuche", "option_explanation": "Keine oder weniger als 1x pro Monat."},
                {"score": 1, "text": "Regelmäßig (1-3 Mal pro Monat)", "option_explanation": "Durchschnittlich 1-3 Besuche pro Monat."},
                {"score": 2, "text": "Häufig (wöchentlich)", "option_explanation": "Durchschnittlich wöchentliche Besuche."},
                {"score": 3, "text": "Sehr häufig (mehrmals wöchentlich)", "option_explanation": "Mehrere Besuche pro Woche erforderlich."}
            ]
        },
        {
            "question": "5.11 Zeitlicher Aufwand von Laien für Organisation/Planung",
            "explanation": "Bewertet wird der Aufwand für Laien (Angehörige) zur Organisation von Hilfen, Terminen, Rezepten etc.",
            "options": [
                {"score": 0, "text": "Kein oder geringer Aufwand", "option_explanation": "Kein oder nur minimaler organisatorischer Aufwand."},
                {"score": 1, "text": "Mäßiger Aufwand", "option_explanation": "Regelmäßiger, aber überschaubarer Aufwand."},
                {"score": 2, "text": "Hoher Aufwand", "option_explanation": "Deutlicher, zeitintensiver organisatorischer Aufwand."},
                {"score": 3, "text": "Sehr hoher Aufwand", "option_explanation": "Sehr umfangreicher, komplexer organisatorischer Aufwand."}
            ]
        },
         {
            "question": "5.12 Einhaltung einer Diät oder anderer krankheits- oder therapiebedingter Verhaltensvorschriften",
            "explanation": "Bewertet wird die Fähigkeit, eine verordnete Diät oder spezifische Verhaltensregeln (z.B. Trinkmengenbeschränkung) selbstständig einzuhalten.",
            "options": [
                {"score": 0, "text": "Selbstständig/Nicht relevant", "option_explanation": "Person kann dies selbstständig einhalten oder benötigt es nicht."},
                {"score": 1, "text": "Überwiegend selbstständig/Anleitung/Aufsicht", "option_explanation": "Person benötigt Anleitung, Aufsicht oder Erinnerung."},
                {"score": 2, "text": "Überwiegend unselbstständig/Kontrolle/Hilfe", "option_explanation": "Einhaltung muss kontrolliert oder teilweise unterstützt werden (z.B. Diätkost zubereiten)."},
                {"score": 3, "text": "Unselbstständig", "option_explanation": "Einhaltung muss vollständig von anderen sichergestellt werden."}
            ]
        }
    ]
}