"""
Gestor de Tareas — Aplicación de Escritorio
=============================================
Ejemplo académico de Aplicación de Escritorio.

Tecnología:
- Lenguaje: Python 3
- GUI: Tkinter (librería estándar de Python, nativa del sistema operativo)
- Persistencia: archivo local JSON (tareas.json), sin necesidad de internet
  ni de un navegador para funcionar.

Características que demuestra (ver reporte adjunto para el detalle):
- Interfaz gráfica nativa (ventanas, menús, cuadros de diálogo)
- Ejecución local, no requiere navegador ni conexión a internet
- Persistencia de datos en el sistema de archivos local
- Operaciones CRUD completas (crear, leer, actualizar, eliminar)
- Atajos de teclado
- Barra de menú nativa (Archivo, Ayuda)
- Cuadros de diálogo modales (confirmación, "Acerca de")
- Manejo de eventos de teclado y mouse
- Acceso directo al sistema de archivos del usuario
- Instalable/ejecutable de forma independiente (no depende de un servidor)
"""

import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, font
from datetime import datetime

ARCHIVO_DATOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tareas.json")

# Paleta de colores
BG         = "#1e1e2e"   # fondo principal
BG2        = "#2a2a3e"   # fondo secundario (lista, entrada)
ACCENT     = "#7c6af7"   # morado acento
ACCENT_HOV = "#9b8df9"
VERDE      = "#4caf7d"
ROJO       = "#e05c5c"
AMARILLO   = "#f0c040"
FG         = "#e0e0f0"   # texto principal
FG_DIM     = "#888aaa"   # texto secundario
FG_DONE    = "#555577"   # texto tarea completada


class GestorTareas:
    def __init__(self, root):
        self.root = root
        self.root.title("✅ Gestor de Tareas")
        self.root.geometry("580x540")
        self.root.minsize(460, 400)
        self.root.configure(bg=BG)
        self.root.resizable(True, True)

        self.tareas = self.cargar_tareas()

        self._crear_menu()
        self._crear_widgets()
        self._refrescar_lista()

        self.root.protocol("WM_DELETE_WINDOW", self._salir)

    # ---------- Persistencia ----------
    def cargar_tareas(self):
        if os.path.exists(ARCHIVO_DATOS):
            try:
                with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                return []
        return []

    def guardar_tareas(self):
        with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
            json.dump(self.tareas, f, ensure_ascii=False, indent=2)

    # ---------- Menú ----------
    def _crear_menu(self):
        barra = tk.Menu(self.root, bg=BG2, fg=FG, activebackground=ACCENT,
                        activeforeground=FG, relief="flat", bd=0)

        menu_archivo = tk.Menu(barra, tearoff=0, bg=BG2, fg=FG,
                               activebackground=ACCENT, activeforeground=FG)
        menu_archivo.add_command(label="💾  Guardar ahora", accelerator="Ctrl+S",
                                 command=self.guardar_tareas)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="🚪  Salir", command=self._salir)
        barra.add_cascade(label="Archivo", menu=menu_archivo)

        menu_ayuda = tk.Menu(barra, tearoff=0, bg=BG2, fg=FG,
                             activebackground=ACCENT, activeforeground=FG)
        menu_ayuda.add_command(label="ℹ️  Acerca de", command=self._acerca_de)
        barra.add_cascade(label="Ayuda", menu=menu_ayuda)

        self.root.config(menu=barra)
        self.root.bind("<Control-s>", lambda e: self.guardar_tareas())

    # ---------- Widgets ----------
    def _crear_widgets(self):
        # ── Encabezado ──────────────────────────────────────────────
        header = tk.Frame(self.root, bg=ACCENT, pady=14)
        header.pack(fill="x")
        tk.Label(header, text="📋  Gestor de Tareas",
                 bg=ACCENT, fg="white",
                 font=("Segoe UI", 16, "bold")).pack()

        # ── Entrada ─────────────────────────────────────────────────
        marco_entrada = tk.Frame(self.root, bg=BG, padx=14, pady=12)
        marco_entrada.pack(fill="x")

        self.entrada = tk.Entry(marco_entrada, bg=BG2, fg=FG,
                                insertbackground=FG, relief="flat",
                                font=("Segoe UI", 11), bd=0,
                                highlightthickness=2,
                                highlightbackground=BG2,
                                highlightcolor=ACCENT)
        self.entrada.pack(side="left", fill="x", expand=True, ipady=7, padx=(0, 8))
        self.entrada.bind("<Return>", lambda e: self._agregar_tarea())

        self._btn(marco_entrada, "＋ Agregar", ACCENT, self._agregar_tarea).pack(side="left")

        # ── Lista ────────────────────────────────────────────────────
        marco_lista = tk.Frame(self.root, bg=BG, padx=14)
        marco_lista.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(marco_lista, bg=BG2, troughcolor=BG,
                                 relief="flat", bd=0)
        scrollbar.pack(side="right", fill="y")

        self.lista = tk.Listbox(
            marco_lista,
            yscrollcommand=scrollbar.set,
            bg=BG2, fg=FG,
            selectbackground=ACCENT, selectforeground="white",
            activestyle="none",
            relief="flat", bd=0,
            font=("Segoe UI", 11),
            highlightthickness=0,
            cursor="hand2",
        )
        self.lista.pack(fill="both", expand=True)
        scrollbar.config(command=self.lista.yview)
        self.lista.bind("<Double-Button-1>", lambda e: self._marcar_completada())

        # ── Botones de acción ────────────────────────────────────────
        marco_botones = tk.Frame(self.root, bg=BG, padx=14, pady=10)
        marco_botones.pack(fill="x")

        self._btn(marco_botones, "✔ Completar",  VERDE,    self._marcar_completada).pack(side="left", padx=(0, 6))
        self._btn(marco_botones, "✏ Editar",     AMARILLO, self._editar_tarea,  fg="#1e1e2e").pack(side="left", padx=(0, 6))
        self._btn(marco_botones, "🗑 Eliminar",  ROJO,     self._eliminar_tarea).pack(side="left")

        # ── Barra de estado ──────────────────────────────────────────
        self.estado = tk.StringVar(value="Listo.")
        tk.Label(self.root, textvariable=self.estado,
                 bg=BG, fg=FG_DIM,
                 font=("Segoe UI", 9), anchor="w",
                 padx=14, pady=6).pack(fill="x")

    def _btn(self, parent, texto, color, comando, fg="white"):
        """Botón plano con color de fondo."""
        b = tk.Button(
            parent, text=texto, command=comando,
            bg=color, fg=fg, activebackground=ACCENT_HOV,
            activeforeground="white", relief="flat", bd=0,
            font=("Segoe UI", 10, "bold"),
            padx=12, pady=6, cursor="hand2",
        )
        b.bind("<Enter>", lambda e: b.config(bg=ACCENT_HOV))
        b.bind("<Leave>", lambda e: b.config(bg=color))
        return b

    def _refrescar_lista(self):
        self.lista.delete(0, tk.END)
        for i, tarea in enumerate(self.tareas):
            if tarea["completada"]:
                texto = f"  ✔  {tarea['texto']}"
            else:
                texto = f"  ○  {tarea['texto']}"
            self.lista.insert(tk.END, texto)
            self.lista.itemconfig(i, fg=FG_DONE if tarea["completada"] else FG)

        total = len(self.tareas)
        hechas = sum(t["completada"] for t in self.tareas)
        self.estado.set(f"  {total} tarea(s)  •  {hechas} completada(s)  •  {total - hechas} pendiente(s)")

    # ---------- CRUD ----------
    def _agregar_tarea(self):
        texto = self.entrada.get().strip()
        if not texto:
            return
        self.tareas.append({
            "texto": texto,
            "completada": False,
            "creada": datetime.now().isoformat(timespec="seconds"),
        })
        self.entrada.delete(0, tk.END)
        self.guardar_tareas()
        self._refrescar_lista()

    def _indice_seleccionado(self):
        sel = self.lista.curselection()
        return sel[0] if sel else None

    def _marcar_completada(self):
        i = self._indice_seleccionado()
        if i is None:
            return
        self.tareas[i]["completada"] = not self.tareas[i]["completada"]
        self.guardar_tareas()
        self._refrescar_lista()

    def _editar_tarea(self):
        i = self._indice_seleccionado()
        if i is None:
            return
        nuevo = simpledialog.askstring(
            "Editar tarea", "Nuevo texto:", initialvalue=self.tareas[i]["texto"]
        )
        if nuevo:
            self.tareas[i]["texto"] = nuevo.strip()
            self.guardar_tareas()
            self._refrescar_lista()

    def _eliminar_tarea(self):
        i = self._indice_seleccionado()
        if i is None:
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar esta tarea?"):
            self.tareas.pop(i)
            self.guardar_tareas()
            self._refrescar_lista()

    # ---------- Diálogos ----------
    def _acerca_de(self):
        messagebox.showinfo(
            "Acerca de",
            "Gestor de Tareas v2.0\nEjemplo de Aplicación de Escritorio\nPython 3 + Tkinter",
        )

    def _salir(self):
        self.guardar_tareas()
        self.root.destroy()


if __name__ == "__main__":
    ventana = tk.Tk()
    app = GestorTareas(ventana)
    ventana.mainloop()
