# Generador de contraseñas seguras
# Lenguaje: Python 3
# Autor: Alexander Lalangui

import string
import secrets
import tkinter as tk
from tkinter import messagebox

# Constantes
LONGITUD_MINIMA = 8
LONGITUD_MAXIMA = 32
SYMBOLS = "!@#$%^&*()-_=+[]{}|;:,.<>/?"  # Caracteres especiales permitidos

#  CAPA DE LÓGICA

def validar_configuracion(longitud, usar_mayus, usar_minus, usar_numeros, usar_simbolos):
    """Comprueba que la configuración sea válida.
    Devuelve (True, "") si todo está bien o (False, "mensaje") si hay error."""

    # Condicional 1: la longitud debe estar dentro del rango permitido
    if longitud < LONGITUD_MINIMA or longitud > LONGITUD_MAXIMA:
        return False, f"La longitud debe estar entre {LONGITUD_MINIMA} y {LONGITUD_MAXIMA} caracteres."

    # Condicional 2: debe haber al menos un tipo de carácter marcado
    if not (usar_mayus or usar_minus or usar_numeros or usar_simbolos):
        return False, "Selecciona al menos un tipo de carácter."

    return True, ""


def construir_caracteres(usar_mayus, usar_minus, usar_numeros, usar_simbolos):
    """Arma la lista de grupos de caracteres que el usuario eligió."""
    grupos = []

    # Se agrega cada grupo solo si su casilla está marcada
    if usar_mayus:
        grupos.append(string.ascii_uppercase)   # ABC...Z
    if usar_minus:
        grupos.append(string.ascii_lowercase)   # abc...z
    if usar_numeros:
        grupos.append(string.digits)            # 0123456789
    if usar_simbolos:
        grupos.append(SYMBOLS)

    return grupos


def generar_contrasena(longitud, grupos):
    """Crea la contraseña aleatoria.
    Garantiza que aparezca al menos un carácter de CADA grupo elegido."""
    caracteres = []

    # Bucle 1: tomar un carácter obligatorio de cada grupo seleccionado
    for grupo in grupos:
        caracteres.append(secrets.choice(grupo))

    # Unimos todos los grupos en una sola cadena para el resto de posiciones
    todos = "".join(grupos)

    # Bucle 2: completar la contraseña hasta la longitud pedida
    while len(caracteres) < longitud:
        caracteres.append(secrets.choice(todos))

    # Mezclamos para que los caracteres obligatorios no queden siempre al inicio
    secrets.SystemRandom().shuffle(caracteres)

    return "".join(caracteres)


def evaluar_fortaleza(contrasena):
    """Evalúa de forma orientativa qué tan fuerte es la contraseña."""
    tiene_mayus = tiene_minus = tiene_numero = tiene_simbolo = False

    # Bucle 3: revisar carácter por carácter qué tipos contiene
    for caracter in contrasena:
        if caracter.isupper():
            tiene_mayus = True
        elif caracter.islower():
            tiene_minus = True
        elif caracter.isdigit():
            tiene_numero = True
        else:
            tiene_simbolo = True

    # Puntaje: 1 punto por cada tipo de carácter + puntos por longitud
    puntos = tiene_mayus + tiene_minus + tiene_numero + tiene_simbolo
    if len(contrasena) >= 12:
        puntos += 1
    if len(contrasena) >= 16:
        puntos += 1

    # Condicional para traducir el puntaje a un nivel
    if puntos <= 2:
        return "Débil", "red"
    elif puntos <= 4:
        return "Media", "orange"
    else:
        return "Fuerte", "green"

#  CAPA DE PRESENTACIÓN (interfaz gráfica)

def al_presionar_generar():
    """Se ejecuta cuando el usuario presiona 'Generar contraseña'."""
    # 1. Leer la configuración elegida en la ventana
    longitud = valor_longitud.get()
    usar_mayus = var_mayus.get()
    usar_minus = var_minus.get()
    usar_numeros = var_numeros.get()
    usar_simbolos = var_simbolos.get()

    # 2. Validar; si hay error se muestra el mensaje y se detiene aquí
    es_valida, mensaje = validar_configuracion(longitud, usar_mayus, usar_minus,
                                               usar_numeros, usar_simbolos)
    if not es_valida:
        messagebox.showerror("Configuración no válida", mensaje)
        return

    # 3. Construir caracteres y generar la contraseña
    grupos = construir_caracteres(usar_mayus, usar_minus, usar_numeros, usar_simbolos)
    contrasena = generar_contrasena(longitud, grupos)

    # 4. Mostrar el resultado y su fortaleza
    texto_resultado.set(contrasena)
    nivel, color = evaluar_fortaleza(contrasena)
    etiqueta_fortaleza.config(text=f"Fortaleza: {nivel}", fg=color)


def al_presionar_copiar():
    """Copia la contraseña mostrada al portapapeles del sistema."""
    contrasena = texto_resultado.get()

    if contrasena == "":
        messagebox.showinfo("Copiar", "Primero genera una contraseña.")
    else:
        ventana.clipboard_clear()
        ventana.clipboard_append(contrasena)
        messagebox.showinfo("Copiar", "Contraseña copiada al portapapeles.")


# ---------------- Construcción de la ventana ----------------
ventana = tk.Tk()
ventana.title("Generador seguro de contraseñas")
ventana.geometry("440x380")
ventana.resizable(False, False)

# Título
tk.Label(ventana, text="Generador seguro de contraseñas",
         font=("Arial", 14, "bold")).pack(pady=10)

# --- Panel de configuración ---
panel_config = tk.LabelFrame(ventana, text="Configuración", padx=10, pady=10)
panel_config.pack(padx=15, fill="x")

tk.Label(panel_config, text="Longitud:").grid(row=0, column=0, sticky="w")
valor_longitud = tk.IntVar(value=12)
tk.Scale(panel_config, from_=4, to=40, orient="horizontal",
         variable=valor_longitud, length=250).grid(row=0, column=1, columnspan=2)

# Variables de las casillas (True = marcada)
var_mayus = tk.BooleanVar(value=True)
var_minus = tk.BooleanVar(value=True)
var_numeros = tk.BooleanVar(value=True)
var_simbolos = tk.BooleanVar(value=False)

tk.Checkbutton(panel_config, text="Mayúsculas (A-Z)", variable=var_mayus).grid(row=1, column=0, columnspan=2, sticky="w")
tk.Checkbutton(panel_config, text="Minúsculas (a-z)", variable=var_minus).grid(row=2, column=0, columnspan=2, sticky="w")
tk.Checkbutton(panel_config, text="Números (0-9)", variable=var_numeros).grid(row=1, column=2, sticky="w")
tk.Checkbutton(panel_config, text="Símbolos (!@#...)", variable=var_simbolos).grid(row=2, column=2, sticky="w")

# --- Botón principal ---
tk.Button(ventana, text="Generar contraseña", bg="#1F4E78", fg="white",
          font=("Arial", 11, "bold"), command=al_presionar_generar).pack(pady=12)

# --- Panel de resultado ---
panel_resultado = tk.LabelFrame(ventana, text="Resultado", padx=10, pady=10)
panel_resultado.pack(padx=15, fill="x")

texto_resultado = tk.StringVar(value="")
tk.Entry(panel_resultado, textvariable=texto_resultado, font=("Consolas", 12),
         width=34, justify="center").pack()

etiqueta_fortaleza = tk.Label(panel_resultado, text="Fortaleza: -", font=("Arial", 10, "bold"))
etiqueta_fortaleza.pack(pady=5)

tk.Button(panel_resultado, text="Copiar", width=12, command=al_presionar_copiar).pack()

# Mantiene la ventana abierta esperando las acciones del usuario
ventana.mainloop()
