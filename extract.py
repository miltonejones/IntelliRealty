 
import os
from pdf2image import convert_from_path 
 


def extract_images_from_pdf(pdf_path):
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_folder = f'./images/{pdf_name}'
    print ('output_folder', output_folder)
 


    images = convert_from_path(pdf_path)
 

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    for i, image in enumerate(images):
        image.save(f"{output_folder}/{pdf_name}-{i}.jpg", "JPEG")
  
# if __name__ == "__main__":
#     pdf_file_path = "path/to/your/pdf_file.pdf"
#     output_folder_path = "path/to/output/folder"
#     extract_images_from_pdf(pdf_file_path, output_folder_path)
