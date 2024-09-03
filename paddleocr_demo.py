from paddleocr import PaddleOCR, draw_ocr

# Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
# 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
ocr = PaddleOCR(use_angle_cls=True, lang="en", use_gpu=True)  # need to run only once to download and load model into memory
img_path = './text_images/bigsleep.jpg'
result = ocr.ocr(img_path, cls=True)
for idx in range(len(result)):
    res = result[idx]
    for line in res:
        print(line)

# 显示结果
from PIL import Image
# from PIL import ImageFont
# font = ImageFont.load_default()
result = result[0]
image = Image.open(img_path).convert('RGB')
boxes = [line[0] for line in result]
txts = [line[1][0] for line in result]
scores = [line[1][1] for line in result]
im_show = draw_ocr(image, boxes, txts, scores, font_path='./fonts/arial.ttf')
im_show = Image.fromarray(im_show)
im_show.save('result.jpg')

# Write word file
from docx import Document
from docx.shared import Pt

# Create a new Word document
doc = Document()

# Iterate over the OCR data
for box, (text, _) in result:
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