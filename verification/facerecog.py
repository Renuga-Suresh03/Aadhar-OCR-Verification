#assign to swarna

#open camera
#capture
#check if faces match
#if not del file and terimante
#if correct print aadhar validated


#working and deleting if not matched
'''import cv2
import numpy as np
import face_recognition
import os
import sys  # To exit the script if face doesn't match

# Aadhaar image from the "secret" folder (relative path)
AADHAAR_IMG_PATH = os.path.join(os.path.dirname(os.getcwd()), "secret", "Swarna Latha.V_Aadhaar_Card.png")
LIVE_IMG_PATH = "live.jpg"  # Captured image

def capture_live_image():
    """Opens webcam, allows user to take a photo, and saves it as 'live.jpg'."""
    cam = cv2.VideoCapture(0)  # Open webcam
    if not cam.isOpened():
        print("❌ Error: Could not open webcam.")
        return False

    print("📷 Press 's' to capture and save the image, 'q' to quit.")
    
    while True:
        ret, frame = cam.read()
        if not ret:
            print("❌ Failed to capture image")
            break

        cv2.imshow("Capture Image - Press 's' to Save, 'q' to Quit", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):  # Save image if user presses 's'
            cv2.imwrite(LIVE_IMG_PATH, frame)
            print("✅ Live image saved successfully!")
            break
        elif key == ord('q'):  # Quit without saving
            print("❌ Image capture canceled.")
            cam.release()
            cv2.destroyAllWindows()
            return False

    cam.release()
    cv2.destroyAllWindows()
    return True

def compare_faces():
    """Compares Aadhaar image with live image. Deletes 'live.jpg' and exits if no match."""
    if not os.path.exists(AADHAAR_IMG_PATH):
        print(f"❌ Error: Aadhaar image not found at {AADHAAR_IMG_PATH}!")
        return
    if not os.path.exists(LIVE_IMG_PATH):
        print("❌ Error: Live image not found!")
        return

    # Load images
    aadhaar_img = face_recognition.load_image_file(AADHAAR_IMG_PATH)
    live_img = face_recognition.load_image_file(LIVE_IMG_PATH)

    # Get face encodings
    aadhaar_encoding = face_recognition.face_encodings(aadhaar_img)
    live_encoding = face_recognition.face_encodings(live_img)

    # Check if faces are detected
    if not aadhaar_encoding:
        print("❌ Error: No face detected in Aadhaar image!")
        return
    if not live_encoding:
        print("❌ Error: No face detected in Live image!")
        return

    # Compare faces
    match = face_recognition.compare_faces([aadhaar_encoding[0]], live_encoding[0], tolerance=0.5)

    if match[0]:
        print("✅ Match: Faces are the same!")
    else:
        print("❌ Not Match: Faces are different. Deleting live image...")
        os.remove(LIVE_IMG_PATH)  # Delete live image
        sys.exit("🚨 Terminating script due to face mismatch.")  # Exit program

if __name__ == "__main__":
    print("📷 Open webcam and capture image.")
    if capture_live_image():
        print("🔍 Comparing faces...")
        compare_faces()
'''

#facenet+MTCNN
'''import cv2
import torch
import numpy as np
import os
import sys
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image

# Aadhaar image from the "secret" folder (relative path)
AADHAAR_IMG_PATH = os.path.join(os.path.dirname(os.getcwd()), "secret", "Swarna Latha.V_Aadhaar_Card.png")
LIVE_IMG_PATH = "live.jpg"  # Captured image

# Initialize MTCNN for face detection and FaceNet for embedding extraction
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
mtcnn = MTCNN(keep_all=False, device=device)
resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)

def capture_live_image():
    """Opens webcam, allows user to take a photo, and saves it as 'live.jpg'."""
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("❌ Error: Could not open webcam.")
        return False

    print("📷 Press 's' to capture and save the image, 'q' to quit.")
    
    while True:
        ret, frame = cam.read()
        if not ret:
            print("❌ Failed to capture image")
            break

        cv2.imshow("Capture Image - Press 's' to Save, 'q' to Quit", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):  # Save image
            cv2.imwrite(LIVE_IMG_PATH, frame)
            print("✅ Live image saved successfully!")
            break
        elif key == ord('q'):  # Quit without saving
            print("❌ Image capture canceled.")
            cam.release()
            cv2.destroyAllWindows()
            return False

    cam.release()
    cv2.destroyAllWindows()
    return True

def get_face_embedding(image_path):
    """Extracts FaceNet embedding from an image."""
    img = Image.open(image_path).convert("RGB")  # Convert image to RGB format
    face = mtcnn(img)  # Detect and crop face
    if face is None:
        return None
    face = face.unsqueeze(0).to(device)  # Convert to tensor
    embedding = resnet(face)  # Generate face embedding
    return embedding.detach().cpu().numpy()

def compare_faces():
    """Compares Aadhaar image with live image using FaceNet embeddings."""
    if not os.path.exists(AADHAAR_IMG_PATH):
        print(f"❌ Error: Aadhaar image not found at {AADHAAR_IMG_PATH}!")
        return
    if not os.path.exists(LIVE_IMG_PATH):
        print("❌ Error: Live image not found!")
        return

    # Get face embeddings
    aadhaar_embedding = get_face_embedding(AADHAAR_IMG_PATH)
    live_embedding = get_face_embedding(LIVE_IMG_PATH)

    if aadhaar_embedding is None:
        print("❌ Error: No face detected in Aadhaar image!")
        return
    if live_embedding is None:
        print("❌ Error: No face detected in Live image!")
        return

    # Compute Euclidean distance between embeddings
    distance = np.linalg.norm(aadhaar_embedding - live_embedding)

    # Threshold (Lower = Stricter Match)
    THRESHOLD = 0.8
    if distance < THRESHOLD:
        print(f"✅ Match: Faces are the same! (Distance: {distance:.3f})")
    else:
        print(f"❌ Not Match: Faces are different! (Distance: {distance:.3f})")
        os.remove(LIVE_IMG_PATH)  # Delete live image
        sys.exit("🚨 Terminating script due to face mismatch.")  # Exit program

if __name__ == "__main__":
    print("📷 Open webcam and capture image.")
    if capture_live_image():
        print("🔍 Comparing faces...")
        compare_faces()
'''
#deleting images after checking
import cv2
import torch
import numpy as np
import os
import sys
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image

# Aadhaar image from the "secret" folder (relative path)
AADHAAR_IMG_PATH = os.path.join(os.path.dirname(os.getcwd()), "secret", r"C:\Projects\Aadhar-OCR-Verification\sampledata\generated_aadhars\Renu.png")

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

def compare_faces(live_frame):
    """Compares Aadhaar image with live image using FaceNet embeddings."""
    if not os.path.exists(AADHAAR_IMG_PATH):
        print(f"❌ Error: Aadhaar image not found at {AADHAAR_IMG_PATH}!")
        return

    # Get face embeddings
    aadhaar_embedding = get_face_embedding(AADHAAR_IMG_PATH)
    live_embedding = get_face_embedding(live_frame)

    if aadhaar_embedding is None:
        print("❌ Error: No face detected in Aadhaar image!")
        return
    if live_embedding is None:
        print("❌ Error: No face detected in Live image!")
        return

    # Compute Euclidean distance between embeddings
    distance = np.linalg.norm(aadhaar_embedding - live_embedding)

    # Threshold (Lower = Stricter Match)
    THRESHOLD = 0.8
    if distance < THRESHOLD:
        print(f"✅ Match: Faces are the same! (Distance: {distance:.3f})")
    else:
        print(f"❌ Not Match: Faces are different! (Distance: {distance:.3f})")
        sys.exit("🚨 Terminating script due to face mismatch.")  # Exit program

if __name__ == "__main__":
    print("📷 Open webcam and capture image.")
    live_frame = capture_live_image()
    if live_frame is not None:
        print("🔍 Comparing faces...")
        compare_faces(live_frame)
