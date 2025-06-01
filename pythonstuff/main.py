import os
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

output_path=r'C:\Users\Ant\Documents\igmcq\output_images'
question_path=r"C:\Users\Ant\Documents\igmcq\questions"

def crop_questions(image_path, output_dir="questions_output"):
    image = Image.open(image_path)
    width, height = image.size
    ignore_margin = 400
    padding_top = 20

    base_name = os.path.splitext(os.path.basename(image_path))[0]

    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

    number_pattern = re.compile(r'^\d+\.?$')  # matches "1" or "1."

    left_limit = width * 0.15

    print("Scanning for left-aligned numbers (excluding margins)...")

    question_positions = []

    for i, word in enumerate(data["text"]):
        word_clean = word.strip()
        if number_pattern.match(word_clean):
            question_num_str = word_clean.rstrip('.')  # Remove trailing dot if present
            if question_num_str.isdigit():
                question_num = int(question_num_str)
                if 1 <= question_num <= 40:  # Only keep question numbers 1 to 40
                    x = data["left"][i]
                    y = data["top"][i]
                    if x <= left_limit and ignore_margin <= y <= (height - ignore_margin):
                        print(f"Found possible question number '{question_num}' at x={x}, y={y}")
                        question_positions.append((question_num, y))

    # Sort and clean based on vertical distance
    question_positions.sort(key=lambda x: x[1])
    cleaned_positions = []
    min_distance = 20

    for qnum, y in question_positions:
        if not cleaned_positions or abs(y - cleaned_positions[-1][1]) > min_distance:
            cleaned_positions.append((qnum, y))

    if not cleaned_positions:
        print("No question numbers detected.")
        return

    os.makedirs(output_dir, exist_ok=True)

    print(f"\nCropping {len(cleaned_positions)} questions...\n")

    for i in range(len(cleaned_positions)):
        question_num, y_start_raw = cleaned_positions[i]
        y_start = max(y_start_raw - padding_top, 0)

        if i + 1 < len(cleaned_positions):
            y_end = cleaned_positions[i + 1][1]
        else:
            y_end = height

        if y_end < y_start:
            print(f"Warning: y_end ({y_end}) < y_start ({y_start}), adjusting y_end.")
            y_end = y_start + 10

        print(f"Cropping question {question_num}: from y={y_start} to y={y_end}")

        cropped = image.crop((0, y_start, width, y_end))
        output_filename = f"{base_name}_question_{question_num}.jpg"
        output_path = os.path.join(output_dir, output_filename)
        cropped.save(output_path)
        print(f"Saved: {output_path}")

    print("\nDone!")

def pdf_to_images(pdf_path, output_folder=None, dpi=500, poppler_path=r"C:\poppler-24.08.0\Library\bin"):
    # Set default output folder if not provided
    if output_folder is None:
        output_folder = os.path.join(os.path.dirname(pdf_path), "output_images")

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Extract base filename without extension
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]

    # Convert PDF to images
    pages = convert_from_path(pdf_path, dpi, poppler_path=poppler_path)

    # Save pages as JPEG images in output folder
    for i, page in enumerate(pages):
        save_path = os.path.join(output_folder, f'{base_name}_page{i}.jpg')
        page.save(save_path, 'JPEG')
        print(f'Saved page {i} to {save_path}')

def all_crop(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            crop_questions(file_path)

def all_pdf(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            pdf_to_images(file_path, output_path)


all_pdf(question_path)

all_crop(output_path)