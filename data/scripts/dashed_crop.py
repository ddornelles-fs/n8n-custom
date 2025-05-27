import fitz  # PyMuPDF
import cv2
import numpy as np
import os
import sys

def detect_dashed_boxes(image):
    print("[DEBUG] Running dashed box detection")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    edges = cv2.Canny(blur, 30, 100)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    boxes = []
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.03 * cv2.arcLength(cnt, True), True)
        if len(approx) == 4 and cv2.contourArea(cnt) > 1000:
            x, y, w, h = cv2.boundingRect(cnt)
            boxes.append((x, y, x + w, y + h))
    print(f"[DEBUG] Found {len(boxes)} boxes")
    return boxes

def convert_page_to_image(page, zoom=3):
    print("[DEBUG] Converting page to image")
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    if img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    return img

def resize_for_thermal(cropped, target_width=384):
    h, w = cropped.shape[:2]
    if w == targe
