from paddleocr import PaddleOCR, draw_ocr
from ocr2word import Write_Result_to_Word
import argparse
import os
from PIL import Image
import fnmatch

# Create a parser
parser = argparse.ArgumentParser()

# Add arguments to parser
parser.add_argument('-i', '--input_dir', type=str, help='Images input directory')
parser.add_argument('-o', '--output_dir', type=str, help='Result output directory')
parser.add_argument('-l', '--lang', type=str, default='en', help="OCR detecting language")
parser.add_argument('-f', '--file', type=str, help='Input file path')
parser.add_argument('-w', '--word', type=bool, default=True, help="Turn result to word")
args = parser.parse_args()

# Parse arguments
if args.input_dir is not None:
    input_dir = args.input_dir
if args.output_dir is not None:
    output_dir = args.output_dir
else:
    output_dir = f'output_{input_dir}'

# Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
# 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
ocr = PaddleOCR(use_angle_cls=True, lang=args.lang, use_gpu=True)  # need to run only once to download and load model into memory

if args.input_dir and args.output_dir:
    # Read folder
    if os.path.exists(input_dir):
        for file_name in os.listdir(input_dir):
            if file_name.endswith('.png') or file_name.endswith('.jpg'): 
                file_path = os.path.join(input_dir, file_name)
                # OCR images
                result = ocr.ocr(file_path, cls=True)

                # Display result
                if result is not None:
                    result = result[0]
                    if result is not None:
                        image = Image.open(file_path).convert('RGB')
                        boxes = [line[0] for line in result]
                        txts = [line[1][0] for line in result]
                        scores = [line[1][1] for line in result]
                        im_show = draw_ocr(image, boxes, txts, scores, font_path='./fonts/arial.ttf')
                        im_show = Image.fromarray(im_show)
                        if os.path.exists(output_dir) == False:
                            os.makedirs(output_dir)
                        im_show.save(f'{output_dir}/{file_name}')

                        # Save result to word
                        if args.word:
                            Write_Result_to_Word(result, f'{output_dir}/{os.path.splitext(file_name)[0]}.docx')
elif args.file:
    # Check file path exist
    if os.path.exists(args.file):
        # OCR image
        result = ocr.ocr(args.file, cls=True)

        # Display result
        if result is not None:
            result = result[0]
            if result is not None:
                image = Image.open(args.file).convert('RGB')
                boxes = [line[0] for line in result]
                txts = [line[1][0] for line in result]
                scores = [line[1][1] for line in result]
                im_show = draw_ocr(image, boxes, txts, scores, font_path='./fonts/arial.ttf')
                im_show = Image.fromarray(im_show)
                # Save result image
                if os.path.exists(output_dir) == False:
                    os.makedirs(output_dir)
                im_show.save(f'{output_dir}/{args.file}')
                
                # Save result to word
                if args.word:
                    Write_Result_to_Word(result, f'{output_dir}/{os.path.splitext(args.file)[0]}.docx')