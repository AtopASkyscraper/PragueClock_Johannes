import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from datetime import datetime, timedelta
import math
import time
from PIL import Image, ImageTk

# Funktion zur Erstellung des Hauptfensters
def erstelle_fenster():
    # Hauptfenster erstellen mit Yaru-Theme
    root = ThemedTk(theme="yaru")  
    root.title("Prager Uhr Simulation")  # Fenstertitel setzen
    root.geometry("1280x720")  # Fenstergröße setzen

    # Frame für die gesamte Anwendung
    haupt_frame = ttk.Frame(root, padding="10")
    haupt_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Ein eingerahmter Bereich für die Bedienelemente links
    elemente_frame = ttk.LabelFrame(haupt_frame, text="Bedienelemente", padding="10")
    elemente_frame.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.W, tk.E))

    # Label-Widget Beispiel
    label = ttk.Label(elemente_frame, text="Willkommen zur Prager Uhr Simulation!")
    label.grid(row=0, column=0, padx=5, pady=5)

    # Combobox (Dropdown-Menü) für Stunden und Minuten erstellen
    auswahl = tk.StringVar()
    optionen = ["Stunden", "Minuten", "MittelEuropaischeZeit","Sonnenverlauf"]#ajouter par Reine

    dropdown = ttk.Combobox(elemente_frame, textvariable=auswahl, values=optionen)
    dropdown.grid(row=1, column=0, padx=5, pady=5)
    dropdown.set("Wähle aus")

    # Label für die Ausgabe der Uhrzeit hinzufügen
    zeit_label = ttk.Label(elemente_frame, text="")
    zeit_label.grid(row=3, column=0, padx=5, pady=5)

    # Variablen zum Hervorheben der Zeiger
    highlight_stundenzeiger = tk.BooleanVar(value=False)
    highlight_minutenzeiger = tk.BooleanVar(value=False)
    highlight_mezzeiger = tk.BooleanVar(value=False)
    highlight_Sonnezeiger= tk.BooleanVar(value=False)  #Von Reine hinzugefügt

    # Funktion zur Anzeige der Auswahl
    def auswahl_anzeigen():

        #  Alle Zeiger zurücksetzen
        highlight_stundenzeiger.set(False)
        highlight_minutenzeiger.set(False)
        highlight_mezzeiger.set(False)
        highlight_Sonnezeiger.set(False)  #Von Reine hinzugefügt

        if auswahl.get() == "Stunden":
            stunde = simulierte_zeit.hour
            zeit_label.config(text=f"Aktuelle Stunde: {stunde}")
            highlight_stundenzeiger.set(True)
        elif auswahl.get() == "Minuten":
            minute = simulierte_zeit.minute
            zeit_label.config(text=f"Aktuelle Minute: {minute}")
            highlight_minutenzeiger.set(True)
        elif auswahl.get() == "MittelEuropaischeZeit":
            mitteleuropaeische_zeit = simulierte_zeit.strftime('"%H:%M:%S MEZ"')
            zeit_label.config(text=f"MittelEuropäische Zeit: {mitteleuropaeische_zeit}")
            highlight_mezzeiger.set(True)
        elif auswahl.get() == "Sonnenverlauf":   #Von Reine hinzugefügt
            Sonne_verlauf = simulierte_zeit.strftime("%A, %d %B %Y")
            zeit_label.config(text=f"Aktuelle Sonne position: {Sonne_verlauf}")
            highlight_Sonnezeiger.set(True)    
        else:
            zeit_label.config(text="Bitte eine Option auswählen")
            highlight_stundenzeiger.set(False)
            highlight_minutenzeiger.set(False)
            highlight_mezzeiger.set(False)
            highlight_Sonnezeiger.set(False)   #Von Reine hinzugefügt

    # Button hinzufügen, um die Auswahl zu bestätigen
    bestätigungs_button = ttk.Button(elemente_frame, text="Bestätigen", command=auswahl_anzeigen)
    bestätigungs_button.grid(row=2, column=0, padx=5, pady=5)

    # Button-Widget Beispiel
    button = ttk.Button(elemente_frame, text="Klick mich!", command=lambda: print("Button wurde geklickt!"))
    button.grid(row=4, column=0, padx=5, pady=5)

    # Ein eingerahmter Bereich für die Uhrzeitanzeige und Geschwindigkeitseinstellungen
    uhr_frame = ttk.LabelFrame(haupt_frame, text="Uhrzeitanzeige", padding="10")
    uhr_frame.grid(row=0, column=1, padx=10, pady=10, sticky=(tk.NE))

    # Label für die aktuelle Uhrzeit rechts im Fenster erstellen
    uhrzeit_label = ttk.Label(uhr_frame, font=("Helvetica", 16))
    uhrzeit_label.grid(row=0, column=0, padx=10, pady=10)

    # Canvas für das analoge Zifferblatt (Auflösung 600x600)
    canvas = tk.Canvas(uhr_frame, width=600, height=600, bg="white")
    canvas.grid(row=1, column=0, padx=10, pady=10)

    # Hintergrundbild laden und auf Canvas anwenden
    hintergrund_image = Image.open("Uhr_Backround_zugeschnitten.jpg")
    hintergrund_image = hintergrund_image.resize((600, 600), Image.LANCZOS)  # Größe des Bildes anpassen
    hintergrund_tk = ImageTk.PhotoImage(hintergrund_image)
    canvas.create_image(0, 0, image=hintergrund_tk, anchor=tk.NW)

    # Variable zur Simulation der Zeit
    simulierte_zeit = datetime.now()

    # Slidebar für Geschwindigkeitsanpassung erstellen
    geschwindigkeits_label = ttk.Label(elemente_frame, text="Zeitraffer (-10x bis 10x)")
    geschwindigkeits_label.grid(row=5, column=0, padx=5, pady=(10, 0))

    # Slider erstellen (nicht als Yaru-Theme)
    geschwindigkeits_slider = tk.Scale(elemente_frame, from_=-10, to=10, orient=tk.HORIZONTAL, length=200)
    geschwindigkeits_slider.grid(row=6, column=0, padx=5, pady=10)
    geschwindigkeits_slider.set(1)  # Standardmäßig auf 1x setzen

    # Funktion zur Aktualisierung der Uhrzeit
    def uhrzeit_aktualisieren():
        nonlocal simulierte_zeit
        geschwindigkeit = geschwindigkeits_slider.get()  # Geschwindigkeit aus dem Slider
        simulierte_zeit += timedelta(seconds=1 * geschwindigkeit)  # Zeit beschleunigen
        uhrzeit_label.config(text=f"Aktuelle Uhrzeit: {simulierte_zeit.strftime('%H:%M:%S')}")
        zeichne_zifferblatt()  # Zifferblatt aktualisieren
        root.after(1000, uhrzeit_aktualisieren)

    # Funktion zum Zeichnen des Zifferblatts
    def zeichne_zifferblatt():
        canvas.delete("all")

        # Hintergrundbild auf Canvas zeichnen
        canvas.create_image(0, 0, image=hintergrund_tk, anchor=tk.NW)

        # Zifferblatt zeichnen
        canvas.create_oval(50, 50, 550, 550, outline="black", width=2)

        # Stundenmarkierungen
        for i in range(12):
            winkel = math.radians(i * 30)
            x1 = 300 + 240 * math.sin(winkel)
            y1 = 300 - 240 * math.cos(winkel)
            x2 = 300 + 280 * math.sin(winkel)
            y2 = 300 - 280 * math.cos(winkel)
            canvas.create_line(x1, y1, x2, y2, width=2)

        # Stundenzeiger
        stunden_winkel = math.radians((simulierte_zeit.hour % 12 + simulierte_zeit.minute / 60) * 30)
        stunden_x = 300 + 140 * math.sin(stunden_winkel)
        stunden_y = 300 - 140 * math.cos(stunden_winkel)
        if highlight_stundenzeiger.get():
            canvas.create_line(300, 300, stunden_x, stunden_y, width=6, fill="red")  # Hervorhebung des Stundenzeigers
        else:
            canvas.create_line(300, 300, stunden_x, stunden_y, width=4, fill="white")

        # Minutenzeiger
        minuten_winkel = math.radians(simulierte_zeit.minute * 6)
        minuten_x = 300 + 200 * math.sin(minuten_winkel)
        minuten_y = 300 - 200 * math.cos(minuten_winkel)
        if highlight_minutenzeiger.get():
            canvas.create_line(300, 300, minuten_x, minuten_y, width=4, fill="blue")  # Hervorhebung des Minutenzeigers
        else:
            canvas.create_line(300, 300, minuten_x, minuten_y, width=2, fill="white")

    # Hier beginnt Daniels Teil

        # Aktuelle Uhrzeit
        stunden = time.localtime().tm_hour % 12
        minuten = time.localtime().tm_min
        
        # Winkel der Zeiger (360 Grad = 24 Stunden oder 60 Minuten/Sekunden)
        angle_stunden = (stunden + minuten/60 ) * 15  # Winkel zwischen 2 aufeinanderfolgenden Stunden = 15 Grad
        winkel_radians = math.radians(angle_stunden)

        # Den Stundenzeiger für die Mitteleuropaische Zeit zeichnen
        x, y = ZeigerRechnen(250, angle_stunden)  #Koordinaten für die Spitze des Dreiecks
        if highlight_mezzeiger.get():
            canvas.create_line(300, 300, x, y, width=7, fill='green', tags="Nadel")
        else:
            canvas.create_line(300, 300, x, y, width=5, fill="white")
        
        # Liste mit den Punkten, um den Dreieck zu zeichnen (handgeformtes Polygon)
        x_h, y_h = ZeigerRechnen(200, angle_stunden)
        gold_hand = [
            x, y,
            x_h - 20*math.cos(winkel_radians), y_h - 20*math.sin(winkel_radians),
            x_h + 20*math.cos(winkel_radians), y_h + 20*math.sin(winkel_radians),
        ]

        #Dreieck zeichnen
        canvas.create_polygon(gold_hand, fill="#FFD700", width=3, outline="black", tags="Nadel")
    
    # Funktion zum Berechnen der Position der Spitze der Nadel
    def ZeigerRechnen(laenge, winkel):
        winkel_radians = math.radians(winkel)
        x = 300 + laenge * math.sin(winkel_radians)
        y = 300 - laenge * math.cos(winkel_radians)
        return x, y

    # Hier endet Daniels Teil


    #Anfang Teil Reine
    
    # Sonnenbild laden
    sonnen_image = Image.open("Sonne.png").resize((50, 50), Image.LANCZOS)
    sonnen_image_tk = ImageTk.PhotoImage(sonnen_image)
    # Speichere die Bildreferenz, damit sie nicht gelöscht wird
    canvas.sonnen_image_tk = sonnen_image_tk
    #z = datetime.now()
    # Beispiel-Positionen für die Sonne (x, y)
    positionen = [96.15, 96.15, 96.15, 107.5, 155,202.3, 249.6, 155, 107, 96, 95, 50]#a changer

    # Funktion zur Simulation der Bewegung
    # Aktuelle Uhrzeit
    stunden = time.localtime().tm_hour % 12
    minuten = time.localtime().tm_min

    # Winkel der Zeiger (360 Grad = 24 Stunden oder 60 Minuten/Sekunden)
    angle_stunden = (stunden + minuten/60 ) * 15  # Winkel zwischen 2 aufeinanderfolgenden Stunden = 15 Grad
    winkel_radians = math.radians(angle_stunden)
    def bewege_sonne(canvas, sonnen_image, positionen):
        # Startindex für das Array
        index = 0

        def aktualisiere_position():
            nonlocal index
            canvas.delete("sonne")  # Alte Position löschen

            # Position aus dem Array nehmen
            x_image, y_image = ZeigerRechnen(positionen[index],angle_stunden )
            canvas.create_image(x_image, y_image, image=sonnen_image_tk, anchor=tk.CENTER)
            
            # Nächste Position im Array
            index = (index + 1) % len(positionen)  # Zyklische Bewegung
            
            # Nächste Aktualisierung nach 500ms
            canvas.after(800, aktualisiere_position)
    
        # Schleife starten
        aktualisiere_position()
           # Funktion zum Berechnen der Position der Spitze der Nadel
    def ZeigerRechnen(laenge, winkel):
        winkel_radians = math.radians(winkel)
        x = 300 + laenge * math.sin(winkel_radians)
        y = 300 - laenge * math.cos(winkel_radians)
        return x, y

    if highlight_Sonnezeiger.get():
        x, y = ZeigerRechnen(250, angle_stunden)  #Koordinaten für die Spitze des Dreiecks
        canvas.create_line(300, 300, x, y, width=7, fill='black', tags="Nadel")
    else:
        bewege_sonne(canvas, sonnen_image_tk, positionen)
    
    # # Aktuelle Uhrzeit
    # stunden = time.localtime().tm_hour % 12
    # minuten = time.localtime().tm_min
    
    # # Winkel der Zeiger (360 Grad = 24 Stunden oder 60 Minuten/Sekunden)
    # angle_stunden = (stunden + minuten/60 ) * 15  # Winkel zwischen 2 aufeinanderfolgenden Stunden = 15 Grad
    # winkel_radians = math.radians(angle_stunden)

    # positions = []
    # for i in range(10):
    #     longueur = 250 * (i + 1) / 10  # Diviser la longueur en 10 segments
    #     x, y = ZeigerRechnen(longueur, angle_stunden)
    #     positions.append((x, y))
    # # Ajouter des conditions pour les positions
    # current_position = (simulierte_zeit.second % 10)  # Change de position toutes les secondes
    # zeiger_x, zeiger_y = positions[current_position]

    # # Ajouter l'image sur la position actuelle
    # canvas.create_image(zeiger_x, zeiger_y, image=sonnen_image_tk, anchor=tk.CENTER)

# def uhrzeit_aktualisieren():
#     nonlocal simulierte_zeit
#     simulierte_zeit += timedelta(seconds=1)
#     zeichne_zifferblatt()
#     root.after(1000, uhrzeit_aktualisieren)

    #uhrzeit_aktualisieren()
#Ende Teil Reine

    # Uhrzeit-Aktualisierung starten
    uhrzeit_aktualisieren()

    return root

# Hauptfunktion, die das Fenster erstellt und die Tkinter-Schleife startet
def main():
    root = erstelle_fenster()
    root.mainloop()

# Entry-Point der Anwendung
if __name__ == "__main__":
    main()
