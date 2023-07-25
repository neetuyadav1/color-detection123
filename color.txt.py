import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

# Function to detect color
def detect_color(frame):
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define lower and upper boundaries for the color you want to detect
    lower_bound = np.array([0, 120, 70])
    upper_bound = np.array([10, 255, 255])

    # Create a mask using the boundaries
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # Find contours of the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        # Find the largest contour
        largest_contour = max(contours, key=cv2.contourArea)
        # Find the centroid of the contour
        M = cv2.moments(largest_contour)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        # Get the color at the centroid
        color = frame[cy, cx]
        return color
    else:
        return None

# Function to update the video frame
def update_frame():
    ret, frame = cap.read()
    if ret:
        color = detect_color(frame)
        if color is not None:
            b, g, r = color
            color_name = get_color_name(b, g, r)
            color_label.config(text="Detected Color: " + color_name)
        else:
            color_label.config(text="Detected Color: None")

        # Convert the frame to PIL format
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(img)

        # Update the video frame
        video_label.img = img
        video_label.config(image=img)
    else:
        color_label.config(text="No Frame")

    # Repeat after 10 milliseconds
    video_label.after(10, update_frame)

# Function to get the color name based on BGR values
def get_color_name(b, g, r):
    colors = {
        (0, 0, 255): "Red",
        (0, 255, 0): "Green",
        (255, 0, 0): "Blue"
        # Add more colors as needed
    }
    closest_color = min(colors, key=lambda x: np.linalg.norm(np.array(x) - np.array([b, g, r])))
    return colors[closest_color]

# Create a Tkinter window
window = tk.Tk()
window.title("Color Detection")

# Create a label for video frame
video_label = tk.Label(window)
video_label.pack()

# Create a label for color display
color_label = tk.Label(window, font=("Arial", 16), pady=10)
color_label.pack()

# Open the camera
cap = cv2.VideoCapture(0)

# Start updating the video frame
update_frame()

# Run the Tkinter event loop
window.mainloop()

# Release the camera and destroy the window
cap.release()
cv2.destroyAllWindows()