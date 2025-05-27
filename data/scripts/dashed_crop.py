import fitz  # PyMuPDF
import cv2
import numpy as np
import os
import sys

def detect_dashed_boxes(image):
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
    return boxes

def convert_page_to_image(page, zoom=3):
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    if img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    return img

def resize_for_thermal(cropped, target_width=384):
    h, w = cropped.shape[:2]
    if w == target_width:
        return cropped
    new_height = int(h * (target_width / w))
    return cv2.resize(cropped, (target_width, new_height), interpolation=cv2.INTER_AREA)

def process_pdf(pdf_path, output_folder):
    if not os.path.exists(pdf_path):
        print(f"❌ Input file not found: {pdf_path}")
        sys.exit(1)
    os.makedirs(output_folder, exist_ok=True)
    doc = fitz.open(pdf_path)
    count = 0
    for i, page in enumerate(doc):
        image = convert_page_to_image(page)
        boxes = detect_dashed_boxes(image)
        for j, (x0, y0, x1, y1) in enumerate(boxes):
