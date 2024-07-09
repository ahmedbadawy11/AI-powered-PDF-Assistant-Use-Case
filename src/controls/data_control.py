import os

from pdf2image import convert_from_path
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter




def save_uploaded_file(uploaded_file):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    files_dir = os.path.join(base_dir, "assets", "files")
    
    if not os.path.exists(files_dir):
        os.makedirs(files_dir)
    
    pdf_name = os.path.splitext(uploaded_file.name)[0]
    pdf_folder = os.path.join(files_dir, pdf_name)
    
    if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder)
    
    file_path = os.path.join(pdf_folder, uploaded_file.name)
    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return file_path, pdf_folder,pdf_name



# Read Arabic Text And Extract it 

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def pdf_to_images(pdf_path, output_folder, dpi=300):
    pop_path=os.path.join( os.path.dirname(__file__) ,"poppler-24.02.0/Library/bin")
  
    images = convert_from_path(pdf_path, dpi=dpi,poppler_path=pop_path)
    image_paths = []
    for i, image in enumerate(images):
        image_path = f"{output_folder}/page_{i + 1}.png"
        image.save(image_path, 'PNG')
        image_paths.append(image_path)
    return image_paths


def preprocess_image(image_path):
    image = Image.open(image_path)
    
    image = image.convert('L')
    
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)
    
    image = image.point(lambda p: p > 128 and 255)
    
    image = image.filter(ImageFilter.MedianFilter())
    return image

def extract_text_from_image(image):
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(image, lang='ara', config=custom_config)
    return text

def extract_text_from_images(image_paths,output_txt_files_path):
    all_text = ""
    for i,image_path in enumerate(image_paths):
        image = preprocess_image(image_path)
        text = extract_text_from_image(image)
        pages_path=os.path.join(output_txt_files_path,"pages")
        if not os.path.exists(pages_path):
            os.makedirs(pages_path)
        text_file_path = os.path.join(pages_path, f'page_{i + 1}.txt')
        save_text_to_file(text,text_file_path)
        all_text += text + "\n\n"
    return all_text



def save_text_to_file(text, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as text_file:
        text_file.write(text)



def Extract_text_from_pdf_Tesseract(pdf_path, pdf_folder):


    output_folder_image=os.path.join(pdf_folder,"output_images")
    if not os.path.exists(output_folder_image):
        os.makedirs(output_folder_image)



    output_txt_files_path=os.path.join(pdf_folder,"output_text")
    if not os.path.exists(output_txt_files_path):
        os.makedirs(output_txt_files_path)
    
    image_paths = pdf_to_images(pdf_path, output_folder_image)
    all_text = extract_text_from_images(image_paths,output_txt_files_path)
    all_text_file_path = os.path.join(output_txt_files_path, f'all_text.txt')
    save_text_to_file(all_text, all_text_file_path)

    print(f"Extracted text saved to {output_txt_files_path}")

    return all_text_file_path,all_text




