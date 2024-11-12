################################################
# Programmeerimine I
# 2024/2025 sügissemester
#
# Projekt
# Teema: To-Do nimekiri, kasutades tkinter ja SQLite.
#
#
# Autorid: Paul-Egert Peensalu, Mart Rõbin
#
# Lisakommentaar (nt käivitusjuhend): Praegu ei ole.
#
##################################################

import tkinter as tk
from tkinter import messagebox
import os

# Funktsioon ülesande lisamiseks nimekirja
def lisa_ülesanne():
    ülesanne = ülesande_sisestus.get()
    if ülesanne != "":
        ülesannete_nimekiri.insert(tk.END, ülesanne)
        ülesande_sisestus.delete(0, tk.END)
    else:
        messagebox.showwarning("Hoiatus", "Peate sisestama ülesande.")

# Funktsioon valitud ülesande kustutamiseks
def kustuta_ülesanne():
    try:
        valitud_ülesande_indeks = ülesannete_nimekiri.curselection()[0]
        ülesannete_nimekiri.delete(valitud_ülesande_indeks)
    except IndexError:
        messagebox.showwarning("Hoiatus", "Peate valima ülesande, mida kustutada.")

# Funktsioon ülesannete salvestamiseks kausta assets
def salvesta_ülesanded():
    # Veendu, et kataloog olemas
    os.makedirs(assets_kaust, exist_ok=True)
    # Salvestamine assets kaustale
    
    
    
    messagebox.showinfo("Info", "Ülesanded salvestatud edukalt.")

# Funktsioon ülesannete laadimiseks kaustast assets
def laadi_ülesanded():
    if os.path.exists(ülesannete_fail):





def main():
    # Algatame peamise rakenduse akna
    root = tk.Tk()
    root.title("Ülesannete Nimekirja Rakendus")
    root.geometry("300x400")

    # Kataloog ülesannete salvestamiseks
    global assets_kaust
    assets_kaust = "assets"
    global ülesannete_fail
    ülesannete_fail = os.path.join(assets_kaust, "ülesanded.txt")

    # Luuakse ja seadistatakse kasutajaliidese vidinad
    global ülesande_sisestus
    ülesande_sisestus = tk.Entry(root, width=35)
    ülesande_sisestus.pack(pady=10)

    lisa_ülesanne_nupp = tk.Button(root, text="Lisa Ülesanne", command=lisa_ülesanne)
    lisa_ülesanne_nupp.pack(pady=5)

    kustuta_ülesanne_nupp = tk.Button(root, text="Kustuta Ülesanne", command=kustuta_ülesanne)
    kustuta_ülesanne_nupp.pack(pady=5)

    global ülesannete_nimekiri
    ülesannete_nimekiri = tk.Listbox(root, width=35, height=15, selectmode=tk.SINGLE)
    ülesannete_nimekiri.pack(pady=10)

    salvesta_nupp = tk.Button(root, text="Salvesta Ülesanded", command=salvesta_ülesanded)
    salvesta_nupp.pack(side=tk.LEFT, padx=20)

    laadi_nupp = tk.Button(root, text="Laadi Ülesanded", command=laadi_ülesanded)
    laadi_nupp.pack(side=tk.RIGHT, padx=20)

    # Rakenduse käivitamine
    laadi_ülesanded()  # Laadib salvestatud ülesanded käivitamisel
    root.mainloop()

if __name__ == "__main__":
    main()

