from google.cloud import vision
import os

def extract_text_from_image(image_path):
    """
    Extracts text along with spaces and formatting from an image.
    """
    # Set the path to your service account key file
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service-account.json"

    # Initialize Vision API client
    client = vision.ImageAnnotatorClient()

    # Load the image
    with open(image_path, "rb") as image_file:
        content = image_file.read()
        image = vision.Image(content=content)

    # Perform text detection
    response = client.text_detection(image=image)
    annotations = response.text_annotations

    if not annotations:
        return "No text detected."

    # Process word-level annotations
    words = []
    lines = []
    current_line_y = None
    space_threshold = 15  # Adjust as needed for space detection

    for word in annotations[1:]:  # Skip the first annotation (it's the full text)
        bounding_box = word.bounding_poly.vertices
        word_text = word.description

        # Calculate word position
        y_position = (bounding_box[0].y + bounding_box[2].y) / 2

        # Detect line breaks
        if current_line_y is None or abs(y_position - current_line_y) > space_threshold:
            # New line
            if words:
                lines.append(" ".join(words))
            words = []  # Reset words for the new line
            current_line_y = y_position

        # Append the word to the current line
        words.append(word_text)

    # Add the last line
    if words:
        lines.append(" ".join(words))

    # Join lines with line breaks
    formatted_text = "\n".join(lines)
    return formatted_text

if __name__ == "__main__":
    # Path to your image
    image_path = "sample.jpg"
    
    # Extract and print text
    text = extract_text_from_image(image_path)
    print("Extracted Text:")
    print(text)

#######################
# from google.cloud import vision
# import os

# # Set the path to your service account key file
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service-account.json"

# def extract_text_with_formatting(image_path):
#     """
#     Extracts text along with spaces and formatting from an image.
#     """
#     from google.cloud import vision
#     import os

#     # Initialize Vision API client
#     client = vision.ImageAnnotatorClient()

#     # Load the image
#     with open(image_path, "rb") as image_file:
#         content = image_file.read()
#         image = vision.Image(content=content)

#     # Perform text detection
#     response = client.text_detection(image=image)
#     annotations = response.text_annotations

#     if not annotations:
#         return "No text detected."

#     # Process word-level annotations
#     words = []
#     lines = []
#     current_line_y = None
#     space_threshold = 15  # Adjust as needed for space detection

#     for word in annotations[1:]:  # Skip the first annotation (it's the full text)
#         bounding_box = word.bounding_poly.vertices
#         word_text = word.description

#         # Calculate word position
#         y_position = (bounding_box[0].y + bounding_box[2].y) / 2

#         # Detect line breaks
#         if current_line_y is None or abs(y_position - current_line_y) > space_threshold:
#             # New line
#             if words:
#                 lines.append(" ".join(words))
#             words = []  # Reset words for the new line
#             current_line_y = y_position

#         # Append the word to the current line
#         words.append(word_text)

#     # Add the last line
#     if words:
#         lines.append(" ".join(words))

#     # Join lines with line breaks
#     formatted_text = "\n".join(lines)
#     return formatted_text

# if __name__ == "__main__":
#     # Path to your image
#     image_path = "sample.jpg"
    
#     # Extract and print text
#     text = extract_text_from_image(image_path)
#     print("Extracted Text:")
#     print(text)





########################


# from PIL import Image
# import pytesseract
# import cv2
# import os

# # Set the Tesseract executable path (if not in system PATH)
# # Uncomment and set the correct path if needed
# # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# def preprocess_image(image_path):
#     """
#     Preprocess the image to improve OCR accuracy.
#     Steps:
#     1. Convert to grayscale.
#     2. Apply thresholding.
#     3. Save the processed image temporarily.
#     """
#     # Load the image using OpenCV
#     image = cv2.imread(image_path)
    
#     # Convert to grayscale
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
#     # Apply binary thresholding
#     _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    
#     # Save the processed image temporarily
#     processed_path = "processed_image.jpg"
#     cv2.imwrite(processed_path, thresh)
    
#     return processed_path

# def extract_text_with_formatting(image_path):
#     """
#     Extract text from an image using Tesseract OCR.
#     """
#     # Preprocess the image for better OCR
#     processed_image_path = preprocess_image(image_path)
    
#     # Load the processed image with PIL
#     image = Image.open(processed_image_path)
    
#     # Perform OCR
#     text = pytesseract.image_to_string(image)
    
#     # Clean up the temporary processed image
#     os.remove(processed_image_path)
    
#     return text

# if __name__ == "__main__":
#     # Input image path
#     image_path = "sample.jpg"  # Replace with your image file path
    
#     # Check if the image file exists
#     if not os.path.exists(image_path):
#         print(f"Image file '{image_path}' not found.")
#     else:
#         # Extract text from the image
#         extracted_text = extract_text_from_image(image_path)
#         print("Extracted Text:")
#         print(extracted_text)
