import os
from pypdf import PdfReader

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.
    
    Args:
        pdf_path (str): The path to the PDF file.
        
    Returns:
        str: The extracted text content.
    """
    if not os.path.exists(pdf_path):
        return f"Error: File not found at {pdf_path}"
    
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def save_text_to_file(text, output_path):
    """
    Saves text to a file.
    
    Args:
        text (str): The text to save.
        output_path (str): The path to the output file.
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        return f"Successfully saved text to {output_path}"
    except Exception as e:
        return f"Error saving file: {str(e)}"

if __name__ == "__main__":
    # Example usage for testing
    import sys
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        print(f"Processing {pdf_path}...")
        content = extract_text_from_pdf(pdf_path)
        print(f"Extracted {len(content)} characters.")
    else:
        print("Please provide a PDF path as an argument.")
        print("IMPORTANT: Do not run this script with direct 'python' invocation.")
        print("Always run via uv to ensure the correct environment and dependency isolation:")
        print("  uv run src/pdf_tools.py <path/to/paper.pdf>")
