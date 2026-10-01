import cv2
import mediapipe as mp
import math
import time


mp_pose = mp.solutions.pose

BRAZOS = {
    "DERECHO": {
        "color": (0, 255, 0),
        "puntos": {
            "Hombro": mp_pose.PoseLandmark.RIGHT_SHOULDER,
            "Codo": mp_pose.PoseLandmark.RIGHT_ELBOW,
            "Muneca": mp_pose.PoseLandmark.RIGHT_WRIST
        }
    },
    "IZQUIERDO": {
        "color": (255, 0, 0),
        "puntos": {
            "Hombro": mp_pose.PoseLandmark.LEFT_SHOULDER,
            "Codo": mp_pose.PoseLandmark.LEFT_ELBOW,
            "Muneca": mp_pose.PoseLandmark.LEFT_WRIST
        }
    }
}

VISIBILIDAD_MINIMA = 0.5
INTERVALO_CONSOLA = 0.5


def obtener_articulaciones(landmarks, lado):
    articulaciones = {}

    for nombre, indice in BRAZOS[lado]["puntos"].items():
        articulaciones[nombre] = landmarks[indice.value]

    return articulaciones


def convertir_a_pixeles(landmark, ancho, alto, espejo=False):
    x = landmark.x * (ancho - 1)
    y = landmark.y * (alto - 1)

    if espejo:
        x = (ancho - 1) - x

    return x, y


def calcular_angulo(a, b, c):
    """Calcula el ángulo en B formado por A-B-C."""

    vector_ba = (
        a[0] - b[0],
        a[1] - b[1]
    )

    vector_bc = (
        c[0] - b[0],
        c[1] - b[1]
    )

    longitud_ba = math.hypot(*vector_ba)
    longitud_bc = math.hypot(*vector_bc)

    if longitud_ba == 0 or longitud_bc == 0:
        return None

    producto_punto = (
        vector_ba[0] * vector_bc[0]
        + vector_ba[1] * vector_bc[1]
    )

    coseno = producto_punto / (longitud_ba * longitud_bc)
    coseno = max(-1.0, min(1.0, coseno))

    return math.degrees(math.acos(coseno))


def calcular_angulo_codo(articulaciones, ancho, alto):
    # Se necesitan los tres puntos visibles.
    if any(
        landmark.visibility < VISIBILIDAD_MINIMA
        for landmark in articulaciones.values()
    ):
        return None

    puntos = {
        nombre: convertir_a_pixeles(landmark, ancho, alto)
        for nombre, landmark in articulaciones.items()
    }

    return calcular_angulo(
        puntos["Hombro"],
        puntos["Codo"],
        puntos["Muneca"]
    )


def dibujar_brazo(frame, articulaciones, lado):
    alto, ancho = frame.shape[:2]
    color = BRAZOS[lado]["color"]
    puntos_visibles = {}

    for nombre, landmark in articulaciones.items():
        if landmark.visibility < VISIBILIDAD_MINIMA:
            continue

        x, y = convertir_a_pixeles(
            landmark,
            ancho,
            alto,
            espejo=True
        )

        posicion = (int(round(x)), int(round(y)))
        puntos_visibles[nombre] = posicion

        cv2.circle(frame, posicion, 7, color, -1)

        texto = (
            f"{nombre} {lado}: "
            f"({posicion[0]}, {posicion[1]})"
        )

        cv2.putText(
            frame,
            texto,
            (posicion[0] + 10, posicion[1] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            color,
            2
        )

    conexiones = [
        ("Hombro", "Codo"),
        ("Codo", "Muneca")
    ]

    for inicio, fin in conexiones:
        if inicio in puntos_visibles and fin in puntos_visibles:
            cv2.line(
                frame,
                puntos_visibles[inicio],
                puntos_visibles[fin],
                color,
                2
            )


def mostrar_angulo(frame, lado, apertura_codo, y):
    color = BRAZOS[lado]["color"]

    texto_angulo = (
        f"{apertura_codo:.1f} grados"
        if apertura_codo is not None
        else "No disponible"
    )

    cv2.putText(
        frame,
        f"Codo {lado}: {texto_angulo}",
        (10, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        color,
        2
    )


def imprimir_datos(lado, articulaciones, apertura_codo):
    print(f"\nBRAZO {lado}")

    for nombre, landmark in articulaciones.items():
        print(
            f"{nombre}: "
            f"X={landmark.x:.3f}, "
            f"Y={landmark.y:.3f}, "
            f"Z={landmark.z:.3f}, "
            f"Visibilidad={landmark.visibility:.2f}"
        )

    if apertura_codo is not None:
        print(f"Apertura del codo: {apertura_codo:.1f} grados")
    else:
        print("Apertura del codo: no disponible")


def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        cap.release()
        raise RuntimeError("No se pudo abrir la cámara")

    ultima_impresion = 0.0

    try:
        with mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            enable_segmentation=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        ) as pose:

            while cap.isOpened():
                ret, imagen_original = cap.read()

                if not ret:
                    break

                # Procesar la imagen sin voltear.
                rgb = cv2.cvtColor(
                    imagen_original,
                    cv2.COLOR_BGR2RGB
                )

                rgb.flags.writeable = False
                resultados = pose.process(rgb)

                # Mostrar la imagen como espejo.
                frame = cv2.flip(imagen_original, 1)
                alto, ancho = frame.shape[:2]

                ahora = time.monotonic()
                imprimir = (
                    ahora - ultima_impresion >= INTERVALO_CONSOLA
                )

                if resultados.pose_landmarks:
                    landmarks = resultados.pose_landmarks.landmark

                    for lado, posicion_y in [
                        ("DERECHO", 30),
                        ("IZQUIERDO", 65)
                    ]:
                        articulaciones = obtener_articulaciones(
                            landmarks,
                            lado
                        )

                        apertura_codo = calcular_angulo_codo(
                            articulaciones,
                            ancho,
                            alto
                        )

                        dibujar_brazo(
                            frame,
                            articulaciones,
                            lado
                        )

                        mostrar_angulo(
                            frame,
                            lado,
                            apertura_codo,
                            posicion_y
                        )

                        if imprimir:
                            imprimir_datos(
                                lado,
                                articulaciones,
                                apertura_codo
                            )

                    if imprimir:
                        print("-" * 60)
                        ultima_impresion = ahora

                else:
                    cv2.putText(
                        frame,
                        "No se detecta una persona",
                        (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 0, 255),
                        2
                    )

                cv2.imshow(
                    "Coordenadas y angulos de los codos",
                    frame
                )

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
