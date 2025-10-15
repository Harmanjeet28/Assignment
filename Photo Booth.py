import cv2
import numpy as np
import os

# ----------------------------- Helper Functions ----------------------------- #
def overlay_text(img, text_list):
    """Overlay instructions on the image"""
    overlay = img.copy()
    y0, dy = 30, 30
    for i, text in enumerate(text_list):
        y = y0 + i*dy
        cv2.putText(overlay, text, (10, y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (0,255,255), 2, cv2.LINE_AA)
    return overlay

def apply_brightness_contrast(image, brightness=0, contrast=0):
    alpha = contrast / 127 + 1
    beta = brightness
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

def apply_padding(image, pad=50, border_type='constant'):
    border_dict = {"constant": cv2.BORDER_CONSTANT,
                   "reflect": cv2.BORDER_REFLECT,
                   "replicate": cv2.BORDER_REPLICATE,
                   "reflect_101": cv2.BORDER_REFLECT_101}
    border = border_dict.get(border_type, cv2.BORDER_CONSTANT)
    if border_type == 'constant':
        return cv2.copyMakeBorder(image, pad, pad, pad, pad, border, value=[0,0,0])
    else:
        return cv2.copyMakeBorder(image, pad, pad, pad, pad, border)

def apply_threshold(image, type='binary'):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if type=='binary':
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    else:
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
    return cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

def blend_images(img1, img2, alpha=0.5):
    img2_resized = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
    return cv2.addWeighted(img1, alpha, img2_resized, 1-alpha, 0)

# ----------------------------- Main App ----------------------------- #
def photo_booth_gui(image_path):
    if not os.path.exists(image_path):
        print("File not found!")
        return

    original = cv2.imread(image_path)
    current = original.copy()
    history = []
    history_log = []

    instructions = [
        "Photo Booth Menu (Press key):",
        "b: Brightness/Contrast",
        "p: Padding",
        "t: Thresholding",
        "l: Blend images",
        "u: Undo",
        "s: Save & Exit"
    ]

    while True:
        display = overlay_text(current.copy(), instructions)
        cv2.imshow("Photo Booth", display)
        key = cv2.waitKey(0) & 0xFF

        if key == ord('b'):
            history.append(current.copy())
            brightness = int(input("Brightness (-127 to 127): "))
            contrast = int(input("Contrast (-127 to 127): "))
            current = apply_brightness_contrast(current, brightness, contrast)
            history_log.append(f"Brightness {brightness}, Contrast {contrast}")

        elif key == ord('p'):
            history.append(current.copy())
            pad = int(input("Padding size (px): "))
            btype = input("Border type (constant/reflect/replicate): ")
            current = apply_padding(current, pad, btype)
            history_log.append(f"Padded {pad}px with {btype}")

        elif key == ord('t'):
            history.append(current.copy())
            ttype = input("Threshold type (binary/binary_inv): ")
            current = apply_threshold(current, ttype)
            history_log.append(f"Threshold {ttype}")

        elif key == ord('l'):
            history.append(current.copy())
            path2 = input("Path for second image: ")
            if not os.path.exists(path2):
                print("File not found!")
                continue
            alpha = float(input("Alpha (0-1): "))
            img2 = cv2.imread(path2)
            current = blend_images(current, img2, alpha)
            history_log.append(f"Blended with {path2} alpha {alpha}")

        elif key == ord('u'):
            if history:
                current = history.pop()
                history_log.append("Undo applied")
                print("Undo successful")
            else:
                print("Nothing to undo")

        elif key == ord('s'):
            filename = input("Enter filename to save (e.g., output.jpg): ")
            cv2.imwrite(filename, current)
            print(f"Image saved as {filename}")
            print("\nHistory log:")
            for i, h in enumerate(history_log):
                print(f"{i+1}. {h}")
            break

        elif key == 27:  # ESC to exit without saving
            print("Exited without saving.")
            break

    cv2.destroyAllWindows()

# ----------------------------- Run ----------------------------- #
if __name__ == "__main__":
    path = input("Enter path to image: ")
    photo_booth_gui(path)
