import tkinter as tk
from tkinter import ttk, messagebox

class TaskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("4.1.4-3 – Gestor de Tareas (Botón y Teclado)")
        self.root.geometry("520x380")

        # --- Top: entrada y botones ---
        top = ttk.Frame(root, padding=10)
        top.pack(fill="x")
        ttk.Label(top, text="Nueva tarea:").pack(side="left")
        self.entry = ttk.Entry(top)
        self.entry.pack(side="left", fill="x", expand=True, padx=6)
        self.entry.focus_set()

        self.btn_add = ttk.Button(top, text="Añadir", command=self.add_task)
        self.btn_add.pack(side="left", padx=(0, 6))
        self.btn_done = ttk.Button(top, text="Completar", command=self.mark_done)
        self.btn_done.pack(side="left")
        self.btn_del = ttk.Button(top, text="Eliminar", command=self.delete_task)
        self.btn_del.pack(side="left", padx=(6, 0))

        # --- Centro: lista de tareas ---
        mid = ttk.Frame(root, padding=(10, 0, 10, 10))
        mid.pack(fill="both", expand=True)
        self.listbox = tk.Listbox(mid, selectmode="extended")
        self.listbox.pack(side="left", fill="both", expand=True)
        vsb = ttk.Scrollbar(mid, orient="vertical", command=self.listbox.yview)
        vsb.pack(side="right", fill="y")
        self.listbox.configure(yscrollcommand=vsb.set)

        # --- Barra inferior: atajos y estado ---
        bottom = ttk.Frame(root, padding=(10, 6))
        bottom.pack(fill="x")
        ttk.Label(
            bottom,
            text="Atajos: Enter=Añadir • C=Completar • D/Delete=Eliminar • Esc=Salir",
            foreground="#555"
        ).pack(side="left")
        self.status = ttk.Label(bottom, text="")
        self.status.pack(side="right")
        self.update_status()

        # --- Vinculaciones teclado ---
        self.entry.bind("<Return>", self.add_task)
        root.bind("<c>", self.mark_done)
        root.bind("<C>", self.mark_done)
        root.bind("<Delete>", self.delete_task)
        root.bind("<d>", self.delete_task)
        root.bind("<D>", self.delete_task)
        root.bind("<Escape>", lambda e: root.destroy())

    # --------- Lógica ---------
    def add_task(self, event=None):
        text = self.entry.get().strip()
        if not text:
            self.flash_entry()
            return
        self.listbox.insert("end", "[ ] " + text)
        self.entry.delete(0, "end")
        self.update_status()

    def mark_done(self, event=None):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo("Completar", "Selecciona una o más tareas.")
            return
        for idx in sel:
            text = self.listbox.get(idx)
            if text.startswith("[ ] "):
                self.listbox.delete(idx)
                self.listbox.insert(idx, text.replace("[ ] ", "[✓] "))
                self.listbox.itemconfig(idx, foreground="gray")
        self.update_status()

    def delete_task(self, event=None):
        sel = list(self.listbox.curselection())
        if not sel:
            messagebox.showinfo("Eliminar", "Selecciona una o más tareas.")
            return
        for idx in reversed(sel):
            self.listbox.delete(idx)
        self.update_status()

    def update_status(self):
        total = self.listbox.size()
        done = sum(1 for i in range(total) if self.listbox.get(i).startswith("[✓] "))
        pend = total - done
        self.status.config(text=f"Tareas: {total} • Pendientes: {pend} • Completadas: {done}")

    def flash_entry(self):
        orig = self.entry.cget("foreground")
        self.entry.config(foreground="red")
        self.root.after(150, lambda: self.entry.config(foreground=orig))
        self.entry.focus_set()

def main():
    root = tk.Tk()
    try:
        ttk.Style().theme_use("clam")
    except:
        pass
    TaskApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
