import serial
import time
import threading
from pynput.keyboard import Controller
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser

# Variables globales
ser = None
keyboard = Controller()
running = False

# Fonction pour démarrer la lecture série
def start_reading(port, baudrate):
    global ser, running
    if running:
        update_status("La lecture est déjà en cours.")
        return
    try:
        ser = serial.Serial(port, baudrate)
        running = True
        update_status(f"Connecté à {port} avec {baudrate} bauds.")
        threading.Thread(target=read_serial, daemon=True).start()
    except serial.SerialException as e:
        messagebox.showerror("Erreur", f"Impossible d'ouvrir le port {port} avec {baudrate} bauds: {e}")

# Fonction pour arrêter la lecture série
def stop_reading():
    global ser, running
    if not running:
        update_status("Aucune lecture en cours.")
        return
    running = False
    if ser:
        ser.close()
        ser = None
    update_status("Lecture arrêtée.")

# Fonction pour lire les données série
def read_serial():
    global running
    while running:
        try:
            if ser and ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                if line:
                    update_data_display(line)
                    valeurs = line.split(',')
                    if len(valeurs) >= 2:
                        valeur1 = int(valeurs[0])
                        valeur2 = int(valeurs[1])
                        update_labels(valeur1, valeur2)

                        # Simulation des touches clavier
                        if valeur1 > 50:
                            keyboard.press('v')
                            update_actions_display("Touche 'v' pressée")
                            time.sleep(0.1)
                            keyboard.release('v')
                        if valeur2 > 50:
                            keyboard.press('n')
                            update_actions_display("Touche 'n' pressée")
                            time.sleep(0.1)
                            keyboard.release('n')
        except ValueError:
            update_status("Erreur de conversion des données.")
        except serial.SerialException:
            update_status("Erreur de communication série. Tentative de reconnexion...")
            time.sleep(1)

# Mise à jour des labels dans l'interface
def update_labels(val1, val2):
    label_valeur1.config(text=f"Valeur 1: {val1}")
    label_valeur2.config(text=f"Valeur 2: {val2}")

# Mise à jour du statut
def update_status(message):
    label_status.config(text=message)

# Mise à jour de l'affichage des données brutes
def update_data_display(data):
    text_data.insert(tk.END, f"{data}\n")
    text_data.see(tk.END)

# Mise à jour de l'affichage des actions
def update_actions_display(action):
    text_actions.insert(tk.END, f"{action}\n")
    text_actions.see(tk.END)

# Fonction pour afficher un guide
def open_guide():
    guide_text = (
        "Bienvenue dans l'interface Rudders !\n\n"
        "1. Connectez votre palonnier Arduino.\n"
        "2. Entrez le port série (ex: COM3) et le baudrate (ex: 9600).\n"
        "3. Cliquez sur 'Démarrer' pour commencer la lecture des données.\n"
        "4. Surveillez les données affichées et les actions exécutées.\n"
        "5. Cliquez sur 'Arrêter' pour terminer la session.\n\n"
        "Pour plus d'informations, visitez le code source en ligne."
    )
    messagebox.showinfo("Guide", guide_text)

# Fonction pour ouvrir le lien vers le code source
def open_source():
    webbrowser.open("https://github.com/funvibestudio/rudders")

# Création de l'interface utilisateur
root = tk.Tk()
root.title("Interface Rudders")
root.geometry("700x500")
root.configure(bg="#1F2937")

style = ttk.Style()
style.configure("TLabel", foreground="#E5E7EB", background="#1F2937", font=("Arial", 12))
style.configure("TButton", font=("Arial", 10))
style.configure("TFrame", background="#1F2937")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Champ pour entrer le port série
label_port = ttk.Label(frame, text="Port Série:")
label_port.grid(row=0, column=0, sticky=tk.W)
entry_port = ttk.Entry(frame)
entry_port.grid(row=0, column=1, sticky=(tk.W, tk.E))
entry_port.insert(0, "COM3")

# Champ pour entrer le baudrate
label_baudrate = ttk.Label(frame, text="Baudrate:")
label_baudrate.grid(row=1, column=0, sticky=tk.W)
entry_baudrate = ttk.Entry(frame)
entry_baudrate.grid(row=1, column=1, sticky=(tk.W, tk.E))
entry_baudrate.insert(0, "9600")

# Boutons démarrer/arrêter
btn_start = ttk.Button(frame, text="Démarrer", command=lambda: start_reading(entry_port.get(), int(entry_baudrate.get())))
btn_start.grid(row=2, column=0, pady=10)
btn_stop = ttk.Button(frame, text="Arrêter", command=stop_reading)
btn_stop.grid(row=2, column=1, pady=10)

# Labels pour afficher les valeurs des capteurs
label_valeur1 = ttk.Label(frame, text="Valeur 1: ---")
label_valeur1.grid(row=3, column=0, columnspan=2, pady=5)
label_valeur2 = ttk.Label(frame, text="Valeur 2: ---")
label_valeur2.grid(row=4, column=0, columnspan=2, pady=5)

# Label pour afficher le statut
label_status = ttk.Label(frame, text="Statut: En attente", font=("Arial", 10), foreground="#60A5FA")
label_status.grid(row=5, column=0, columnspan=2, pady=10)

# Affichage des données brutes
label_data = ttk.Label(frame, text="Données Série:")
label_data.grid(row=6, column=0, columnspan=2, sticky=tk.W)
text_data = tk.Text(frame, height=8, width=70, bg="#111827", fg="#D1D5DB", insertbackground="white")
text_data.grid(row=7, column=0, columnspan=2, pady=5)

# Affichage des actions effectuées
label_actions = ttk.Label(frame, text="Actions Effectuées:")
label_actions.grid(row=8, column=0, columnspan=2, sticky=tk.W)
text_actions = tk.Text(frame, height=8, width=70, bg="#111827", fg="#D1D5DB", insertbackground="white")
text_actions.grid(row=9, column=0, columnspan=2, pady=5)

# Boutons pour le guide et le code source
btn_guide = ttk.Button(frame, text="?", command=open_guide)
btn_guide.grid(row=10, column=0, pady=10, sticky=tk.W)
btn_source = ttk.Button(frame, text="Code Source", command=open_source)
btn_source.grid(row=10, column=1, pady=10, sticky=tk.E)

# Gestion de la fermeture
def on_closing():
    stop_reading()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()