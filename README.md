# MoveOnCam – Comunicación UDP

## Descripción
Este módulo permite enviar mediante el protocolo UDP los datos de las articulaciones de ambos brazos detectados por la cámara. Los datos incluyen coordenadas, visibilidad y ángulo del codo.

La información se convierte a formato JSON antes de enviarse.

## Software usado
- Python 3.11.
- Cámara web.
- Las librerías indicadas en `requirements.txt`.

## 1. Instalar dependencias (solo de ser necesario, si ya las tiene pasar a probar la comunicación)

Abre una terminal en la carpeta del proyecto y ejecuta:

py -3.11 -m pip install -r requirements.txt


## 2. Probar la comunicación UDP

Abre dos terminales en la carpeta del proyecto.

**Terminal 1 – Iniciar el receptor:**

py -3.11 receptor.py


**Terminal 2 – Enviar datos de prueba:**

py -3.11 prueba_protocol.py


El receptor debe mostrar los mensajes recibidos.


## 3. Ejecutar la detección con la cámara

Deja el receptor ejecutándose en la primera terminal. En la segunda, ejecuta:


py -3.11 vision.py


Se abrirá la cámara y se mostrarán las articulaciones detectadas y los ángulos de los codos. Los datos se enviarán al receptor aproximadamente cada 0.5 segundos cuando se detecte una persona.

Para cerrar la ventana de la cámara, presiona la tecla `q`.

## Configuración de comunicación

En `protocol.py` se configuran estos valores:

- `IP_DESTINO = "127.0.0.1"`: dirección local del equipo que recibe los datos.
- `PUERTO_DESTINO = 5005`: puerto UDP al que se envían los mensajes.

El archivo `receptor.py` debe utilizar la misma dirección y el mismo puerto para recibir los mensajes.

**Importante:** esta configuración está preparada para ejecutar el emisor y el receptor en la misma computadora.
