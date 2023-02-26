Den Table auch in einem Store speichern?
    - ist wsl auch besser perspektivisch für den Datenupload
    - dort das ganze Preprocessing machen und das saubere Ergebnis weitergeben
        - model_results.py für OLS
        - plot.py für den Graph
        - validation.py für die Warnmeldungen
        - variable_selection.py für die Auswahl der Zielvariablen
    - das Preprocessing muss aus den anderen Components dann rausgenommen werden.
        - ist auch besser für die Übersichtlichkeit
        - liefert Performance, weil Preprocessing nur einmal gemacht werden muss
        - losere Kopplung
    - da rein können auch csv oder Excel files erst mal reingeladen werden


Warum nicht nur im table.py callback die dataprep machen und ann alle anderen callbacks weitergeben?
    - Store stellt sicher, dass die Daten wirklich im Browser des User gespeichert sind
        - wo werden sie sonst gespeichert?
    - hier kann noch mehr data_prep unter der Haube passieren, was für den View ungeeignet ist
        - drop_minority_type -> rows
        - drop NaNs -> rows
        - ...
    - Store auch besser, weil sonst immer wenn View sich ändert ALLE data prep Sachen gemacht werden
        - Bzw. immer wenn Plot oder Berechnung getriggert wird -> passiert was genau?
            -> nochmal genau überlegen

    - computation for data cleaning has to be calculated two times
        - Dashboard hat viele andere Elemente


# Fazit
Frage: Store nutzen für Data Prep oder nicht?
<br>
Entscheidung: Mit Store probieren (und Performance auswerten)

- Passiert eine teure Berechnung unnötig oft?
- data prep sollte NICHT nochmal gemacht werden, wenn z.B. target_var oder Plot geändert wird
    


