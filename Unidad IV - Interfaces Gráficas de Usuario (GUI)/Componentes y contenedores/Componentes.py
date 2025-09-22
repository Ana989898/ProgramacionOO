"""
Agenda diaria para estudiante (Tkinter)
"""

import json
import re
import tkinter as tk
from tkinter import messagebox, Menu, scrolledtext, filedialog
from tkinter import ttk

DIAS = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
PRIORIDADES = ["Baja","Media","Alta"]
TIPOS = ["Clase","Estudio","Tarea","Descanso"]

class AgendaEstudiante(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Agenda diaria del estudiante")
        self.geometry("980x640")
        self.minsize(900, 600)

        # Datos en memoria
        self.registros = []     # lista de dicts
        self._next_id = 1
        self._edit_id = None    # id del registro a actualizar

        # ====== Menú ======
        self._crear_menu()

        # ====== Contenedores ======
        cont = tk.Frame(self)
        cont.pack(fill="both", expand=True, padx=10, pady=10)

        # Izquierda: filtros + tabla
        left = tk.Frame(cont)
        left.pack(side="left", fill="both", expand=True)

        self._bloque_filtro(left)
        self._tabla(left)

        # Derecha: formulario y acciones
        right = tk.Frame(cont)
        right.pack(side="right", fill="y", padx=(10, 0))

        self._formulario(right)
        self._acciones(right)

        # Estado inicial
        self._refrescar_tabla()

    # ----------------- Construcción UI -----------------
    def _crear_menu(self):
        barra_menu = Menu(self)

        m_archivo = Menu(barra_menu, tearoff=0)
        m_archivo.add_command(label="Nuevo (limpiar todo)", command=self._nuevo_archivo)
        m_archivo.add_separator()
        m_archivo.add_command(label="Abrir JSON…", command=self._abrir_json)
        m_archivo.add_command(label="Guardar JSON…", command=self._guardar_json)
        m_archivo.add_separator()
        m_archivo.add_command(label="Salir", command=self.quit)
        barra_menu.add_cascade(label="Archivo", menu=m_archivo)

        m_ayuda = Menu(barra_menu, tearoff=0)
        m_ayuda.add_command(label="Acerca de", command=lambda:
            messagebox.showinfo("Acerca de",
                "Agenda diaria para estudiantes\n— Tkinter + TreeView\n— Guarda/abre JSON"))
        barra_menu.add_cascade(label="Ayuda", menu=m_ayuda)

        self.config(menu=barra_menu)

    def _bloque_filtro(self, parent):
        marco = tk.LabelFrame(parent, text="Vista por día", padx=10, pady=8)
        marco.pack(fill="x", pady=(0, 8))

        tk.Label(marco, text="Día:").pack(side="left")
        self.var_dia_vista = tk.StringVar(value=DIAS[0])
        dia_menu = tk.OptionMenu(marco, self.var_dia_vista, *DIAS, command=lambda _: self._refrescar_tabla())
        dia_menu.pack(side="left", padx=6)

        tk.Label(marco, text="Filtro rápido:").pack(side="left", padx=(10, 0))
        self.var_filtro = tk.StringVar()
        tk.Entry(marco, textvariable=self.var_filtro, width=32).pack(side="left", padx=6)
        tk.Button(marco, text="Aplicar", command=self._refrescar_tabla).pack(side="left", padx=2)
        tk.Button(marco, text="Limpiar", command=self._limpiar_filtro).pack(side="left")

    def _tabla(self, parent):
        marco = tk.LabelFrame(parent, text="Actividades del día", padx=8, pady=6)
        marco.pack(fill="both", expand=True)

        cols = ("inicio","fin","materia","lugar","tipo","prioridad","virtual","participantes","estado")
        self.tree = ttk.Treeview(marco, columns=cols, show="headings", selectmode="browse")

        defs = [
            ("inicio","Inicio",80,"center"),
            ("fin","Fin",80,"center"),
            ("materia","Materia/Título",160,"w"),
            ("lugar","Lugar",140,"w"),
            ("tipo","Tipo",90,"center"),
            ("prioridad","Prioridad",90,"center"),
            ("virtual","Virtual",70,"center"),
            ("participantes","Participantes",160,"w"),
            ("estado","Estado",85,"center"),
        ]
        for key, label, w, anch in defs:
            self.tree.heading(key, text=label)
            self.tree.column(key, width=w, anchor=anch)

        yscroll = ttk.Scrollbar(marco, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=yscroll.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        yscroll.grid(row=0, column=1, sticky="ns")

        marco.rowconfigure(0, weight=1)
        marco.columnconfigure(0, weight=1)

        # Doble clic para ver detalle
        self.tree.bind("<Double-1>", self._mostrar_detalle)

    def _formulario(self, parent):
        marco = tk.LabelFrame(parent, text="Nueva/Editar actividad", padx=10, pady=8)
        marco.pack(fill="x")

        # Día
        tk.Label(marco, text="Día:").grid(row=0, column=0, sticky="w")
        self.var_dia = tk.StringVar(value=DIAS[0])
        tk.OptionMenu(marco, self.var_dia, *DIAS).grid(row=0, column=1, sticky="w", pady=2)

        # Materia / título
        tk.Label(marco, text="Materia/Título:").grid(row=1, column=0, sticky="w")
        self.ent_materia = tk.Entry(marco, width=28)
        self.ent_materia.grid(row=1, column=1, columnspan=3, sticky="we", pady=2)

        # Inicio / Fin
        tk.Label(marco, text="Inicio (HH:MM):").grid(row=2, column=0, sticky="w")
        self.ent_inicio = tk.Entry(marco, width=10)
        self.ent_inicio.insert(0, "07:00")
        self.ent_inicio.grid(row=2, column=1, sticky="w")

        tk.Label(marco, text="Fin (HH:MM):").grid(row=2, column=2, sticky="e")
        self.ent_fin = tk.Entry(marco, width=10)
        self.ent_fin.insert(0, "08:00")
        self.ent_fin.grid(row=2, column=3, sticky="w")

        # Lugar
        tk.Label(marco, text="Lugar:").grid(row=3, column=0, sticky="w")
        self.ent_lugar = tk.Entry(marco, width=28)
        self.ent_lugar.grid(row=3, column=1, columnspan=3, sticky="we", pady=2)

        # Tipo (Radiobuttons)
        tk.Label(marco, text="Tipo:").grid(row=4, column=0, sticky="w")
        self.var_tipo = tk.StringVar(value=TIPOS[0])
        fila_tipo = tk.Frame(marco)
        fila_tipo.grid(row=4, column=1, columnspan=3, sticky="w")
        for t in TIPOS:
            tk.Radiobutton(fila_tipo, text=t, variable=self.var_tipo, value=t).pack(side="left", padx=(0,8))

        # Prioridad (OptionMenu)
        tk.Label(marco, text="Prioridad:").grid(row=5, column=0, sticky="w")
        self.var_prioridad = tk.StringVar(value="Media")
        tk.OptionMenu(marco, self.var_prioridad, *PRIORIDADES).grid(row=5, column=1, sticky="w")

        # Virtual (Checkbutton)
        self.var_virtual = tk.IntVar(value=0)
        tk.Checkbutton(marco, text="Virtual", variable=self.var_virtual).grid(row=5, column=2, sticky="w")

        # Participantes
        tk.Label(marco, text="Participantes (coma):").grid(row=6, column=0, sticky="w")
        self.ent_participantes = tk.Entry(marco, width=28)
        self.ent_participantes.grid(row=6, column=1, columnspan=3, sticky="we", pady=2)

        # Notas
        tk.Label(marco, text="Notas:").grid(row=7, column=0, sticky="nw")
        self.txt_notas = scrolledtext.ScrolledText(marco, width=34, height=6, wrap=tk.WORD)
        self.txt_notas.grid(row=7, column=1, columnspan=3, sticky="we", pady=4)

        # Ajuste de columnas
        for c in range(4):
            marco.columnconfigure(c, weight=1)

    def _acciones(self, parent):
        marco = tk.LabelFrame(parent, text="Acciones", padx=10, pady=10)
        marco.pack(fill="x", pady=(8,0))

        tk.Button(marco, text="Agregar", command=self.agregar).pack(fill="x", pady=3)
        tk.Button(marco, text="Editar seleccionado", command=self.editar).pack(fill="x", pady=3)
        tk.Button(marco, text="Aplicar cambios", command=self.aplicar).pack(fill="x", pady=3)
        tk.Button(marco, text="Marcar como Hecho", command=self.marcar_hecho).pack(fill="x", pady=3)
        tk.Button(marco, text="Eliminar seleccionado", command=self.eliminar).pack(fill="x", pady=3)
        tk.Button(marco, text="Limpiar formulario", command=self._limpiar_formulario).pack(fill="x", pady=(6,0))

    # ----------------- Lógica -----------------
    @staticmethod
    def _val_hora(s):
        return bool(re.fullmatch(r"(?:[01]\d|2[0-3]):[0-5]\d", s or ""))

    def _tomar_form(self):
        return {
            "id": None,
            "dia": self.var_dia.get().strip(),
            "inicio": self.ent_inicio.get().strip(),
            "fin": self.ent_fin.get().strip(),
            "materia": self.ent_materia.get().strip(),
            "lugar": self.ent_lugar.get().strip(),
            "tipo": self.var_tipo.get().strip(),
            "prioridad": self.var_prioridad.get().strip(),
            "virtual": bool(self.var_virtual.get()),
            "participantes": self.ent_participantes.get().strip(),
            "notas": self.txt_notas.get("1.0", tk.END).strip(),
            "estado": "Pendiente",
        }

    def _validar(self, d):
        if d["dia"] not in DIAS:
            messagebox.showerror("Día inválido", "Selecciona un día válido.")
            return False
        if not self._val_hora(d["inicio"]):
            messagebox.showerror("Hora inválida", "Inicio debe ser HH:MM (24h).")
            return False
        if not self._val_hora(d["fin"]):
            messagebox.showerror("Hora inválida", "Fin debe ser HH:MM (24h).")
            return False
        if d["materia"] == "":
            messagebox.showwarning("Falta información", "Ingresa la materia o título de la actividad.")
            return False
        return True

    def agregar(self):
        d = self._tomar_form()
        if not self._validar(d):
            return
        d["id"] = self._next_id; self._next_id += 1
        self.registros.append(d)
        self._refrescar_tabla()
        self._limpiar_parciales()

    def editar(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Sin selección", "Selecciona una actividad en la tabla.")
            return