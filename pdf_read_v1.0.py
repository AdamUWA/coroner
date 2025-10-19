import re

from pdfminer.high_level import extract_pages, extract_text

for page_layout in extract_pages("2.pdf"):
    for element in page_layout:
        print(element)

# import fitz
# import PIL.Image
# import io

# pdf = fitz.open("5.pdf")
# counter = 1
# for i in range(len(pdf)):
#     page = pdf[i]
#     images = page.get_images()
#     for image in images:
#         base_img = pdf.extract_image(image[0])
#         image_data = base_img["image"]
#         img = PIL.Image.open(io.BytesIO(image_data))
#         extension = base_img["ext"]
#         img.save(open(f"image_5_{counter}.{extension}", "wb"))
#         counter += 1