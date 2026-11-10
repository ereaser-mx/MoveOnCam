"""
Modulo que contiene la implementación del protocolo de comunicación UDP para enviar datos
en formato JSON a un servidor remoto.
"""


import json
import socket


IP_DESTINO = "127.0.0.1"
PUERTO_DESTINO = 5005


def crear_socket():
    """Crea el socket UDP que utilizaremos para enviar datos."""

    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM
    )

    return sock


def enviar_datos(sock, datos):
    """Convierte los datos a JSON y los envia por UDP."""

    mensaje = json.dumps(datos).encode("utf-8")

    bytes_enviados = sock.sendto(
        mensaje,
        (IP_DESTINO, PUERTO_DESTINO)
    )

    return bytes_enviados


def cerrar_socket(sock):
    """Cierra el socket cuando terminan las pruebas."""

    sock.close()