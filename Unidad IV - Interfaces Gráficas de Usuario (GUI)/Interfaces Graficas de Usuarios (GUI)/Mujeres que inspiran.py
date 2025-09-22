# mujeres_app.py
import tkinter as tk
from tkinter import messagebox

SEED = [
    {"nombre": "Matilde Hidalgo", "area": "Medicina / Sufragio",
     "logro": "Primera mujer en votar en Ecuador y doctora en medicina."},
    {"nombre": "Dolores Cacuango", "area": "Liderazgo social",
     "logro": "Defensora de derechos indígenas; cofundó escuelas bilingües."},
    {"nombre": "Marie Curie", "area": "Ciencia",
     "logro": "Doble Premio Nobel por investigaciones en radiactividad."},
    {"nombre": "Ada Lovelace", "area": "Tecnología",
     "logro": "Pionera de la programación con la Máquina Analítica."},
    {"nombre": "Frida Kahlo", "area": "Arte",
     "logro": "Pintora icónica; referente de identidad y resiliencia."},
]

class MujeresApp:
    def __init__(self, win: tk.Tk):
        self.win = win
        self.win.title("Mujeres que Inspiran - GUI")
        self.win.geometry("560x380")
        self.win.after(100, self._force_front)  # trae la ventana al frente

        # Estado
        self.items = list(SEED)

        # --- Encabezado ---
        tk.Label(self.win, text="Mujeres que inspiran", font=("Arial", 16, "bold")).pack(pady=(10, 6))
        tk.Label(self.win, text="Agrega nombres y consulta sus aportes.").pack()

        # --- Formulario ---
        form = tk.Frame(self.win)
        form.pack(fill="x", padx=12, pady=10)

        tk.Label(form, text="Nombre:").grid(row=0, column=0, sticky="w")
        tk.Label(form, text="Área:").grid(row=1, column=0, sticky="w")
        tk.Label(form, text="Logro:").grid(row=2, column=0, sticky="w")

        self.var_nombre = tk.StringVar()
        self.var_area = tk.StringVar()
        self.txt_logro = tk.Text(form, height=3, width=40)

        entry_nombre = tk.Entry(form, textvariable=self.var_nombre)
        entry_area   = tk.Entry(form, textvariable=self.var_area)

        entry_nombre.grid(row=0, column=1, sticky="ew", padx=6, pady=2)
        entry_area.grid(row=1, column=1, sticky="ew", padx=6, pady=2)
        self.txt_logro.grid(row=2, column=1, sticky="ew", padx=6, pady=2)
        form.columnconfigure(1, weight=1)
        entry_nombre.focus_set()

        # --- Botones ---
        buttons = tk.Frame(self.win)
        buttons.pack(fill="x", padx=12)
        tk.Button(buttons, text="Agregar", width=12, command=self.agregar).pack(side="left")
        tk.Button(buttons, text="Limpiar", width=12, command=self.limpiar_form).pack(side="left", padx=6)
        tk.Button(buttons, text="Eliminar seleccionado", width=18, command=self.eliminar_sel).pack(side="left")

        # --- Lista + Detalle ---
        panel = tk.Frame(self.win)
        panel.pack(fill="both", expand=True, padx=12, pady=10)

        self.listbox = tk.Listbox(panel, height=10)
        self.listbox.grid(row=0, column=0, sticky="nsew")
        self.listbox.bind("<<ListboxSelect>>", self.mostrar_detalle)

        scroll = tk.Scrollbar(panel, orient="vertical", command=self.listbox.yview)
        scroll.grid(row=0, column=1, sticky="ns")
        self.listbox.config(yscrollcommand=scroll.set)

        detail = tk.Frame(panel, bd=1, relief="groove", padx=8, pady=8)
        detail.grid(row=0, column=2, sticky="nsew", padx=(10, 0))

        tk.Label(detail, text="Detalle", font=("Arial", 12, "bold")).pack(anchor="w")
        self.lbl_nombre = tk.Label(detail, text="Nombre: -")
        self.lbl_area   = tk.Label(detail, text="Área: -")
        self.lbl_logro  = tk.Label(detail, text="Logro:", justify="left", wraplength=260)
        self.lbl_nombre.pack(anchor="w", pady=(6, 0))
        self.lbl_area.pack(anchor="w", pady=(2, 0))
        self.lbl_logro.pack(anchor="w", pady=(6, 0))

        panel.columnconfigure(0, weight=1)
        panel.columnconfigure(2, weight=2)
        panel.rowconfigure(0, weight=1)

        # Datos y atajos
        self.refrescar_lista()
        self.win.bind("<Return>", self.on_add)    # Enter = agregar
        self.win.bind("<Escape>", self.on_clear)  # Esc = limpiar formulario

    # ======= Lógica principal =======
    def agregar(self):
        nombre = self.var_nombre.get().strip()
        area   = self.var_area.get().strip()
        logro  = self.txt_logro.get("1.0", "end").strip()

        if not nombre or not area or not logro:
            messagebox.showwarning("Faltan datos", "Completa Nombre, Área y Logro.")
            return

        self.items.append({"nombre": nombre, "area": area, "logro": logro})
        self.refrescar_lista()
        self.limpiar_form()
        messagebox.showinfo("Agregado", f"Se agregó: {nombre}")

    def eliminar_sel(self):
        idx = self._indice_sel()
        if idx is None:
            messagebox.showinfo("Sin selección", "Selecciona un elemento de la lista.")
            return
        nombre = self.items[idx]["nombre"]
        del self.items[idx]
        self.refrescar_lista()
        self._limpiar_detalle()
        messagebox.showinfo("Eliminado", f"Se eliminó: {nombre}")

    def mostrar_detalle(self, event=None):
        idx = self._indice_sel()
        if idx is None:
            return
        it = self.items[idx]
        self.lbl_nombre.config(text=f"Nombre: {it['nombre']}")
        self.lbl_area.config(text=f"Área: {it['area']}")
        self.lbl_logro.config(text=f"Logro: {it['logro']}")

    # ======= Handlers de atajo =======
    def on_add(self, event=None):
        self.agregar()

    def on_clear(self, event=None):
        self.limpiar_form()

    # ======= Utilidades =======
    def refrescar_lista(self):
        self.listbox.delete(0, "end")
        for it in self.items:
            self.listbox.insert("end", it["nombre"])

    def limpiar_form(self):
        self.var_nombre.set("")
        self.var_area.set("")
        self.txt_logro.delete("1.0", "end")

    def _limpiar_detalle(self):
        self.lbl_nombre.config(text="Nombre: -")
        self.lbl_area.config(text="Área: -")
        self.lbl_logro.config(text="Logro:")

    def _indice_sel(self):
        sel = self.listbox.curselection()
        return None if not sel else sel[0]

    def _force_front(self):
        # Solo problemas de foco/orden de ventanas
        try:
            self.win.lift()
            self.win.attributes("-topmost", True)
            self.win.after(200, lambda: self.win.attributes("-topmost", False))
        except tk.TclError:
            # Si el gestor de ventanas no soporta algún atributo, lo ignoramos.
            pass


if __name__ == "__main__":
    ventana = tk.Tk()
    app = MujeresApp(ventana)
    ventana.mainloop()

