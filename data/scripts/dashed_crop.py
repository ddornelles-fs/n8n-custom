import fitz  # PyMuPDF
import cv2
import numpy as np
import os
import sys

def count_segments(line, min_gap=3):
    binary_line = (line > 0).astype(np.uint8)
    segments = 0
    in_segment = False
    for value in binary_line:
        if value and not in_segment:
            segments += 1
            in_segment = True
        elif not value:
            in_segment = False
    return segments

def detect_dashed_boxes(image, min_width=100, min_height=100, max_density=6.0, min_segments=2):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    edges = cv2.Canny(blur, 30, 100)

    # Save edge image for debug
    cv2.imwrite("/mnt/data/debug_edges.jpg", edges)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(f"[DEBUG] Found {len(contours)} contours")
    boxes = []

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.03 * cv2.arcLength(cnt, True), True)
        if len(approx) == 4 and cv2.contourArea(cnt) > 500:
            x, y, w, h = cv2.boundingRect(cnt)
            if w < min_width or h < min_height:
                continue

            # Mask edges on contour
            mask = np.zeros_like(gray)
            cv2.drawContours(mask, [cnt], -1, 255, 2)
            edge_pixels = cv2.bitwise_and(edges, mask)
            non_zero_count = cv2.countNonZero(edge_pixels)

            arc_length = cv2.arcLength(cnt, True)
            dashiness_ratio = non_zero_count / arc_length if arc_length > 0 else 999

            top_row = edges[y, x:x + w]
            segment_count = count_segments(top_row)

            print(f"[DEBUG] Box {x},{y},{w},{h} | Dashiness: {dashiness_ratio:.2f} | Segments: {segment_count}")

            if dashiness_ratio < max_density and segment_count >= min_segments:
                boxes.append((x, y, x + w, y + h))

    # Draw all contours for debug
    debug_img = image.copy()
    cv2.drawContours(debug_img, contours, -1, (0, 255, 0), 2)
    cv2.imwrite("/mnt/data/debug_contours.jpg", debug_img)

    # Sort boxes top to bottom, then left to right
    boxes.sort(key=lambda b: (b[1], b[0]))
    print(f"[DEBUG] Total dashed boxes detected: {len(boxes)}")
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
    print(f"[DEBUG] Processing PDF: {pdf_path}")
    os.makedirs(output_folder, exist_ok=True)

    if not os.path.exists(pdf_path):
        print(f"[ERROR] File not found: {pdf_path}")
        sys.exit(1)

    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"[ERROR] Failed to open PDF: {e}")
        sys.exit(1)

    print(f"[DEBUG] Total pages: {len(doc)}")
    count = 0

    for i, page in enumerate(doc):
        print(f"[DEBUG] Processing page {i}")
        image = convert_page_to_image(page)
        boxes = detect_dashed_boxes(image)

        for j, (x0, y0, x1, y1) in enumerate(boxes):
            cropped = image[y0:y1, x0:x1]
            cropped = resize_for_thermal(cropped)
            out_path = os.path.join(output_folder, f"page{i}_crop{j}.jpg")
            cv2.imwrite(out_path, cropped)
            print(f"[DEBUG] Saved {out_path}")
            count += 1

    print(f"[INFO] Total crops saved: {count}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python dashed_crop.py input.pdf output_folder")
        sys.exit(1)

    input_pdf = sys.argv[1]
    output_dir = sys.argv[2]
    process_pdf(input_pdf, output_dir)
