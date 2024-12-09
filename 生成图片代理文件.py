import cv2
import os
from concurrent.futures import ThreadPoolExecutor

input_folder = '1'
n = 0.2

def resize_image(filename, input_folder, output_folder, n):
    file_path = os.path.join(input_folder, filename)
    if os.path.isfile(file_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        img = cv2.imread(file_path)
        if img is not None:
            height, width = img.shape[:2]
            new_dimensions = (int(width * n), int(height * n))
            resized_img = cv2.resize(img, new_dimensions)
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, resized_img)

def resize_images(input_folder, n):
    output_folder = f"{input_folder}_{n}"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    filenames = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    with ThreadPoolExecutor() as executor:
        for filename in filenames:
            executor.submit(resize_image, filename, input_folder, output_folder, n)

resize_images(input_folder, n)
