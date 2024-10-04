import cv2
import pyfirmata

# Load the face cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize video capture
cap = cv2.VideoCapture(0)

# Define pin numbers
D2 = 13
D3 = 12

# Get the port input from the user
port = input("Enter port (e.g., 3 for COM3): ")
com = "COM" + port
print(com)

# Set up the Arduino board
board = pyfirmata.Arduino(com)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Failed to capture image")
        break

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    # Check if faces are detected
    if len(faces) > 0:
        board.digital[D2].write(1)
        board.digital[D3].write(0)
        # Draw rectangles around faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    else: 

            # If no faces are detected, turn off the light connected to D2 and turn on the light connected to D3
        board.digital[D2].write(0)
        board.digital[D3].write(1)

    # Display the resulting frameq
    cv2.imshow('Face Detection', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break

# When everything is done, release the capture and destroy windows
cap.release()
cv2.destroyAllWindows()

# Reset the Arduino board pins to low state
board.digital[D2].write(0)
board.digital[D3].write(0)
board.exit()