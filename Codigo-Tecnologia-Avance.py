import csv
from datetime import datetime
import os
import requests
import google.generativeai as genai
from collections import Counter

USUARIOS_FILE = "usuarios_simulados.csv"
HISTORIAL_FILE = "historial_global.csv"
API_KEY = "TU_API_KEY_OPENWEATHER"
GEMINI_API_KEY = "TU_API_KEY_GEMINI"

usuario_actual = None


# =========================
# FUNCIONES AUXILIARES
# =========================

def inicializar_archivos():
    if not os.path.exists(USUARIOS_FILE):
        with open(USUARIOS_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["username", "password"])

    if not os.path.exists(HISTORIAL_FILE):
        with open(HISTORIAL_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                "usuario",
                "ciudad",
                "fecha_hora",
                "temperatura",
                "condicion_clima",
                "humedad",
                "viento"
            ])


# =========================
# MENU ACCESO
# =========================

def menu_acceso():
    print("\n=== MENU ACCESO ===")
    print("1. Iniciar sesion")
    print("2. Registrarse")
    print("3. Salir")


# =========================
# VALIDAR PASSWORD
# =========================

def validar_password(password):
    errores = []

    if len(password) < 6:
        errores.append("La contraseña debe tener al menos 6 caracteres")

    if not any(c.isdigit() for c in password):
        errores.append("La contraseña debe contener un numero")

    if not any(c.isupper() for c in password):
        errores.append("La contraseña debe contener una mayuscula")

    return errores


# =========================
# REGISTRAR USUARIO
# =========================

def registrar_usuario():
    global usuario_actual

    username = input("Nuevo username: ")

    with open(USUARIOS_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for fila in reader:
            if fila["username"] == username:
                print("Usuario ya existente")
                return False

    password = input("Nueva contraseña: ")

    errores = validar_password(password)

    if errores:
        print("\nErrores en la contraseña:")
        for error in errores:
            print("-", error)
        return False

    with open(USUARIOS_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([username, password])

    usuario_actual = username

    print("Usuario registrado correctamente")
    return True


# =========================
# INICIAR SESION
# =========================

def iniciar_sesion():
    global usuario_actual

    username = input("Username: ")
    password = input("Password: ")

    with open(USUARIOS_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for fila in reader:
            if fila["username"] == username and fila["password"] == password:
                usuario_actual = username
                print("Login exitoso")
                return True

    print("Credenciales incorrectas")
    return False


# =========================
# MENU PRINCIPAL
# =========================

def menu_principal():
    print("\n=== MENU PRINCIPAL ===")
    print("1. Consultar clima")
    print("2. Ver historial")
    print("3. Estadisticas")
    print("4. Consejo IA")
    print("5. Acerca de")
    print("6. Cerrar sesion")


# =========================
# CONSULTAR CLIMA
# =========================

def consultar_clima():
    ciudad = input("Ingrese una ciudad: ")

    url = (
        f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}"
        f"&appid={API_KEY}&units=metric&lang=es"
    )

    respuesta = requests.get(url)

    if respuesta.status_code == 200:
        datos = respuesta.json()

        temperatura = datos["main"]["temp"]
        humedad = datos["main"]["humidity"]
        viento = datos["wind"]["speed"]
        condicion = datos["weather"][0]["description"]
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"\nClima en {ciudad}")
        print(f"Temperatura: {temperatura} °C")
        print(f"Condicion: {condicion}")
        print(f"Humedad: {humedad}%")
        print(f"Viento: {viento} m/s")

        with open(HISTORIAL_FILE, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                usuario_actual,
                ciudad,
                fecha_hora,
                temperatura,
                condicion,
                humedad,
                viento
            ])

    else:
        print("Error al obtener datos del clima")


# =========================
# VER HISTORIAL
# =========================

def ver_historial():
    ciudad = input("Ingrese una ciudad: ")

    encontrado = False

    with open(HISTORIAL_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        print("\n=== HISTORIAL ===")

        for fila in reader:
            if fila["usuario"] == usuario_actual and fila["ciudad"].lower() == ciudad.lower():
                encontrado = True

                print(
                    f"Fecha: {fila['fecha_hora']} | "
                    f"Ciudad: {fila['ciudad']} | "
                    f"Temp: {fila['temperatura']} °C | "
                    f"Condicion: {fila['condicion_clima']} | "
                    f"Humedad: {fila['humedad']}% | "
                    f"Viento: {fila['viento']} m/s"
                )

    if not encontrado:
        print("No hay consultas registradas")


# =========================
# ESTADISTICAS
# =========================

def estadisticas():
    ciudades = []
    temperaturas = []
    total = 0

    with open(HISTORIAL_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for fila in reader:
            ciudades.append(fila["ciudad"])
            temperaturas.append(float(fila["temperatura"]))
            total += 1

    if total == 0:
        print("No hay datos suficientes")
        return

    ciudad_mas_consultada = Counter(ciudades).most_common(1)[0][0]
    promedio_temperatura = sum(temperaturas) / len(temperaturas)

    print("\n=== ESTADISTICAS ===")
    print(f"Ciudad mas consultada: {ciudad_mas_consultada}")
    print(f"Promedio temperatura: {promedio_temperatura:.2f} °C")
    print(f"Total consultas: {total}")


# =========================
# CONSEJO IA
# =========================

def consejo_ia():
    try:
        ultima_consulta = None

        with open(HISTORIAL_FILE, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for fila in reader:
                if fila["usuario"] == usuario_actual:
                    ultima_consulta = fila

        if ultima_consulta is None:
            print("No hay consultas previas")
            return

        temperatura = ultima_consulta["temperatura"]
        condicion = ultima_consulta["condicion_clima"]
        humedad = ultima_consulta["humedad"]
        viento = ultima_consulta["viento"]

        genai.configure(api_key=GEMINI_API_KEY)

        model = genai.GenerativeModel("gemini-pro")

        prompt = (
            f"La temperatura es {temperatura}°C, "
            f"el clima es {condicion}, "
            f"la humedad es {humedad}% y "
            f"el viento es de {viento} m/s. "
            f"Dame un consejo breve sobre como vestirme hoy."
        )

        response = model.generate_content(prompt)

        print("=== CONSEJO IA ===")
        print(response.text)

    except Exception as e:
        print(f"Error al generar consejo IA: {e}")


# =========================
# ACERCA DE
# =========================

def acerca_de():
    print("=== ACERCA DE ===")
    print("GuardianClima ITBA")
    print("Aplicacion de consola desarrollada en Python")
    print("Permite consultar clima, guardar historial global,")
    print("generar estadisticas y obtener consejos con IA.")
    print("Seguridad:")
    print("Las contraseñas se validan con criterios minimos")
    print("de seguridad. El almacenamiento es simulado y")
    print("no seguro para aplicaciones reales.")
    print("Desarrolladores:")
    print("- Agregar integrantes del grupo")


# =========================
# CERRAR SESION
# =========================

def cerrar_sesion():
    global usuario_actual

    usuario_actual = None
    print("Sesion cerrada")


# =========================
# PROGRAMA PRINCIPAL
# =========================

def main():
    inicializar_archivos()

    print("Bienvenido a GuardianClima ITBA")

    usuario_logueado = False

    while not usuario_logueado:
        menu_acceso()

        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            usuario_logueado = iniciar_sesion()

        elif opcion == "2":
            usuario_logueado = registrar_usuario()

        elif opcion == "3":
            print("Programa finalizado")
            return

        else:
            print("Opcion invalida")

    while usuario_logueado:
        menu_principal()

        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            consultar_clima()

        elif opcion == "2":
            ver_historial()

        elif opcion == "3":
            estadisticas()

        elif opcion == "4":
            consejo_ia()

        elif opcion == "5":
            acerca_de()

        elif opcion == "6":
            cerrar_sesion()
            usuario_logueado = False

        else:
            print("Opcion invalida")


if __name__ == "__main__":
    main()