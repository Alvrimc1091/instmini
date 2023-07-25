import sys

comandos_disponibles = {
    "comando1": {
        "abreviatura": "c1",
        "funcion": "funcion_comando1",
        "comentario": "Este es el comando 1",
    },
    "comando2": {
        "abreviatura": "c2",
        "funcion": "funcion_comando2",
        "comentario": "Este es el comando 2",
    },
    "comando3": {
        "abreviatura": "c3",
        "funcion": "funcion_comando3",
        "comentario": "Este es el comando 3",
    },
    # Agrega más comandos aquí según sea necesario
}

def imprimir_lista_comandos():
    print("Lista de comandos disponibles:")
    for comando, detalles in comandos_disponibles.items():
        print(f"Comando: {comando} ({detalles['abreviatura']})")
        print(f"Función: {detalles['funcion']}")
        print(f"Comentario: {detalles['comentario']}")
        print()

def imprimir_info_comando(comando):
    if comando in comandos_disponibles:
        detalles = comandos_disponibles[comando]
        print(f"Información del comando {comando}:")
        print(f"Función: {detalles['funcion']}")
        print(f"Comentario: {detalles['comentario']}")
    else:
        print(f"El comando {comando} no existe.")

# Obtener los argumentos de línea de comandos
args = sys.argv[1:]

# Verificar los argumentos y ejecutar el comportamiento correspondiente
if len(args) == 0:
    imprimir_lista_comandos()
else:
    comando = args[0]
    imprimir_info_comando(comando)

