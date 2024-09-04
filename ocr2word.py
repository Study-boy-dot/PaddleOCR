# Write word file
from docx import Document
from docx.shared import Pt
import numpy as np

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

# First pass: Determine the final average heights
def _font_size_generator(result:list):
    # Initialize the list to store average heights
    average_heights = []

    # Tolerance percentage (10%)
    tolerance_percentage = 0.10

    height_mappings = []  # List to store the mapping of heights to their average indices

    for i, (box, _) in enumerate(result):
        # Calculate the height of the current box
        y1 = box[0][1]
        y2 = box[3][1]
        y3 = box[1][1]
        y4 = box[2][1]
        height = np.average((y2- y1, y4 - y3)).astype(np.int32)

        # Calculate the tolerance based on height
        tolerance = height * tolerance_percentage

        # Find the closest average height index within tolerance
        index = find_closest_average(average_heights, height, tolerance)

        if index is None:
            # If no close average is found, add the height and base to averages
            average_heights.append(height)
            index = len(average_heights) - 1
        else:
            # Update the average height with the new height
            # avg_new_ = avg_old_ + (new_value - avg_old) / (n+1)
            average_heights[index] = average_heights[index] + (height - average_heights[index]) / i # Approximate to real average

        height_mappings.append(index)

    return average_heights, height_mappings

# Second pass: Apply the determined font sizes based on average heights
def Write_Result_to_Word(result:list, output_path:str = "output.docs"):
    doc = Document()

    average_heights, height_mappings = _font_size_generator(result)

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
    doc.save(output_path)

    print("Document created successfully!")