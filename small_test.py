# Write word file
from docx import Document
from docx.shared import Pt

# Sample OCR output
ocr_data = [
    [[[60.0, 120.0], [541.0, 120.0], [541.0, 134.0], [60.0, 134.0]], 
     ('shining and a look of hard wet rain in the clearness of the foothills. I was', 0.9506351351737976)],
    [[[60.0, 134.0], [538.0, 134.0], [538.0, 148.0], [60.0, 148.0]], 
     ('wearing my powder-blue suit, with dark blue shirt, tie and display', 0.942742109298706)],
    [[[60.0, 150.0], [539.0, 150.0], [539.0, 164.0], [60.0, 164.0]], 
     ('handkerchief, black brogues, black wool socks with dark blue clocks on', 0.9439840912818909)],
    [[[60.0, 165.0], [541.0, 165.0], [541.0, 179.0], [60.0, 179.0]], 
     ("them.I was neat, clean,shaved and sober, and I didn't care who knew it.I", 0.9368178844451904)]
]

# Create a new Word document
doc = Document()

# Iterate over the OCR data
for box, (text, _) in ocr_data:
    # Extract the Y-coordinate (vertical position)
    y1 = box[0][1]
    y2 = box[2][1]
    height = y2 - y1  # The height of the text box in the image

    # Add the text to the document
    paragraph = doc.add_paragraph(text)

    # Set the font size based on the height
    run = paragraph.runs[0]
    font_size = Pt(height * 0.75)  # Adjust the scaling factor as needed
    run.font.size = font_size

# Save the document
doc.save("output.docx")

print("Document created successfully!")