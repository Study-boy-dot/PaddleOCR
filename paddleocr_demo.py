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

# Function to find the index of the closest average height
def find_closest_average(averages, height, tolerance):
    closest = []
    for i, avg in enumerate(averages):
        if abs(avg - height) <= tolerance:
            closest.append((abs(avg - height), i))
    if len(closest) > 0:
        closest.sort(key=lambda x : x[0])
        return closest[0][1]
    return None

# Initialize the list to store average heights
average_heights = []

# Tolerance percentage (10%)
tolerance_percentage = 0.10

# First pass: Determine the final average heights
height_mappings = []  # List to store the mapping of heights to their average indices

for box, _ in result:
    # Calculate the height of the current box
    y1 = box[0][1]
    y2 = box[3][1]
    y3 = box[1][1]
    y4 = box[2][1]
    height = ((y2 - y1) + (y4 - y3)) / 2

    # Calculate the tolerance based on height
    tolerance = height * tolerance_percentage

    # Find the closest average height index within tolerance
    index = find_closest_average(average_heights, height, tolerance)

    if index is None:
        # If no close average is found, add the height to averages
        average_heights.append(height)
        index = len(average_heights) - 1
    else:
        # Update the average height with the new height
        average_heights[index] = (average_heights[index] + height) / 2

    height_mappings.append(index)

# Second pass: Apply the determined font sizes based on average heights
doc = Document()

for i, (box, (text, _)) in enumerate(result):
    # Get the corresponding average height index
    index = height_mappings[i]
    average_height = average_heights[index]

    # Calculate the font size based on the average height
    font_size = Pt(average_height * 0.75)

    # Add the text to the document with the calculated font size
    paragraph = doc.add_paragraph(text)
    run = paragraph.runs[0]
    run.font.size = font_size

# Save the document
doc.save("output.docx")

print("Document created successfully!")