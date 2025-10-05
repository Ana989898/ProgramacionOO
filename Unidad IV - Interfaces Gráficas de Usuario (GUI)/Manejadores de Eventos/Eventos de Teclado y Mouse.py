import tkinter as tk
from tkinter import ttk

def on_left_click(event):
    info.set("Clic izquierdo detectado.")
def on_right_click(event):
    info.set("Clic derecho detectado.")
def on_middle_click(event):
    info.set("Clic de rueda (scroll) detectado.")
def on_enter(event):
    panel.config(background="#e8f4ff")
    info.set("Mouse dentro del panel.")
def on_leave(event):
    panel.config(background="SystemButtonFace")
    info.set("Mouse fuera del panel.")
def on_motion(event):
    pos.set(f"Posición: x={event.x}, y={event.y}")

def on_key(event):
    key.set(f"Tecla: {event.keysym}")
def clear_panel(event=None):
    info.set("Panel listo. Usa clics y mueve el mouse.")
    pos.set("Posición: x=0, y=0")
    key.set("Tecla: —")
def quit_app(event=None):
    root.destroy()

root = tk.Tk()
root.title("4.1.4-4 – Eventos de Teclado y Mouse (Tkinter)")
root.geometry("520x380")

# Variables de estado
info = tk.StringVar(value="Panel listo. Usa clics y mueve el mouse.")
pos  = tk.StringVar(value="Posición: x=0, y=0")
key  = tk.StringVar(value="Tecla: —")

# Instrucciones
ttk.Label(
    root,
    text=("Instrucciones:\n"
          "• Clic izquierdo/derecho/rueda dentro del panel.\n"
          "• Mueve el mouse para ver la posición.\n"
          "• Teclado: presiona cualquier tecla para mostrarla.\n"
          "• Atajos: R = Reiniciar panel, Esc = Salir."),
    justify="left"
).pack(padx=10, pady=8, anchor="w")

# Panel de interacción
panel = ttk.Frame(root, height=220, relief="groove")
panel.pack(fill="both", expand=True, padx=10, pady=(0,8))

lbl_info = ttk.Label(panel, textvariable=info)
lbl_info.place(relx=0.5, rely=0.35, anchor="center")

lbl_pos = ttk.Label(panel, textvariable=pos)
lbl_pos.place(relx=0.5, rely=0.55, anchor="center")

lbl_key = ttk.Label(panel, textvariable=key)
lbl_key.place(relx=0.5, rely=0.75, anchor="center")

# Bindings de mouse sobre el panel
panel.bind("<Button-1>", on_left_click)
panel.bind("<Button-2>", on_middle_click)
panel.bind("<Button-3>", on_right_click)
panel.bind("<Enter>", on_enter)
panel.bind("<Leave>", on_leave)
panel.bind("<Motion>", on_motion)

# Bindings de teclado sobre ventana
root.bind("<Key>", on_key)
root.bind("<r>", clear_panel)
root.bind("<R>", clear_panel)
root.bind("<Escape>", quit_app)

root.mainloop()
