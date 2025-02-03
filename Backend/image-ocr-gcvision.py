from google.cloud import vision
import os

# Set the path to your service account key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service-account.json"

def extract_text_from_image(image_path):
    # Initialize the Vision API client
    client = vision.ImageAnnotatorClient()

    # Load the image
    with open(image_path, "rb") as image_file:
        content = image_file.read()
        image = vision.Image(content=content)

    # Perform text detection
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if not texts:
        return "No text detected."

    # Extract detected text
    detected_text = texts[0].description
    return detected_text

if __name__ == "__main__":
    # Path to your image
    image_path = "sample.jpg"
    
    # Extract and print text
    text = extract_text_from_image(image_path)
    print("Extracted Text:")
    print(text)
