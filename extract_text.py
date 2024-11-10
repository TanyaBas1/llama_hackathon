import pdfplumber

# Define file paths
input_pdf = "pension_document.pdf"
output_file = "extracted_text.txt"

# Extract text from the PDF
with pdfplumber.open(input_pdf) as pdf:
    with open(output_file, "w", encoding="utf-8") as f:
        for page in pdf.pages:
            f.write(page.extract_text())
            f.write("\n\n")  # Separate pages with double newlines
print("Text extraction completed. The output is saved in 'extracted_text.txt'.")