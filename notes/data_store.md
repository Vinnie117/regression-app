# Frage
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
    - höhere Kohäsion
- da rein können auch csv oder Excel files erst mal reingeladen werden

<br>

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

<br>

ABER: Store speichert die Daten im Browser des Users. D.h. Berechnung könnte auch mehrfach durchgeführt werden, wenn Kosten gering sind
- was passiert bei vielen Usern? Compute costs?
- Store ist für gerine Daten Mengen OK -> Datensatz klein halten
    - Stores verlangen JSON und sollten nur wenige MB groß sein
    - https://www.joshzeigler.com/technology/web-development/how-big-is-too-big-for-json
    - https://community.plotly.com/t/storing-large-datasets-in-dcc-store/60986/1


# Fazit
Frage: Store nutzen für Data Prep oder nicht?
<br>
Entscheidung: Mit Store probieren (und Performance auswerten)

- Passiert eine teure Berechnung unnötig oft?
- data prep sollte NICHT nochmal gemacht werden, wenn z.B. target_var oder Plot geändert wird
    

![grafik](https://user-images.githubusercontent.com/52510339/221421081-5d22d171-06f9-47ef-8c19-70972c0adc76.png)



