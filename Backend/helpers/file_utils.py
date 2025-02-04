from PyPDF2 import PdfReader
from helpers.ocr import extract_text_from_image
from fpdf import FPDF
from pdf2image import convert_from_path
import os

def save_output_to_pdf(text, output_path):
    """
    Save the extracted text into a PDF file with Unicode support.
    """
    try:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Get absolute path of the font file
        # font_path = os.path.abspath("/home/faizan-raza/Documents/qs-solver/Backend/fonts/DejaVuSans.ttf")
        # print(type(font_path))
        # current_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the font path relative to the script's directory
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Navigate up one directory level to the "Backend" folder
        backend_dir = os.path.dirname(current_dir)

        # Construct the font path relative to the "Backend" directory
        font_path = os.path.join(backend_dir, "fonts", "DejaVuSans.ttf")
        print(f"Font Path: {font_path}")
        print(f"Type of font_path: {type(font_path)}")

        if not os.path.exists(font_path):
            raise FileNotFoundError(f"Font file not found: {font_path}")

        print("Font file exists!")

        print("reaccched")
        # Use a font that supports Unicode (TTF)
        try:
            pdf.add_font("DejaVuSans", "", font_path, uni=True)
            print("Font added successfully!")
        except Exception as e:
            print(f"Error adding font: {e}")
            raise  # Re-raise the exception to stop execution
        pdf.set_font("DejaVuSans", size=12)
        print("reaccched2")
        # Add text to the PDF, handling line breaks
        for line in text.split("\n"):
            pdf.multi_cell(0, 10, line)
            # print("Line added to PDF.")

        # Save the PDF
        pdf.output(output_path)
        print(f"PDF saved successfully at {output_path}")
    except Exception as e:
        print(f"Error generating PDF: {e}")

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF. Handles both plain text and image-based PDFs.
    """
    try:
        reader = PdfReader(pdf_path)
        plain_text = "".join(page.extract_text() + "\n" for page in reader.pages if page.extract_text())

        if plain_text.strip():
            return plain_text

        images = convert_from_path(pdf_path)
        ocr_text = "\n".join(extract_text_from_image(image) for image in images)

        return ocr_text.strip()
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""
