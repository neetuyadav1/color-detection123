import cv2

def main():
    # Open the default camera (usually the primary camera, 0 index)
    camera = cv2.VideoCapture(0)

    # Check if the camera was successfully opened
    if not camera.isOpened():
        print("Error: Unable to access the camera.")
        return

    # Set the window name for displaying the camera feed
    window_name = "Camera Feed"

    while True:
        # Read a frame from the camera
        ret, frame = camera.read()

        # If the frame was not successfully read, break the loop
        if not ret:
            break

        # Display the frame in a window
        cv2.imshow(window_name, frame)

        # Exit the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close the window
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
