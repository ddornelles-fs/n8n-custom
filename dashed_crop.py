import fitz  # PyMuPDF
import cv2
import numpy as np
import os
import sys

def detect_dashed_boxes(image):
    """Detect dashed rectangle contours using OpenCV edge + contour logic."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    edges = cv2.Canny(blur, 30, 100)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    boxes = []

    for cnt in c
