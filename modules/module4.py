"""
Module 4: Selbstversorgung
Weight: 40% (0.4)
"""

module4 = {
    "name": "Modul 4: Selbstversorgung",
    "weight": 0.4,
    "questions": [
        # --- Bereich: Körperpflege ---
        {
            "question": "4.1 Waschen des vorderen Oberkörpers",
            "explanation": "Bewertet wird die Fähigkeit, Gesicht, Hals, Arme, Hände und vorderen Brust-/Bauchbereich zu waschen.",
            "options": [
                {"score": 0, "text": "Selbstständig", "option_explanation": "Person kann den Bereich ohne personelle Hilfe waschen."},
                {"score": 1, "text": "Überwiegend selbstständig", "option_explanation": "Person benötigt nur geringe Hilfe (z.B. Wasser bereitstellen, Anleitung, Waschen schwer erreichbarer Stellen)."},
                {"score": 2, "text": "Überwiegend unselbstständig", "option_explanation": "Person benötigt umfangreiche Hilfe (z.B. Waschen großer Teile des Bereichs)."},
                {"score": 3, "text": "Unselbstständig", "option_explanation": "Person muss vollständig von anderen gewaschen werden."}
            ]
        },
        {
            "question": "4.2 Körperpflege im Bereich des Kopfes",
            "explanation": "Bewertet wird die Fähigkeit zum Kämmen, zur Zahnpflege/Prothesenreinigung und zum Rasieren.",
            "options": [
                {"score": 0, "text": "Selbstständig", "option_explanation": "Person kann alle genannten Tätigkeiten ohne personelle Hilfe durchführen."},
                {"score": 1, "text": "Überwiegend selbstständig", "option_explanation": "Person benötigt nur geringe Hilfe (z.B. Zahnpasta auftragen, Utensilien anreichen, Teilbereiche übernehmen)."},
                {"score": 2, "text": "Überwiegend unselbstständig", "option_explanation": "Person benötigt umfangreiche Hilfe (z.B. Übernahme der meisten Tätigkeiten)."},
                {"score": 3, "text": "Unselbstständig", "option_explanation": "Alle Tätigkeiten müssen vollständig von anderen übernommen werden."}
            ]
        },
        {
            "question": "4.3 Waschen des Intimbereichs",
            "explanation": "Bewertet wird die Fähigkeit, den Intimbereich (vorne und hinten) zu waschen und abzutrocknen.",
            "options": [
                {"score": 0, "text": "Selbstständig", "option_explanation": "Person kann den Intimbereich ohne personelle Hilfe waschen und abtrocknen."},
                {"score": 1, "text": "Überwiegend selbstständig", "option_explanation": "Person benötigt nur geringe Hilfe (z.B. Anleitung, Waschlappen anreichen, Teilbereiche übernehmen)."},
                {"score": 2, "text": "Überwiegend unselbstständig", "option_explanation": "Person benötigt umfangreiche Hilfe (z.B. Waschen großer Teile des Bereichs)."},
                {"score": 3, "text": "Unselbstständig", "option_explanation": "Person muss im Intimbereich vollständig von anderen gewaschen werden."}
            ]
        },
        {
            "question": "4.4 Duschen und Baden einschließlich Waschen der Haare",
            "explanation": "Bewertet wird die Fähigkeit, den gesamten Körper (einschließlich Rücken und Füße) und die Haare zu waschen, entweder in der Dusche oder Badewanne.",
            "options": [
                {"score": 0, "text": "Selbstständig", "option_explanation": "Person kann ohne personelle Hilfe duschen/baden und Haare waschen."},
                {"score": 1, "text": "Überwiegend selbstständig", "option_explanation": "Person benötigt nur geringe Hilfe (z.B. Ein-/Ausstiegshilfe, Rücken waschen, Anleitung)."},
                {"score": 2, "text": "Überwiegend unselbstständig", "option_explanation": "Person benötigt umfangreiche Hilfe (z.B. Waschen großer Körperbereiche, ständige Aufsicht/Unterstützung)."},
                {"score": 3, "text": "Unselbstständig", "option_explanation": "Person muss vollständig geduscht/gebadet werden oder Ganzkörperwäsche am Waschbecken/im Bett ist nötig."}
            ]
        },
        # --- Bereich: Kleiden ---
        {
            "question": "4.5 An- und Auskleiden des Oberkörpers",
            "explanation": "Bewertet wird die Fähigkeit, Kleidung für den Oberkörper (Hemd, Pullover, BH etc.) an- und auszuziehen.",
            "options": [
                {"score": 0, "text": "Selbstständig", "option_explanation": "Person kann sich ohne personelle Hilfe am Oberkörper an- und auskleiden."},
                {"score": 1, "text": "Überwiegend selbstständig", "option_explanation": "Person benötigt nur geringe Hilfe (z.B. Kleidung zurechtlegen, Knöpfe/Reißverschluss schließen, über Kopf helfen)."},
                {"score": 2, "text": "Überwiegend unselbstständig", "option_explanation": "Person benötigt umfangreiche Hilfe (z.B. An-/Ausziehen großer Kleidungsstücke)."},
                {"score": 3, "text": "Unselbstständig", "option_explanation": "Person muss am Oberkörper vollständig an- und ausgekleidet werden."}
            ]
        },
        {
            "question": "4.6 An- und Auskleiden des Unterkörpers",
            "explanation": "Bewertet wird die Fähigkeit, Kleidung für den Unterkörper (Hose, Rock, Strümpfe, Schuhe) an- und auszuziehen.",
            "options": [
                {"score": 0, "text": "Selbstständig", "option_explanation": "Person kann sich ohne personelle Hilfe am Unterkörper an- und auskleiden."},
                {"score": 1, "text": "Überwiegend selbstständig", "option_explanation": "Person benötigt nur geringe Hilfe (z.B. Strümpfe anziehen, Schuhe binden, Reißverschluss schließen)."},
                {"score": 2, "text": "Überwiegend unselbstständig", "option_explanation": "Person benötigt umfangreiche Hilfe (z.B. Hose hochziehen, An-/Ausziehen im Liegen)."},
                {"score": 3, "text": "Unselbstständig", "option_explanation": "Person muss am Unterkörper vollständig an- und ausgekleidet werden."}
            ]
        },
        # --- Bereich: Essen und Trinken ---
        {
            "question": "4.7 Essen",
            "explanation": "Bewertet wird die Fähigkeit, mundgerecht zubereitete Nahrung aufzunehmen, Besteck zu verwenden und zum Mund zu führen.",
            "options": [
                {"score": 0, "text": "Selbstständig", "option_explanation": "Person kann ohne personelle Hilfe essen."},
                {"score": 1, "text": "Überwiegend selbstständig", "option_explanation": "Person benötigt nur geringe Hilfe (z.B. Nahrung klein schneiden, Becher halten, motivieren)."},
                {"score": 2, "text": "Überwiegend unselbstständig", "option_explanation": "Person benötigt umfangreiche Hilfe (z.B. Nahrung anreichen, füttern)."},
                {"score": 3, "text": "Unselbstständig", "option_explanation": "Person muss vollständig gefüttert werden (auch bei Sondenernährung relevant)."}
            ]
        },
        {
            "question": "4.8 Trinken",
            "explanation": "Bewertet wird die Fähigkeit, Getränke selbstständig aufzunehmen und aus einem Glas/Becher/Tasse zu trinken.",
            "options": [
                {"score": 0, "text": "Selbstständig", "option_explanation": "Person kann ohne personelle Hilfe trinken."},
                {"score": 1, "text": "Überwiegend selbstständig", "option_explanation": "Person benötigt nur geringe Hilfe (z.B. Getränk einschenken, Gefäß halten/anreichen)."},
                {"score": 2, "text": "Überwiegend unselbstständig", "option_explanation": "Person benötigt umfangreiche Hilfe (z.B. Getränk anreichen, beim Trinken helfen)."},
                {"score": 3, "text": "Unselbstständig", "option_explanation": "Person muss Getränke vollständig eingegeben bekommen."}
            ]
        },
        # --- Bereich: Ausscheidungen ---
        {
            "question": "4.9 Benutzen einer Toilette oder eines Toilettenstuhls",
            "explanation": "Bewertet wird die Fähigkeit, zur Toilette zu gehen/fahren, sich hinzusetzen/aufzustehen, sich nach dem Toilettengang zu reinigen und Kleidung zu richten.",
            "options": [
                {"score": 0, "text": "Selbstständig", "option_explanation": "Person kann die Toilette/den Toilettenstuhl ohne personelle Hilfe benutzen."},
                {"score": 1, "text": "Überwiegend selbstständig", "option_explanation": "Person benötigt nur geringe Hilfe (z.B. Hilfe beim Transfer, Kleidung richten, Intimhygiene teilweise)."},
                {"score": 2, "text": "Überwiegend unselbstständig", "option_explanation": "Person benötigt umfangreiche Hilfe (z.B. Transfer, Intimhygiene größtenteils)."},
                {"score": 3, "text": "Unselbstständig", "option_explanation": "Person ist vollständig auf Hilfe angewiesen oder benötigt Versorgung mit Urinflasche/Bettpfanne."}
            ]
        },
        {
            "question": "4.10 Bewältigung der Folgen einer Harninkontinenz und Umgang mit Dauerkatheter/Urostoma",
            "explanation": "Bewertet wird die Fähigkeit, mit Inkontinenzmaterial (Vorlagen, Windeln) umzugehen oder einen Katheter/Stoma selbstständig zu versorgen.",
            "options": [
                {"score": 0, "text": "Selbstständig/Kontinent", "option_explanation": "Person ist kontinent oder kann Inkontinenz-/Stomaversorgung ohne personelle Hilfe durchführen."},
                {"score": 1, "text": "Überwiegend selbstständig", "option_explanation": "Person benötigt nur geringe Hilfe (z.B. Material anreichen, Kontrolle, kleine Hilfestellungen)."},
                {"score": 2, "text": "Überwiegend unselbstständig", "option_explanation": "Person benötigt umfangreiche Hilfe (z.B. Wechseln des Materials, Versorgung des Systems)."},
                {"score": 3, "text": "Unselbstständig", "option_explanation": "Inkontinenz-/Stomaversorgung muss vollständig von anderen übernommen werden."}
            ]
        },
        {
            "question": "4.11 Bewältigung der Folgen einer Stuhlinkontinenz und Umgang mit Stoma",
            "explanation": "Bewertet wird die Fähigkeit, mit Inkontinenzmaterial umzugehen oder ein Stoma selbstständig zu versorgen.",
            "options": [
                {"score": 0, "text": "Selbstständig/Kontinent", "option_explanation": "Person ist kontinent oder kann Inkontinenz-/Stomaversorgung ohne personelle Hilfe durchführen."},
                {"score": 1, "text": "Überwiegend selbstständig", "option_explanation": "Person benötigt nur geringe Hilfe (z.B. Material anreichen, Kontrolle, kleine Hilfestellungen)."},
                {"score": 2, "text": "Überwiegend unselbstständig", "option_explanation": "Person benötigt umfangreiche Hilfe (z.B. Wechseln des Materials, Versorgung des Systems)."},
                {"score": 3, "text": "Unselbstständig", "option_explanation": "Inkontinenz-/Stomaversorgung muss vollständig von anderen übernommen werden."}
            ]
        }
    ]
}