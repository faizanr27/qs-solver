from flask import Flask, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
from helpers.ocr import extract_text_from_image
from helpers.solver import solve_questions
from helpers.file_utils import save_output_to_pdf
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
from flask_cors import CORS
from helpers.text_processing import extract_questions

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'

CORS(app)  # Enable CORS for all routes

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)


def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.
    - If the PDF has selectable text, it extracts text directly.
    - If the PDF contains images, it applies OCR to extract text.

    Returns:
        str: Extracted text from the PDF.
    """
    try:
        reader = PdfReader(pdf_path)
        extracted_text = ""

        # Extract text from all pages
        for page in reader.pages:
            if page.extract_text():
                extracted_text += page.extract_text() + "\n"

        # If the extracted text is empty, assume it's an image-based PDF and use OCR
        if not extracted_text.strip():
            images = convert_from_path(pdf_path)
            for i, image in enumerate(images):
                image_path = f"temp_page_{i}.jpg"
                image.save(image_path, "JPEG")
                extracted_text += extract_text_from_image(image_path) + "\n"
                os.remove(image_path)  # Cleanup temp images

        return extracted_text.strip()
    except Exception as e:
        return f"Error extracting text from PDF: {str(e)}"


@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Handles file uploads, extracts text, filters out non-question content,
    solves questions, and returns a downloadable solution file.
    """
    try:
        # ✅ Ensure a file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']

        # ✅ Check if the filename is empty
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # ✅ Secure filename to prevent directory traversal attacks
        filename = secure_filename(file.filename)

        # ✅ Define the full file path
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # ✅ Save file to uploads directory
        file.save(file_path)

        # ✅ Extract text based on file type
        if filename.endswith('.txt'):
            with open(file_path, 'r', encoding="utf-8") as f:
                extracted_text = f.read()
        elif filename.endswith('.pdf'):
            extracted_text = extract_text_from_pdf(file_path)  # Use PDF extraction
        else:
            extracted_text = extract_text_from_image(file_path)  # Use OCR for images

        # ✅ Apply question filtering before solving
        questions = extract_questions(extracted_text)

        if not questions:
            return jsonify({'error': 'No valid questions found in the file'}), 400

        answers = solve_questions(questions)

        # ✅ Format output
        solved_text = "\n".join(f"Q: {q}\nA: {a}" for q, a in zip(questions, answers))

        # ✅ Save to PDF
        pdf_filename = f"solved_{filename}.pdf"
        pdf_output_path = os.path.join(app.config['OUTPUT_FOLDER'], pdf_filename)
        save_output_to_pdf(solved_text, pdf_output_path)

        return jsonify({
            'message': 'File processed successfully',
            'pdf_download_url': f"/download/{pdf_filename}"
        })

    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500


@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    """
    Allows users to download the processed PDF file.
    """
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
