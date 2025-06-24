from PIL import Image
import pytesseract
import cv2
import numpy as np
import os

# Specify the path to Tesseract executable (update this based on your system)
# pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # Example for Linux/Mac, adjust for your system
# For Windows, use: r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image_path):
    """
    Preprocess the image to improve OCR accuracy:
    - Convert to grayscale
    - Apply thresholding to enhance text contrast
    - Resize for better readability
    """
    # Read image using OpenCV
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Image file '{image_path}' not found.")
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply adaptive thresholding to binarize the image
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    
    # Resize image to improve OCR (optional, adjust scale factor as needed)
    scale_factor = 1.5
    resized = cv2.resize(thresh, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)
    
    # Save preprocessed image temporarily (for debugging)
    preprocessed_path = 'preprocessed_invoice.png'
    cv2.imwrite(preprocessed_path, resized)
    
    return preprocessed_path

def extract_text_from_invoice(image_path, lang='eng'):
    """
    Extract text from an invoice image using PyTesseract.
    """
    try:
        # Preprocess the image
        preprocessed_path = preprocess_image(image_path)
        
        # Open the preprocessed image with PIL
        img = Image.open(preprocessed_path)
        
        # Custom Tesseract configuration
        # --oem 3: Default OCR engine
        # --psm 6: Assume a single uniform block of text (good for invoices)
        custom_config = r'--oem 3 --psm 6'
        
        # Extract text
        text = pytesseract.image_to_string(img, lang=lang, config=custom_config)
        
        # Clean up temporary file
        os.remove(preprocessed_path)
        
        return text
    except Exception as e:
        return f"Error during OCR: {str(e)}"

def main():
    # Path to your invoice image (replace with your image path)
    invoice_image_path = '/Users/bhargavdeviprasads/Documents/works/practise/c++/Developer/dropBox1/DropBox-1/Screenshot 2025-06-24 at 2.02.20 PM.png'
    
    # Specify language (e.g., 'eng' for English)
    language = 'eng'
    
    # Extract text
    extracted_text = extract_text_from_invoice(invoice_image_path, lang=language)
    
    # Print the extracted text
    print("\nExtracted Text from Invoice:\n")
    print(extracted_text)
    
    # Optional: Save extracted text to a file
    output_file = 'invoice_text.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(extracted_text)
    print(f"\nExtracted text saved to '{output_file}'")
    
    # Optional: Basic parsing example (e.g., find invoice number and date)
    lines = extracted_text.split('\n')
    for line in lines:
        if 'invoice no' in line.lower():
            print(f"Found Invoice Number: {line}")
        elif 'date' in line.lower():
            print(f"Found Date: {line}")
        elif 'due date' in line.lower():
            print(f"Found Due Date: {line}")

if __name__ == '__main__':
    main()