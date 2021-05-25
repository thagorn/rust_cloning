import cv2
import pyautogui
import pytesseract
from PIL import Image, ImageGrab, ImageOps
import numpy as np
import sys
from getch import Getch

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
SAVE_LOCATION = r'C:\Users\Andy\Downloads\temp.png'
CLONES_TSV = 'clones.tsv'

def get_BBox(point):
    return (point.x -50, point.y -25, point.x +50, point.y +25)

def convert_image(image):
    image = image.convert('RGB')
    data = np.array(image)
    red, green, blue = data.T
    red_areas = (red >= 150) &  (blue <= 100) & (green <= 100)
    green_areas = (red <= 150) & (blue <= 80) & (green >= 100)
    data[:,:,:3][red_areas.T] = (0, 0, 0)
    data[:,:,:3][green_areas.T] = (0, 0, 0)
    red, green, blue = data.T
    other = (red > 0) & (blue > 0) & (green > 0)
    data[:,:,:3][other.T] = (255, 255, 255)
    return cv2.cvtColor(data, cv2.COLOR_RGB2BGR)

def add_to_file(text):
    with open(CLONES_TSV, 'a') as clones:
        clones.write(text + '\n')

def clear_file():
    with open(CLONES_TSV, 'w') as clones:
        clones.truncate()

def remove_noise(cv2_image):
    return cv2.medianBlur(cv2_image, 5)

def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

def erode(cv2_image):
    kernal = np.ones((5,5),np.uint8)
    return cv2.erode(cv2_image, kernal, iterations = 1)

def opening(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

def convert_back(image):
    return Image.fromarray(image)

def get_text_at_cursor():
    point = pyautogui.position()
    image = ImageGrab.grab(bbox=get_BBox(point))
    cv2_image = convert_image(image)
    return pytesseract.image_to_string(cv2_image, config='-c tessedit_char_whitelist=XYGHW').strip()

def test():
    point = pyautogui.position()
    image = ImageGrab.grab(bbox=get_BBox(point))
    img = convert_image(image)
    print(img.shape)
    hImg, wImg, _ = img.shape
    text = pytesseract.image_to_string(img, config='-c tessedit_char_whitelist=XYGHW').strip()
    print(text)

    boxes = pytesseract.image_to_boxes(img, config='-c tessedit_char_whitelist=XYGHW')
    for b in boxes.splitlines():
        b = b.split(' ')
        x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
        cv2.rectangle(img, (x, hImg - y), (w, hImg - h), (0, 0, 255), 1)

    cv2.imshow('Result', img)
    cv2.waitKey(0)

def main():
    clear_file()
    clone_text = ""
    getch = Getch()
    while True:
        print
        print('(N)ext clone, (R)epeat same, (A)dd manually or (D)one:\n')
        value = getch()
        if value == b'\x03':
            sys.exit(0)
        value = value.decode("utf-8")
        if value.lower() == 'n':
            add_to_file(clone_text)
        elif value.lower() == 'a':
            good_value = False
            while not good_value:
                value = input('Type clone out:\n')
                if len(value) == 6:
                    add_to_file(value)
                    good_value = True
            continue
        elif value.lower() == 'd':
            sys.exit(0)
        elif value.lower() != 'r':
            continue
        clone_text = get_text_at_cursor()
        print(clone_text)

if __name__ == '__main__':
    main()
