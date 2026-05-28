import csv
import requests
import google.generativeai as genai


def iniciar_sesion():
    pass


def registrar_usuario():
    pass


def validar_password(password):
    pass


def consultar_clima(usuario_actual):
    pass


def guardar_historial(usuario_actual, datos_clima):
    pass


def ver_historial(usuario_actual):
    pass


def mostrar_estadisticas():
    pass


def consejo_ia(usuario_actual):
    pass


def acerca_de():
    pass


def cerrar_sesion():
    pass


programa_activo = True


while programa_activo:

    print("\nGUARDIANCLIMA ITBA")
    print("1. Iniciar sesión")
    print("2. Registrar usuario")
    print("3. Salir")

    opcion = input("Elegí una opción: ")

    if opcion == "1":

        usuario_actual = iniciar_sesion()

        if usuario_actual != None:

            sesion_activa = True

            while sesion_activa:

                print("\nMENU PRINCIPAL")
                print("1. Consultar clima")
                print("2. Ver historial")
                print("3. Estadísticas")
                print("4. Consejo IA")
                print("5. Acerca de")
                print("6. Cerrar sesión")

                opcion_menu = input("Elegí una opción: ")

                if opcion_menu == "1":
                    consultar_clima(usuario_actual)

                elif opcion_menu == "2":
                    ver_historial(usuario_actual)

                elif opcion_menu == "3":
                    mostrar_estadisticas()

                elif opcion_menu == "4":
                    consejo_ia(usuario_actual)

                elif opcion_menu == "5":
                    acerca_de()

                elif opcion_menu == "6":

                    cerrar_sesion()
                    sesion_activa = False

                else:
                    print("Opción inválida")

    elif opcion == "2":

        usuario_actual = registrar_usuario()

    elif opcion == "3":

        print("Programa finalizado")
        programa_activo = False

    else:
        print("Opción inválida")
