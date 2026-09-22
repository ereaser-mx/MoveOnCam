import cv2
import mediapipe as mp

# Inicializar MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    enable_segmentation=False,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Cámara
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    # Voltear imagen como espejo
    frame = cv2.flip(frame, 1)

    # Convertir BGR a RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Procesar imagen
    resultados = pose.process(rgb)

    if resultados.pose_landmarks:

        landmarks = resultados.pose_landmarks.landmark

        # Landmarks del brazo derecho
        hombro = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        codo = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
        muneca = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]

        alto, ancho, _ = frame.shape

        # Convertir coordenadas normalizadas a píxeles
        hombro_px = (
            int(hombro.x * ancho),
            int(hombro.y * alto)
        )

        codo_px = (
            int(codo.x * ancho),
            int(codo.y * alto)
        )

        muneca_px = (
            int(muneca.x * ancho),
            int(muneca.y * alto)
        )

        # Dibujar puntos
        cv2.circle(frame, hombro_px, 10, (0, 255, 0), -1)
        cv2.circle(frame, codo_px, 10, (255, 0, 0), -1)
        cv2.circle(frame, muneca_px, 10, (0, 0, 255), -1)

        # Dibujar líneas entre articulaciones
        cv2.line(frame, hombro_px, codo_px, (255, 255, 255), 3)
        cv2.line(frame, codo_px, muneca_px, (255, 255, 255), 3)

        # Mostrar nombres
        cv2.putText(
            frame,
            "Hombro",
            hombro_px,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            "Codo",
            codo_px,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 0, 0),
            2
        )

        cv2.putText(
            frame,
            "Muneca",
            muneca_px,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 255),
            2
        )

        # Mostrar coordenadas normalizadas en consola
        print("HOMBRO:")
        print("X:", round(hombro.x, 3))
        print("Y:", round(hombro.y, 3))
        print("Z:", round(hombro.z, 3))

        print("CODO:")
        print("X:", round(codo.x, 3))
        print("Y:", round(codo.y, 3))
        print("Z:", round(codo.z, 3))

        print("MUNECA:")
        print("X:", round(muneca.x, 3))
        print("Y:", round(muneca.y, 3))
        print("Z:", round(muneca.z, 3))

        print("------------------------")

    cv2.imshow("Hombro - Codo - Muneca", frame)

    # Presiona Q para salir
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
pose.close()
