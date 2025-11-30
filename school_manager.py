
# School Management System - Production Version
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from pathlib import Path
import webbrowser
import urllib.parse as urlparse

TEXTS = {
    "ar": {
        "title": "نظام إدارة الطلاب والفصول",
        "class": "الفصل",
        "name": "الاسم",
        "age": "العمر",
        "id": "رقم الهوية",
        "grade": "الدرجة",
        "status": "الحالة",
        "pass": "ناجح",
        "fail": "راسب",
        "add_class": "إضافة فصل",
        "add_student": "إضافة طالب",
        "show_class": "عرض طلاب الفصل",
        "export": "تصدير / طباعة",
        "email": "إيميل"
    }
}

DATA_FILE = Path("school_data.json")
classes = {}

def save():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(classes, f, ensure_ascii=False, indent=2)

def load():
    global classes
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            classes = json.load(f)

def add_class():
    c = class_entry.get()
    if c not in classes:
        classes[c] = []
        save()

def add_student():
    c = class_entry.get()
    s = {
        "name": name_entry.get(),
        "age": age_entry.get(),
        "id": id_entry.get(),
        "grade": grade_entry.get()
    }
    s["status"] = "ناجح" if float(s["grade"]) >= 50 else "راسب"
    classes[c].append(s)
    save()

def show_students():
    c = class_entry.get()
    win = tk.Toplevel(root)
    tree = ttk.Treeview(win, columns=("n","a","i","g","s"), show="headings")
    for col,text in zip(("n","a","i","g","s"),("الاسم","العمر","الهوية","الدرجة","الحالة")):
        tree.heading(col, text=text)
    tree.pack(fill="both", expand=True)
    for st in classes.get(c,[]):
        tree.insert("", "end", values=(st["name"],st["age"],st["id"],st["grade"],st["status"]))

root = tk.Tk()
root.title("School Manager")

class_entry = ttk.Entry(root); class_entry.pack()
ttk.Button(root, text="إضافة فصل", command=add_class).pack()

name_entry = ttk.Entry(root); name_entry.pack()
age_entry = ttk.Entry(root); age_entry.pack()
id_entry = ttk.Entry(root); id_entry.pack()
grade_entry = ttk.Entry(root); grade_entry.pack()

ttk.Button(root, text="إضافة طالب", command=add_student).pack()
ttk.Button(root, text="عرض طلاب الفصل", command=show_students).pack()

load()
root.mainloop()
