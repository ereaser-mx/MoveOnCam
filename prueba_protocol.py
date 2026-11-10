import time

from protocol import crear_socket, enviar_datos, cerrar_socket


def main():
    sock = crear_socket()

    datos = {
    "tipo": "articulaciones",
    "brazos": {
        "DERECHO": {
            "articulaciones": {
                "Hombro": {
                    "x": 0.42,
                    "y": 0.30,
                    "z": -0.05,
                    "visibilidad": 0.98
                },
                "Codo": {
                    "x": 0.51,
                    "y": 0.44,
                    "z": -0.02,
                    "visibilidad": 0.95
                },
                "Muneca": {
                    "x": 0.59,
                    "y": 0.58,
                    "z": 0.01,
                    "visibilidad": 0.93
                }
            },
            "angulo_codo": 92.4
        },
        "IZQUIERDO": {
            "articulaciones": {
                "Hombro": {
                    "x": 0.58,
                    "y": 0.30,
                    "z": -0.04,
                    "visibilidad": 0.97
                },
                "Codo": {
                    "x": 0.49,
                    "y": 0.45,
                    "z": -0.01,
                    "visibilidad": 0.96
                },
                "Muneca": {
                    "x": 0.40,
                    "y": 0.57,
                    "z": 0.02,
                    "visibilidad": 0.94
                    }
                },
            "angulo_codo": 87.6
            }
        },
    "tiempo": time.monotonic()
    }

    try:
        for numero in range(20):
            enviados = enviar_datos(sock, datos)

            print(
                f"Muestra {numero + 1}: "
                f"{enviados} bytes enviados"
            )

            time.sleep(0.1)

    finally:
        cerrar_socket(sock)


if __name__ == "__main__":
    main()