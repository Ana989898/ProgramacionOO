import re
import tkinter as tk
from tkinter import ttk, messagebox, Menu, scrolledtext

# ---------------------- Datos base ----------------------
DIAS = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
PRIORIDADES = ["Baja","Media","Alta"]
TIPOS = ["Clase","Estudio","Tarea","Descanso"]

REGISTROS = []   # lista de dicts con todas las actividades
NEXT_ID = 1      # id incremental
EDIT_ID = None   # id en edición (cuando se pulsa "Editar seleccionado")

# ---------------------- Utilidades ----------------------
def val_hora(s: str) -> bool:
    return bool(re.fullmatch(r"(?:[01]\d|2[0-3]):[0-5]\d", (s or "").strip()))

def buscar_por_id(rid: int):
    for r in REGISTROS:
        if r["id"] == rid:
            return r
    return None

# ---------------------- Handlers ----------------------
def aplicar_filtro():
    refrescar_tabla()

def limpiar_filtro():
    var_filtro.set("")
    refrescar_tabla()

def agregar():
    global NEXT_ID
    d = tomar_formulario()
    if not validar(d):
        return
    d["id"] = NEXT_ID; NEXT_ID += 1
    REGISTROS.append(d)
    refrescar_tabla()
    limpiar_parciales()

def editar():
    global EDIT_ID
    sel = tree.selection()
    if not sel:
        messagebox.showinfo("Sin selección", "Selecciona una actividad en la tabla.")
        return
    rid = tree.item(sel[0], "text")
    try:
        rid = int(rid)
    except Exception:
        return
    rec = buscar_por_id(rid)
    if not rec:
        return

    # cargar en formulario
    var_dia.set(rec["dia"])
    ent_inicio.delete(0, tk.END); ent_inicio.insert(0, rec["inicio"])
    ent_fin.delete(0, tk.END);    ent_fin.insert(0, rec["fin"])
    ent_materia.delete(0, tk.END); ent_materia.insert(0, rec["materia"])
    ent_lugar.delete(0, tk.END);   ent_lugar.insert(0, rec["lugar"])
    var_tipo.set(rec["tipo"])
    combo_prioridad.set(rec["prioridad"])
    var_virtual.set(1 if rec["virtual"] else 0)
    ent_participantes.delete(0, tk.END); ent_participantes.insert(0, rec["participantes"])
    txt_notas.delete("1.0", tk.END); txt_notas.insert("1.0", rec["notas"])

    EDIT_ID = rec["id"]

def aplicar_cambios():
    global EDIT_ID
    if not EDIT_ID:
        messagebox.showinfo("Sin edición", "Primero pulsa 'Editar seleccionado'.")
        return
    d = tomar_formulario()
    if not validar(d):
        return

    # mantener id y estado
    for i, r in enumerate(REGISTROS):
        if r["id"] == EDIT_ID:
            d["id"] = r["id"]
            d["estado"] = r["estado"]
            REGISTROS[i] = d
            break
    EDIT_ID = None
    refrescar_tabla()
    messagebox.showinfo("Actualizado", "Cambios aplicados.")

def marcar_hecho():
    sel = tree.selection()
    if not sel:
        messagebox.showinfo("Sin selección", "Selecciona una actividad.")
        return
    rid = tree.item(sel[0], "text")
    try:
        rid = int(rid)
    except Exception:
        return
    rec = buscar_por_id(rid)
    if not rec: return
    rec["estado"] = "Hecho"
    refrescar_tabla()

def eliminar():
    sel = tree.selection()
    if not sel:
        messagebox.showinfo("Sin selección", "Selecciona una actividad.")
        return
    rid = tree.item(sel[0], "text")
    try:
        rid = int(rid)
    except Exception:
        return
    rec = buscar_por_id(rid)
    if not rec: return
    if messagebox.askyesno("Confirmar", f"¿Eliminar '{rec['materia']}' ({rec['inicio']}-{rec['fin']})?"):
        # filtrar fuera
        REGISTROS[:] = [x for x in REGISTROS if x["id"] != rid]
        refrescar_tabla()

def mostrar_detalle(_evt=None):
    sel = tree.selection()
    if not sel: return
    rid = tree.item(sel[0], "text")
    try:
        rid = int(rid)
    except Exception:
        return
    rec = buscar_por_id(rid)
    if not rec: return
    msg = (
        f"Día: {rec['dia']}\n"
        f"Inicio: {rec['inicio']}  Fin: {rec['fin']}\n"
        f"Materia/Título: {rec['materia']}\n"
        f"Lugar: {rec['lugar']}\n"
        f"Tipo: {rec['tipo']} | Prioridad: {rec['prioridad']} | Virtual: {'Sí' if rec['virtual'] else 'No'}\n"
        f"Participantes: {rec['participantes']}\n"
        f"Estado: {rec['estado']}\n\n"
        f"Notas:\n{rec['notas'] if rec['notas'] else '(sin notas)'}"
    )
    messagebox.showinfo("Detalle de actividad", msg)

def limpiar_formulario():
    global EDIT_ID
    var_dia.set(DIAS[0])
    ent_inicio.delete(0, tk.END); ent_inicio.insert(0, "07:00")
    ent_fin.delete(0, tk.END);    ent_fin.insert(0, "08:00")
    ent_materia.delete(0, tk.END)
    ent_lugar.delete(0, tk.END)
    var_tipo.set(TIPOS[0])
    combo_prioridad.set("Media")
    var_virtual.set(0)
    ent_participantes.delete(0, tk.END)
    txt_notas.delete("1.0", tk.END)
    EDIT_ID = None

def limpiar_parciales():
    ent_materia.delete(0, tk.END)
    ent_lugar.delete(0, tk.END)
    ent_participantes.delete(0, tk.END)
    txt_notas.delete("1.0", tk.END)

def tomar_formulario():
    return {
        "id": None,
        "dia": var_dia.get().strip(),
        "inicio": ent_inicio.get().strip(),
        "fin": ent_fin.get().strip(),
        "materia": ent_materia.get().strip(),
        "lugar": ent_lugar.get().strip(),
        "tipo": var_tipo.get().strip(),
        "prioridad": combo_prioridad.get().strip(),
        "virtual": bool(var_virtual.get()),
        "participantes": ent_participantes.get().strip(),
        "notas": txt_notas.get("1.0", tk.END).strip(),
        "estado": "Pendiente",
    }

def validar(d) -> bool:
    if d["dia"] not in DIAS:
        messagebox.showerror("Día inválido", "Selecciona un día válido.")
        return False
    if not val_hora(d["inicio"]):
        messagebox.showerror("Hora inválida", "Inicio debe ser HH:MM (24h).")
        return False
    if not val_hora(d["fin"]):
        messagebox.showerror("Hora inválida", "Fin debe ser HH:MM (24h).")
        return False
    if not d["materia"]:
        messagebox.showwarning("Falta información", "Ingresa la materia o título.")
        return False
    return True

def refrescar_tabla():
    # limpiar
    for i in tree.get_children(""):
        tree.delete(i)

    dia_vista = var_dia_vista.get().strip()
    filtro = (var_filtro.get() or "").lower()

    # ordenar por inicio
    registros = sorted(
        [r for r in REGISTROS if r["dia"] == dia_vista],
        key=lambda x: x["inicio"]
    )

    for r in registros:
        texto = " ".join([
            r["materia"], r["lugar"], r["tipo"], r["prioridad"],
            r["participantes"], r["notas"], r["estado"]
        ]).lower()
        if filtro and filtro not in texto:
            continue
        tree.insert(
            "", "end", text=str(r["id"]),
            values=(
                r["inicio"], r["fin"], r["materia"], r["lugar"], r["tipo"],
                r["prioridad"], "Sí" if r["virtual"] else "No",
                r["participantes"], r["estado"]
            )
        )

# ---------------------- Ventana principal ----------------------
root = tk.Tk()
root.title("Componentes y Contenedores — Agenda diaria del estudiante")
root.geometry("1000x620")

# ===== Menú =====
barra_menu = Menu(root)
menu_archivo = Menu(barra_menu, tearoff=0)
menu_archivo.add_command(label="Nuevo", command=limpiar_formulario)
menu_archivo.add_separator()
menu_archivo.add_command(label="Salir", command=root.quit)
barra_menu.add_cascade(label="Archivo", menu=menu_archivo)
root.config(menu=barra_menu)

# ===== Contenedor: Filtro por día =====
panel_dia = tk.Frame(root, borderwidth=2, relief="groove", bg="#f0efe9")
panel_dia.pack(padx=10, pady=(10,5), fill=tk.X)
tk.Label(panel_dia, text="Vista por día", bg="#f0efe9").pack(side=tk.LEFT, padx=6)
var_dia_vista = tk.StringVar(value=DIAS[0])
tk.OptionMenu(panel_dia, var_dia_vista, *DIAS, command=lambda _=None: aplicar_filtro()).pack(side=tk.LEFT)
tk.Label(panel_dia, text="Filtro rápido:", bg="#f0efe9").pack(side=tk.LEFT, padx=(12,4))
var_filtro = tk.StringVar()
tk.Entry(panel_dia, textvariable=var_filtro, width=34).pack(side=tk.LEFT, padx=4)
tk.Button(panel_dia, text="Aplicar", command=aplicar_filtro).pack(side=tk.LEFT, padx=2)
tk.Button(panel_dia, text="Limpiar", command=limpiar_filtro).pack(side=tk.LEFT)

# ===== Contenedor: Panel de entrada =====
panel_entrada = tk.Frame(root, borderwidth=2, relief="groove", bg="light gray")
panel_entrada.pack(padx=10, pady=5, fill=tk.X)
tk.Label(panel_entrada, text="Entrada de datos", bg="light gray").pack(side=tk.TOP, fill=tk.X)

fila1 = tk.Frame(panel_entrada, bg="light gray"); fila1.pack(fill=tk.X, padx=8, pady=4)
tk.Label(fila1, text="Día:", bg="light gray").pack(side=tk.LEFT)
var_dia = tk.StringVar(value=DIAS[0])
tk.OptionMenu(fila1, var_dia, *DIAS).pack(side=tk.LEFT, padx=6)
tk.Label(fila1, text="Materia/Título:", bg="light gray").pack(side=tk.LEFT, padx=(10,4))
ent_materia = tk.Entry(fila1); ent_materia.pack(side=tk.LEFT, fill=tk.X, expand=True)

fila2 = tk.Frame(panel_entrada, bg="light gray"); fila2.pack(fill=tk.X, padx=8, pady=4)
tk.Label(fila2, text="Inicio (HH:MM):", bg="light gray").pack(side=tk.LEFT)
ent_inicio = tk.Entry(fila2, width=8); ent_inicio.insert(0,"07:00"); ent_inicio.pack(side=tk.LEFT, padx=(2,10))
tk.Label(fila2, text="Fin (HH:MM):", bg="light gray").pack(side=tk.LEFT)
ent_fin = tk.Entry(fila2, width=8); ent_fin.insert(0,"08:00"); ent_fin.pack(side=tk.LEFT, padx=(2,10))
tk.Label(fila2, text="Lugar:", bg="light gray").pack(side=tk.LEFT)
ent_lugar = tk.Entry(fila2); ent_lugar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=4)

# ===== Contenedor: Panel de botones/selección =====
panel_botones = tk.Frame(root, borderwidth=2, relief="groove", bg="light blue")
panel_botones.pack(padx=10, pady=5, fill=tk.X)
tk.Label(panel_botones, text="Selección y acciones", bg="light blue").pack(side=tk.TOP, fill=tk.X)

fila_sel = tk.Frame(panel_botones, bg="light blue"); fila_sel.pack(fill=tk.X, padx=8, pady=4)
# Combobox Prioridad
tk.Label(fila_sel, text="Prioridad:", bg="light blue").pack(side=tk.LEFT)
combo_prioridad = ttk.Combobox(fila_sel, values=PRIORIDADES, width=10, state="readonly")
combo_prioridad.current(1); combo_prioridad.pack(side=tk.LEFT, padx=(2,12))
# Radiobuttons Tipo
var_tipo = tk.StringVar(value=TIPOS[0])
for t in TIPOS:
    tk.Radiobutton(fila_sel, text=t, variable=var_tipo, value=t, bg="light blue").pack(side=tk.LEFT, padx=(0,8))
# Checkbutton Virtual
var_virtual = tk.IntVar(value=0)
tk.Checkbutton(fila_sel, text="Virtual", variable=var_virtual, bg="light blue").pack(side=tk.LEFT, padx=(8,0))

fila_part = tk.Frame(panel_botones, bg="light blue"); fila_part.pack(fill=tk.X, padx=8, pady=(0,6))
tk.Label(fila_part, text="Participantes (coma):", bg="light blue").pack(side=tk.LEFT)
ent_participantes = tk.Entry(fila_part); ent_participantes.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=6)

fila_acc = tk.Frame(panel_botones, bg="light blue"); fila_acc.pack(fill=tk.X, padx=8, pady=(0,6))
tk.Button(fila_acc, text="Agregar", command=agregar).pack(side=tk.LEFT, padx=4)
tk.Button(fila_acc, text="Editar seleccionado", command=editar).pack(side=tk.LEFT, padx=4)
tk.Button(fila_acc, text="Aplicar cambios", command=aplicar_cambios).pack(side=tk.LEFT, padx=4)
tk.Button(fila_acc, text="Marcar Hecho", command=marcar_hecho).pack(side=tk.LEFT, padx=4)
tk.Button(fila_acc, text="Eliminar", command=eliminar).pack(side=tk.LEFT, padx=4)
tk.Button(fila_acc, text="Limpiar formulario", command=limpiar_formulario).pack(side=tk.LEFT, padx=4)

# ===== Contenedor: Panel de texto (Notas) =====
panel_texto = tk.Frame(root, borderwidth=2, relief="groove", bg="light green")
panel_texto.pack(padx=10, pady=5, fill=tk.X)
tk.Label(panel_texto, text="Notas", bg="light green").pack(side=tk.TOP, fill=tk.X)
txt_notas = scrolledtext.ScrolledText(panel_texto, wrap=tk.WORD, height=5)
txt_notas.pack(padx=8, pady=6, fill=tk.X)

# ===== Contenedor: Lista (TreeView) =====
panel_lista = tk.Frame(root, borderwidth=2, relief="groove", bg="#eef7ff")
panel_lista.pack(padx=10, pady=(5,10), fill=tk.BOTH, expand=True)
tk.Label(panel_lista, text="Actividades del día", bg="#eef7ff").pack(side=tk.TOP, fill=tk.X)

cols = ("inicio","fin","materia","lugar","tipo","prioridad","virtual","participantes","estado")
tree = ttk.Treeview(panel_lista, columns=cols, show="headings", selectmode="browse")
defs = [
    ("inicio","Inicio",80,"center"),
    ("fin","Fin",80,"center"),
    ("materia","Materia/Título",180,"w"),
    ("lugar","Lugar",160,"w"),
    ("tipo","Tipo",90,"center"),
    ("prioridad","Prioridad",90,"center"),
    ("virtual","Virtual",70,"center"),
    ("participantes","Participantes",200,"w"),
    ("estado","Estado",90,"center"),
]
for key, label, w, anch in defs:
    tree.heading(key, text=label)
    tree.column(key, width=w, anchor=anch)

yscroll = ttk.Scrollbar(panel_lista, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=yscroll.set)

# colocación
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(8,0), pady=8)
yscroll.pack(side=tk.RIGHT, fill=tk.Y, padx=(0,8), pady=8)

tree.bind("<Double-1>", mostrar_detalle)

# Inicializar tabla
var_filtro = tk.StringVar()
var_dia_vista = tk.StringVar(value=DIAS[0])
refrescar_tabla()

root.mainloop()
