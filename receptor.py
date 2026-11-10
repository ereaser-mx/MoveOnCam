import json
import socket


IP_LOCAL = "127.0.0.1"
PUERTO_LOCAL = 5005


sock = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM
)

sock.bind((IP_LOCAL, PUERTO_LOCAL))

print("Receptor UDP iniciado.")
print(f"Esperando datos en {IP_LOCAL}:{PUERTO_LOCAL}")

try:
    while True:
        mensaje, direccion = sock.recvfrom(65535)

        datos = json.loads(
            mensaje.decode("utf-8")
        )

        print("\nMensaje recibido:")
        print(json.dumps(
            datos,
            indent=2,
            ensure_ascii=False
        ))

except KeyboardInterrupt:
    print("\nCerrando receptor.")

finally:
    sock.close()
