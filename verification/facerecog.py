import cv2
import torch
import numpy as np
import os
import sys
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image

# Initialize MTCNN for face detection and FaceNet for embedding extraction
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
mtcnn = MTCNN(keep_all=False, device=device)
resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)

def capture_live_image():
    """Opens webcam, captures an image, and returns the frame."""
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("❌ Error: Could not open webcam.")
        return None

    print("📷 Press 's' to capture an image, 'q' to quit.")
    
    while True:
        ret, frame = cam.read()
        if not ret:
            print("❌ Failed to capture image")
            break

        cv2.imshow("Capture Image - Press 's' to Capture, 'q' to Quit", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):  # Capture image
            print("✅ Image captured successfully!")
            cam.release()
            cv2.destroyAllWindows()
            return frame  # Return the captured frame
        elif key == ord('q'):  # Quit without capturing
            print("❌ Image capture canceled.")
            cam.release()
            cv2.destroyAllWindows()
            return None

def get_face_embedding(image):
    """Extracts FaceNet embedding from an image (can be file path or OpenCV frame)."""
    if isinstance(image, str):  # If it's a file path
        img = Image.open(image).convert("RGB")
    else:  # If it's an OpenCV frame
        img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    face = mtcnn(img)  # Detect and crop face
    if face is None:
        return None
    face = face.unsqueeze(0).to(device)  # Convert to tensor
    embedding = resnet(face)  # Generate face embedding
    return embedding.detach().cpu().numpy()

def compare_faces(live_frame, aadhaar_path):
    """Compares Aadhaar image with live image using FaceNet embeddings."""
    if not os.path.exists(aadhaar_path):
        print(f"❌ Error: Aadhaar image not found at {aadhaar_path}!")
        return False

    # Get face embeddings
    aadhaar_embedding = get_face_embedding(aadhaar_path)
    live_embedding = get_face_embedding(live_frame)

    if aadhaar_embedding is None:
        print("❌ Error: No face detected in Aadhaar image!")
        return False
    if live_embedding is None:
        print("❌ Error: No face detected in Live image!")
        return False

    # Compute Euclidean distance between embeddings
    distance = np.linalg.norm(aadhaar_embedding - live_embedding)

    # Threshold (Lower = Stricter Match)
    THRESHOLD = 0.8
    if distance < THRESHOLD:
        print(f"✅ Match: Faces are the same! (Distance: {distance:.3f})")
        return True
    else:
        print(f"❌ Not Match: Faces are different! (Distance: {distance:.3f})")
        return False
