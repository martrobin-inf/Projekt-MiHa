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
# Lisakommentaar:
# Rakenduse käivitamiseks veenduge, et kõik vajalikud failid on olemas:
# 1. Python peab olema teie arvutisse installeeritud.
# 2. Veenduge, et SQLite andmebaas (./data/ülesanded.db) oleks õigesti salvestatud programmi kaustas. Kui faili ei leita, loob rakendus selle automaatselt.
# 3. Käivitage skript, kasutades käsureal käsku `python miha.py` või IDE-s.
# 
# Rakendus võimaldab lisada, kustutada ja otsida ülesandeid. Prioriteedid tähistatakse erinevate taustavärvidega:
# - Kõrge: punane
# - Keskmine: kollane
# - Madal: roheline
# 
# Kuupäeva sisestamisel peab järgima formaati YYYY-MM-DD.
#
##################################################

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
from datetime import datetime

# SQLite andmebaasi ühendamine ja loomine
# See funktsioon loob vajaliku tabeli, kui seda pole olemas
# ja tagab ühenduse andmebaasiga

def init_db():
    global conn, cursor
    db_path = "./data/ülesanded.db"  # Andmebaasi fail asub rakenduse kataloogis
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS ülesanded (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        pealkiri TEXT NOT NULL,
                        kategooria TEXT,
                        prioriteet TEXT,
                        tähtaeg TEXT,
                        loodud TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )''')
    conn.commit()

# Funktsioon ülesande lisamiseks andmebaasi
# Kasutaja sisestab vajalikud andmed vormi kaudu

def lisa_ülesanne():
    pealkiri = ülesande_sisestus.get()
    kategooria = kategooria_var.get()
    prioriteet = prioriteet_var.get()
    tähtaeg = tähtaeg_sisestus.get()

    if not pealkiri.strip():
        messagebox.showwarning("Viga", "Ülesande pealkiri ei tohi olla tühi.")
        return

    try:
        if tähtaeg:
            datetime.strptime(tähtaeg, "%Y-%m-%d")  # Kontrollime kuupäeva formaati
        cursor.execute("INSERT INTO ülesanded (pealkiri, kategooria, prioriteet, tähtaeg) VALUES (?, ?, ?, ?)",
                       (pealkiri, kategooria, prioriteet, tähtaeg))
        conn.commit()
        laadi_ülesanded()
        tühjenda_väljad()
        messagebox.showinfo("Õnnestus", "Ülesanne edukalt lisatud.")
    except ValueError:
        messagebox.showerror("Viga", "Kuupäev peab olema formaadis YYYY-MM-DD.")

# Funktsioon valitud ülesande kustutamiseks

def kustuta_ülesanne():
    valitud_üksus = ülesannete_loend.selection()
    if not valitud_üksus:
        messagebox.showwarning("Viga", "Valige ülesanne kustutamiseks.")
        return

    ülesande_id = ülesannete_loend.item(valitud_üksus[0], 'values')[0]
    cursor.execute("DELETE FROM ülesanded WHERE id = ?", (ülesande_id,))
    conn.commit()
    laadi_ülesanded()

# Funktsioon ülesannete laadimiseks andmebaasist ja kuvamiseks tabelis

def laadi_ülesanded():
    for item in ülesannete_loend.get_children():
        ülesannete_loend.delete(item)

    otsingu_päring = otsingu_sisestus.get().strip().lower()
    if otsingu_päring:
        cursor.execute("SELECT * FROM ülesanded WHERE LOWER(pealkiri) LIKE ? OR LOWER(kategooria) LIKE ?", 
                       (f"%{otsingu_päring}%", f"%{otsingu_päring}%"))
    else:
        cursor.execute("SELECT * FROM ülesanded ORDER BY CASE prioriteet WHEN 'Kõrge' THEN 1 WHEN 'Keskmine' THEN 2 WHEN 'Madal' THEN 3 END")

    for row in cursor.fetchall():
        ülesande_id, pealkiri, kategooria, prioriteet, tähtaeg, _ = row
        värv = "#ffcccc" if prioriteet == "Kõrge" else "#ffffcc" if prioriteet == "Keskmine" else "#ccffcc"
        ülesannete_loend.insert("", tk.END, values=(ülesande_id, pealkiri, kategooria, prioriteet, tähtaeg), tags=(värv,))

    ülesannete_loend.tag_configure("#ffcccc", background="#ffcccc")
    ülesannete_loend.tag_configure("#ffffcc", background="#ffffcc")
    ülesannete_loend.tag_configure("#ccffcc", background="#ccffcc")

# Tühjendame vormiväljad peale ülesande lisamist

def tühjenda_väljad():
    ülesande_sisestus.delete(0, tk.END)
    kategooria_var.set(kategooriad[0])
    prioriteet_var.set(prioriteedid[0])
    tähtaeg_sisestus.delete(0, tk.END)

# Peamise akna loomine
root = tk.Tk()
root.title("Ülesannete haldur | Projekt MiHa")
root.geometry("800x600")
root.configure(bg="#f7f9fc")

# Andmebaasiga ühendamine
init_db()

# Stiilid
stiil = ttk.Style()
stiil.configure("TLabel", font=("Arial", 12), background="#f7f9fc")
stiil.configure("TButton", font=("Arial", 12), padding=6)
stiil.configure("Treeview", font=("Arial", 10))
stiil.configure("Treeview.Heading", font=("Arial", 12, "bold"))

# UI komponendid
sisestus_raam = tk.Frame(root, bg="#f7f9fc")
sisestus_raam.pack(pady=10, padx=10, fill=tk.X)

# Ülesande sisestusväli
tk.Label(sisestus_raam, text="Ülesande pealkiri:", bg="#f7f9fc", font=("Arial", 12)).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
ülesande_sisestus = tk.Entry(sisestus_raam, width=50, font=("Arial", 12))
ülesande_sisestus.grid(row=0, column=1, padx=5, pady=5)

# Ülesannete kategooriad
kategooriad = ["Töö", "Isiklik", "Projektid", "Haridus", "Muud"]  # Lisatud rohkem kategooriaid
tk.Label(sisestus_raam, text="Kategooria:", bg="#f7f9fc", font=("Arial", 12)).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
kategooria_var = tk.StringVar(value=kategooriad[0])
kategooria_menüü = ttk.Combobox(sisestus_raam, textvariable=kategooria_var, values=kategooriad, state="readonly", font=("Arial", 12))
kategooria_menüü.grid(row=1, column=1, padx=5, pady=5)

# Ülesannete prioriteet
prioriteedid = ["Kõrge", "Keskmine", "Madal"]
tk.Label(sisestus_raam, text="Prioriteet:", bg="#f7f9fc", font=("Arial", 12)).grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
prioriteet_var = tk.StringVar(value=prioriteedid[0])
prioriteet_menüü = ttk.Combobox(sisestus_raam, textvariable=prioriteet_var, values=prioriteedid, state="readonly", font=("Arial", 12))
prioriteet_menüü.grid(row=2, column=1, padx=5, pady=5)

# Tähtaeg
tk.Label(sisestus_raam, text="Tähtaeg (YYYY-MM-DD):", bg="#f7f9fc", font=("Arial", 12)).grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
tähtaeg_sisestus = tk.Entry(sisestus_raam, font=("Arial", 12))
tähtaeg_sisestus.grid(row=3, column=1, padx=5, pady=5)

# Nupud
nupu_raam = tk.Frame(root)
nupu_raam.pack(pady=10)

lisa_nupp = tk.Button(nupu_raam, text="Lisa ülesanne", command=lisa_ülesanne, bg="#4caf50", fg="white", font=("Arial", 12), relief="flat")
lisa_nupp.grid(row=0, column=0, padx=5)

kustuta_nupp = tk.Button(nupu_raam, text="Kustuta ülesanne", command=kustuta_ülesanne, bg="#f44336", fg="white", font=("Arial", 12), relief="flat")
kustuta_nupp.grid(row=0, column=1, padx=5)

# Otsing
otsingu_raam = tk.Frame(root, bg="#f7f9fc")
otsingu_raam.pack(pady=10, fill=tk.X)

tk.Label(otsingu_raam, text="Otsing:", bg="#f7f9fc", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
otsingu_sisestus = tk.Entry(otsingu_raam, font=("Arial", 12))
otsingu_sisestus.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
otsingu_nupp = tk.Button(otsingu_raam, text="Otsi", command=laadi_ülesanded, bg="#2196f3", fg="white", font=("Arial", 12), relief="flat")
otsingu_nupp.pack(side=tk.RIGHT, padx=5)

# Ülesannete tabel
veerud = ("id", "pealkiri", "kategooria", "prioriteet", "tähtaeg")
ülesannete_loend = ttk.Treeview(root, columns=veerud, show="headings")

for veerg in veerud:
    ülesannete_loend.heading(veerg, text=veerg.capitalize())
    ülesannete_loend.column(veerg, anchor=tk.CENTER)

ülesannete_loend.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Ülesannete laadimine ja automaatne salvestamine
laadi_ülesanded()

# Rakenduse käivitamine
root.mainloop()

# Andmebaasi ühenduse sulgemine rakenduse lõpetamisel
conn.close()

