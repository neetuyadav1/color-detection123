import cv2
import numpy as np
import tkinter as tk
from PIL import ImageTk, Image
def detect_colors(image, color_ranges):
    # Convert image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    detected_colors = []
    
    for color_name, lower_range, upper_range in color_ranges:
        # Create a mask for the color range
        mask = cv2.inRange(hsv_image, lower_range, upper_range)
        
        # Apply the mask to the original image
        result = cv2.bitwise_and(image, image, mask=mask)
        
        # Check if any pixels of the color range are detected
        if np.any(result):
            detected_colors.append((color_name, result))
    
    return detected_colors

# Define s
color_ranges = [
    ('Red', np.array([0, 120, 70]), np.array([10, 255, 255])),
    ('Green', np.array([35, 120, 70]), np.array([130, 255, 255])),
    ('Blue', np.array([100, 120, 70]), np.array([85, 255, 255]))
]

# Create GUI window
window = tk.Tk()
window.title('Color Detection')
window.geometry('800x600')

# Create a label to display the processed image
label_image = tk.Label(window)
label_image.pack()

# Open the webcam
cap = cv2.VideoCapture(0)

def update_frame():
    # Read the current frame from the webcam
    ret, frame = cap.read()
    
    # Flip the frame horizontally for mirror effect
    frame = cv2.flip(frame, 1)
    
    # Detect colors in the frame
    detected_colors = detect_colors(frame, color_ranges)
    
    # Display the detected colors
    for color_name, result in detected_colors:
        # Convert the result image to PIL format for display
        result_pil = Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
        result_tk = ImageTk.PhotoImage(result_pil)
        
        # Display the result image in the GUI window
        label_image.configure(image=result_tk)
        label_image.image = result_tk
        
    # Update the frame continuously
    window.after(10, update_frame)

# Start updating the frame
update_frame()

# Run the GUI main loop
window.mainloop()

# Release the webcam
cap.release()
