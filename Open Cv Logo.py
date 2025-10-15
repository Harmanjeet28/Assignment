import cv2
import numpy as np

# Create a blank white image
height, width = 600, 600
img = np.ones((height, width, 3), dtype=np.uint8) * 255

# Define colors in BGR
red = (0, 0, 255)
green = (0, 255, 0)
blue = (255, 0, 0)
black = (0, 0, 0)

# Center points for the three circles
center_red = (300, 150)
center_green = (150, 450)
center_blue = (450, 450)
radius_outer = 100
radius_inner = 40
thickness = -1  # filled

# Draw the outer circles
cv2.circle(img, center_red, radius_outer, red, thickness)
cv2.circle(img, center_green, radius_outer, green, thickness)
cv2.circle(img, center_blue, radius_outer, blue, thickness)

# Draw the inner "cut-out" circles (white)
cv2.circle(img, center_red, radius_inner, (255, 255, 255), thickness)
cv2.circle(img, center_green, radius_inner, (255, 255, 255), thickness)
cv2.circle(img, center_blue, radius_inner, (255, 255, 255), thickness)

# Draw connecting triangles (approximation)
points = np.array([center_red, center_green, center_blue])
cv2.drawContours(img, [points], 0, (255, 255, 255), thickness=-1)

# Add "OpenCV" text
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img, "OpenCV", (150, 580), font, 2, black, 5, cv2.LINE_AA)

# Show and save image
cv2.imshow("OpenCV Logo", img)
cv2.imwrite("opencv_logo_generated.png", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
