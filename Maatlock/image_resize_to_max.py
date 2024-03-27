from PIL import Image
import os
import warnings
from multiprocessing import Pool, cpu_count

# Suppress all warnings
warnings.filterwarnings("ignore")

def resize_image(args):
    input_path, max_dimension = args
    """
    Resize the image at input_path if its width or height exceeds max_dimension,
    maintaining the aspect ratio.
    """
    
    # Remove the pixel limit entirely for large image processing
    Image.MAX_IMAGE_PIXELS = None
    try:
        with Image.open(input_path) as img:
            width, height = img.size
            # Determine if the image exceeds the maximum dimensions
            if width > max_dimension or height > max_dimension:
                # Calculate the new size maintaining the aspect ratio
                if width > height:
                    new_height = int((max_dimension / width) * height)
                    new_size = (max_dimension, new_height)
                else:
                    new_width = int((max_dimension / height) * width)
                    new_size = (new_width, max_dimension)
                
                # Resize the image
                resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
                
                # Save the resized image back to the same path
                resized_img.save(input_path)
                print(f"Resized: {os.path.basename(input_path)}")
            else:
                print(f"No resize needed: {os.path.basename(input_path)}")
    except Exception as e:
        print(f"Error processing file: {os.path.basename(input_path)}. Error: {e}")

def resize_images_in_directory(directory, max_dimension):
    """
    Resize images in the specified directory if they exceed the specified maximum dimension.
    """
    
    # Remove the pixel limit entirely for large image processing
    Image.MAX_IMAGE_PIXELS = None
    # Prepare arguments for multiprocessing
    args = [(os.path.join(directory, filename), max_dimension) 
            for filename in os.listdir(directory) 
            if os.path.isfile(os.path.join(directory, filename)) and filename.lower().endswith(('.png', '.jpg', '.jpeg'))]

    # Use multiprocessing to resize images
    with Pool(processes=cpu_count()) as pool:
        pool.map(resize_image, args)

if __name__ == '__main__':
    directory = r"G:\My Drive\Programming\Python VS Code\Dyson Mapper\dyson_maps_jpg"  # Update this to the directory containing your images
    max_dimension = 1024*8  # Update this to your desired maximum dimension (width or height)
    
    resize_images_in_directory(directory, max_dimension)
