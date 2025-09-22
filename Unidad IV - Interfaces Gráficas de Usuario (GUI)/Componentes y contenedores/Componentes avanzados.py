import re
import tkinter as tk
from tkinter import ttk, messagebox, Menu
from tkcalendar import DateEntry

# ---------------------- Utilidades ----------------------
HORA_RE = re.compile(r"(?:[01]\d|2[0-3]):[0-5]\d")

def hora_valida(s: str) -> bool:
    return bool(HORA_RE.fullmatch((s or "").strip()))

def hm_to_min(hhmm: str) -> int:
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)

def min_to_hm(total: int) -> str:
    h = total // 60
    m = total % 60
    return f"{h:02d}:{m:02d}"

# ---------------------- App ----------------------
class AgendaAvanzada(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Agenda — Componentes Avanzados")
        self.geometry("900x600")
        self.minsize(820, 560)

        # Datos: dict por fecha -> lista de dicts (actividades)
        self.data = {}
        self._edit_row_id = None  # iid del TreeView que está en edición

        # Estilo e iconos simples
        style = ttk.Style(self)
        if "clam" in style.theme_names():
            style.theme_use("clam")
        style.configure("Treeview", rowheight=26)

        # --- Top: Día + Filtro + Progreso ---
        top = ttk.Frame(self, padding=10)
        top.pack(fill="x")

        ttk.Label(top, text="Día:").pack(side="left")
        self.date_picker = DateEntry(top, date_pattern="yyyy-mm-dd", width=12)
        self.date_picker.pack(side="left", padx=(6, 12))
        self.date_picker.bind("<<DateEntrySelected>>", lambda _e: self.refresh_tree())

        ttk.Label(top, text="Filtro rápido:").pack(side="left")
        self.filter_var = tk.StringVar()
        filter_entry = ttk.Entry(top, textvariable=self.filter_var, width=28)
        filter_entry.pack(side="left", padx=6)
        ttk.Button(top, text="Aplicar", command=self.refresh_tree).pack(side="left", padx=2)
        ttk.Button(top, text="Limpiar", command=self._clear_filter).pack(side="left")

        # Progreso
        prog_box = ttk.Frame(top)
        prog_box.pack(side="right")
        self.progress = ttk.Progressbar(prog_box, orient=tk.HORIZONTAL, length=220, mode="determinate")
        self.progress.grid(row=0, column=0, padx=(0, 8))
        self.prog_label = ttk.Label(prog_box, text="0/0 (0%)")
        self.prog_label.grid(row=0, column=1)

        # --- Middle: Formulario ---
        form = ttk.LabelFrame(self, text="Nueva/Editar actividad", padding=10)
        form.pack(fill="x", padx=10)

        # Hora inicio/fin
        ttk.Label(form, text="Inicio (HH:MM):").grid(row=0, column=0, sticky="w")
        self.hini = ttk.Entry(form, width=8); self.hini.insert(0, "07:00")
        self.hini.grid(row=0, column=1, sticky="w", padx=(4, 12))

        ttk.Label(form, text="Fin (HH:MM):").grid(row=0, column=2, sticky="e")
        self.hfin = ttk.Entry(form, width=8); self.hfin.insert(0, "08:00")
        self.hfin.grid(row=0, column=3, sticky="w", padx=(4, 12))

        # Materia / lugar
        ttk.Label(form, text="Materia/Título:").grid(row=1, column=0, sticky="w", pady=(6,0))
        self.materia = ttk.Entry(form, width=32)
        self.materia.grid(row=1, column=1, columnspan=3, sticky="we", padx=(4, 12), pady=(6,0))

        ttk.Label(form, text="Lugar:").grid(row=2, column=0, sticky="w", pady=(6,0))
        self.lugar = ttk.Entry(form, width=32)
        self.lugar.grid(row=2, column=1, columnspan=3, sticky="we", padx=(4, 12), pady=(6,0))

        # Prioridad
        ttk.Label(form, text="Prioridad:").grid(row=0, column=4, sticky="e")
        self.prioridad = ttk.Combobox(form, values=["Baja","Media","Alta"], state="readonly", width=10)
        self.prioridad.current(1)
        self.prioridad.grid(row=0, column=5, sticky="w")

        # Notas (opcional, ligero)
        ttk.Label(form, text="Notas (opcional):").grid(row=1, column=4, sticky="ne", padx=(0,4))
        self.notas = ttk.Entry(form, width=28)
        self.notas.grid(row=1, column=5, sticky="we")

        # Ajuste columnas
        for c in range(6):
            form.columnconfigure(c, weight=1)

        # --- Acciones ---
        actions = ttk.Frame(self, padding=(10,8))
        actions.pack(fill="x")
        ttk.Button(actions, text="Agregar", command=self.add_item).pack(side="left")
        ttk.Button(actions, text="Editar seleccionado", command=self.start_edit).pack(side="left", padx=6)
        ttk.Button(actions, text="Aplicar cambios", command=self.apply_edit).pack(side="left")
        ttk.Separator(actions, orient="vertical").pack(side="left", fill="y", padx=8)
        ttk.Button(actions, text="Marcar Hecho", command=self.mark_done).pack(side="left")
        ttk.Button(actions, text="Eliminar", command=self.delete_selected).pack(side="left", padx=6)
        ttk.Separator(actions, orient="vertical").pack(side="left", fill="y", padx=8)
        ttk.Button(actions, text="Limpiar formulario", command=self.clear_form).pack(side="left")

        # --- Lista (TreeView) ---
        list_box = ttk.LabelFrame(self, text="Actividades del día", padding=8)
        list_box.pack(fill="both", expand=True, padx=10, pady=(0,10))

        cols = ("inicio","fin","materia","lugar","prioridad","estado")
        self.tree = ttk.Treeview(list_box, columns=cols, show="headings", selectmode="extended")
        headers = [
            ("inicio","Inicio",90,"center"),
            ("fin","Fin",90,"center"),
            ("materia","Materia/Título",220,"w"),
            ("lugar","Lugar",180,"w"),
            ("prioridad","Prioridad",90,"center"),
            ("estado","Estado",90,"center"),
        ]
        for key, lbl, w, anch in headers:
            self.tree.heading(key, text=lbl, command=lambda k=key: self.sort_by(k, False))
            self.tree.column(key, width=w, anchor=anch)

        # Scrollbar
        yscroll = ttk.Scrollbar(list_box, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=yscroll.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        yscroll.grid(row=0, column=1, sticky="ns")
        list_box.rowconfigure(0, weight=1); list_box.columnconfigure(0, weight=1)

        # Estilos para tags (hecho)
        self.tree.tag_configure("done", foreground="#6b7280")  # gris

        # Doble clic = detalle
        self.tree.bind("<Double-1>", self._show_detail)

        # Menú contextual
        self.ctx_menu = Menu(self, tearoff=0)
        self.ctx_menu.add_command(label="Marcar Hecho", command=self.mark_done)
        self.ctx_menu.add_command(label="Eliminar", command=self.delete_selected)
        self.tree.bind("<Button-3>", self._open_context_menu)

        # Render inicial
        self.refresh_tree()

    # ---------------------- Helpers de datos ----------------------
    def _current_date_key(self) -> str:
        return self.date_picker.get_date().strftime("%Y-%m-%d")

    def _get_day_list(self):
        key = self._current_date_key()
        if key not in self.data:
            self.data[key] = []
        return self.data[key]

    def _match_filter(self, rec: dict) -> bool:
        f = (self.filter_var.get() or "").lower()
        if not f:
            return True
        blob = " ".join([
            rec.get("inicio",""), rec.get("fin",""), rec.get("materia",""),
            rec.get("lugar",""), rec.get("prioridad",""), rec.get("estado",""),
            rec.get("notas","")
        ]).lower()
        return f in blob

    # ---------------------- Acciones ----------------------
    def add_item(self):
        d = self._read_form()
        if not self._validate(d):
            return
        day = self._get_day_list()
        day.append(d)
        self._sort_day(day)
        self.refresh_tree()
        self._clear_partials()

    def start_edit(self):
        sels = self.tree.selection()
        if not sels:
            messagebox.showinfo("Sin selección", "Selecciona una fila para editar.")
            return
        iid = sels[0]
        self._edit_row_id = iid
        values = self.tree.item(iid, "values")
        # Map: ("inicio","fin","materia","lugar","prioridad","estado")
        self.hini.delete(0, tk.END); self.hini.insert(0, values[0])
        self.hfin.delete(0, tk.END); self.hfin.insert(0, values[1])
        self.materia.delete(0, tk.END); self.materia.insert(0, values[2])
        self.lugar.delete(0, tk.END); self.lugar.insert(0, values[3])
        self.prioridad.set(values[4])
        # buscar notas: la guardamos en data
        rec = self._find_record_by_row(iid)
        self.notas.delete(0, tk.END); self.notas.insert(0, rec.get("notas",""))

    def apply_edit(self):
        if not self._edit_row_id:
            messagebox.showinfo("Sin edición", "Pulsa 'Editar seleccionado' primero.")
            return
        d = self._read_form()
        if not self._validate(d):
            return
        rec = self._find_record_by_row(self._edit_row_id)
        if not rec:
            self._edit_row_id = None
            return
        # mantener estado
        d["estado"] = rec["estado"]
        # actualizar datos
        day = self._get_day_list()
        idx = day.index(rec)
        day[idx] = d
        self._sort_day(day)
        self._edit_row_id = None
        self.refresh_tree()
        messagebox.showinfo("Actualizado", "Cambios aplicados.")

    def mark_done(self):
        sels = self.tree.selection()
        if not sels:
            messagebox.showinfo("Sin selección", "Selecciona una o más filas.")
            return
        changed = 0
        for iid in sels:
            rec = self._find_record_by_row(iid)
            if rec and rec["estado"] != "Hecho":
                rec["estado"] = "Hecho"
                changed += 1
        if changed:
            self.refresh_tree()

    def delete_selected(self):
        sels = self.tree.selection()
        if not sels:
            messagebox.showinfo("Sin selección", "Selecciona una o más filas.")
            return
        if not messagebox.askyesno("Confirmar", f"¿Eliminar {len(sels)} actividad(es)?"):
            return
        day = self._get_day_list()
        for iid in sels:
            rec = self._find_record_by_row(iid)
            if rec and rec in day:
                day.remove(rec)
        self.refresh_tree()

    # ---------------------- UI helpers ----------------------
    def _read_form(self) -> dict:
        return {
            "inicio": self.hini.get().strip(),
            "fin": self.hfin.get().strip(),
            "materia": self.materia.get().strip(),
            "lugar": self.lugar.get().strip(),
            "prioridad": self.prioridad.get().strip(),
            "estado": "Pendiente",
            "notas": self.notas.get().strip(),
        }

    def _validate(self, d: dict) -> bool:
        if not hora_valida(d["inicio"]):
            messagebox.showerror("Hora inválida", "Inicio debe ser HH:MM (24h).")
            return False
        if not hora_valida(d["fin"]):
            messagebox.showerror("Hora inválida", "Fin debe ser HH:MM (24h).")
            return False
        if d["materia"] == "":
            messagebox.showwarning("Falta título", "Ingresa la materia o título.")
            return False
        # coherencia temporal
        if hm_to_min(d["fin"]) <= hm_to_min(d["inicio"]):
            messagebox.showwarning("Rango horario", "La hora de fin debe ser mayor que la de inicio.")
            return False
        return True

    def _clear_filter(self):
        self.filter_var.set("")
        self.refresh_tree()

    def _clear_partials(self):
        self.materia.delete(0, tk.END)
        self.lugar.delete(0, tk.END)
        self.notas.delete(0, tk.END)

    def clear_form(self):
        self.hini.delete(0, tk.END); self.hini.insert(0, "07:00")
        self.hfin.delete(0, tk.END); self.hfin.insert(0, "08:00")
        self.materia.delete(0, tk.END)
        self.lugar.delete(0, tk.END)
        self.prioridad.set("Media")
        self.notas.delete(0, tk.END)
        self._edit_row_id = None

    def _sort_day(self, day_list):
        day_list.sort(key=lambda r: (hm_to_min(r["inicio"]), hm_to_min(r["fin"])))

    def _find_record_by_row(self, iid):
        """Mapea una fila del TreeView a su dict en self.data (por igualdad de campos)."""
        vals = self.tree.item(iid, "values")
        day = self._get_day_list()
        for r in day:
            if (r["inicio"], r["fin"], r["materia"], r["lugar"], r["prioridad"], r["estado"]) == vals:
                return r
        return None

    def refresh_tree(self):
        # limpiar
        for i in self.tree.get_children(""):
            self.tree.delete(i)

        # rellenar
        day = self._get_day_list()
        # Orden principal por inicio (si se cambió orden por columna, se aplicará al click)
        self._sort_day(day)

        done = 0
        total = 0
        for r in day:
            if not self._match_filter(r):
                continue
            tags = ()
            if r["estado"] == "Hecho":
                done += 1
                tags = ("done",)
            total += 1
            self.tree.insert("", "end", values=(
                r["inicio"], r["fin"], r["materia"], r["lugar"], r["prioridad"], r["estado"]
            ), tags=tags)

        # progreso
        pct = int((done/total)*100) if total else 0
        self.progress["value"] = pct
        self.prog_label.config(text=f"{done}/{total} ({pct}%)")

    # ---- Orden por columnas (toggle asc/desc) ----
    def sort_by(self, col_key, reverse):
        rows = [(self.tree.set(k, col_key), k) for k in self.tree.get_children("")]
        # conversión especial para horas
        if col_key in ("inicio","fin"):
            rows.sort(key=lambda x: hm_to_min(x[0]), reverse=reverse)
        else:
            rows.sort(key=lambda x: x[0].lower(), reverse=reverse)
        for idx, (_, k) in enumerate(rows):
            self.tree.move(k, "", idx)
        # siguiente click invierte
        self.tree.heading(col_key, command=lambda: self.sort_by(col_key, not reverse))

    # ---- Menú contextual ----
    def _open_context_menu(self, event):
        try:
            row_id = self.tree.identify_row(event.y)
            if row_id:
                # seleccionar fila bajo el cursor si no está seleccionada
                if row_id not in self.tree.selection():
                    self.tree.selection_set(row_id)
                self.ctx_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.ctx_menu.grab_release()

    # ---- Detalle (doble clic) ----
    def _show_detail(self, _e=None):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0], "values")
        rec = self._find_record_by_row(sel[0]) or {}
        messagebox.showinfo(
            "Detalle de actividad",
            "Inicio: {}\nFin: {}\nMateria/Título: {}\nLugar: {}\n"
            "Prioridad: {}\nEstado: {}\n\nNotas: {}".format(
                vals[0], vals[1], vals[2], vals[3], vals[4], vals[5],
                rec.get("notas","(sin notas)")
            )
        )

if __name__ == "__main__":
    app = AgendaAvanzada()
    app.mainloop()
