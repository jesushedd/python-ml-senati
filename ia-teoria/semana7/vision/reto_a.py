import cv2
import face_recognition
import numpy as np
import os
import time

# --- CARGAR CARAS CONOCIDAS ---
known_face_encodings = []
known_face_names = []

# Lista de archivos con imágenes conocidas
personas = {
    "richard.jpg": "Richard",
    "jose.jpg": "Jose"
}

# Cargar y codificar las caras conocidas
for archivo, nombre in personas.items():
    if not os.path.exists(archivo):
        print(f"⚠️ Imagen no encontrada: {archivo}")
        continue

    imagen = face_recognition.load_image_file(archivo)
    encoding = face_recognition.face_encodings(imagen)

    if len(encoding) == 0:
        print(f"❌ No se detectó rostro en {archivo}")
        continue

    known_face_encodings.append(encoding[0])
    known_face_names.append(nombre)
    print(f"✅ Rostro cargado: {nombre}")

if len(known_face_encodings) == 0:
    print("❌ No hay rostros conocidos cargados. Cerrando programa.")
    exit()

# --- INICIAR WEBCAM ---
video_capture = cv2.VideoCapture(0)
print("🎥 Webcam iniciada. Presioná 'q' para salir.")

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("❌ Error al acceder a la webcam.")
        break

    # Reducir tamaño del frame para acelerar el procesamiento
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Detectar rostros y codificarlos
    face_locations = face_recognition.face_locations(rgb_small_frame)
    print(len(face_locations))
    print('TIPO', type(face_locations), face_locations)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        name = "Desconocido"
        acceso = "❌ Acceso denegado"
        color = (0, 0, 255)  # Rojo

        # Comparar con rostros conocidos
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

        if len(face_distances) > 0:
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                acceso = "✔️ Acceso permitido"
                color = (0, 255, 0)  # Verde

        # Escalar coordenadas al frame original
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        print(top,right,bottom,left)

        # Dibujar rectángulo
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        # Mostrar nombre
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        # Mostrar estado de acceso
        cv2.putText(frame, acceso, (left, bottom + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    # Mostrar ventana
    cv2.imshow(" Control de Acceso", frame)

    # Salir con 'q'
    if cv2.waitKey(17) & 0xFF == ord('q'):
        print("Cerrando...")
        break

# --- LIBERAR RECURSOS ---
video_capture.release()
cv2.destroyAllWindows()
