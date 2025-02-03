from PIL import Image
import pytesseract
import cv2
import os

# Set the Tesseract executable path (if not in system PATH)
# Uncomment and set the correct path if needed
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image_path):
    """
    Preprocess the image to improve OCR accuracy.
    Steps:
    1. Convert to grayscale.
    2. Apply thresholding.
    3. Save the processed image temporarily.
    """
    # Load the image using OpenCV
    image = cv2.imread(image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply binary thresholding
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    
    # Save the processed image temporarily
    processed_path = "processed_image.jpg"
    cv2.imwrite(processed_path, thresh)
    
    return processed_path

def extract_text_from_image(image_path):
    """
    Extract text from an image using Tesseract OCR.
    """
    # Preprocess the image for better OCR
    processed_image_path = preprocess_image(image_path)
    
    # Load the processed image with PIL
    image = Image.open(processed_image_path)
    
    # Perform OCR
    text = pytesseract.image_to_string(image)
    
    # Clean up the temporary processed image
    os.remove(processed_image_path)
    
    return text

if __name__ == "__main__":
    # Input image path
    image_path = "sample.jpg"  # Replace with your image file path
    
    # Check if the image file exists
    if not os.path.exists(image_path):
        print(f"Image file '{image_path}' not found.")
    else:
        # Extract text from the image
        extracted_text = extract_text_from_image(image_path)
        print("Extracted Text:")
        print(extracted_text)
