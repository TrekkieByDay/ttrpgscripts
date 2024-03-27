from PIL import Image
import os
from multiprocessing import Pool, cpu_count
import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")

def convert_and_resize_image(args):
    input_path, output_path, resize_percentage, quality, output_format = args
    
    # Remove the pixel limit entirely for large image processing
    Image.MAX_IMAGE_PIXELS = None
    
    try:
        with Image.open(input_path) as img:
            # Convert the image to RGB if saving as JPG
            if output_format.lower() == 'jpg':
                img = img.convert('RGB')
            
            # Resize the image if resize_percentage is not 100
            if resize_percentage != 100:
                width, height = img.size
                new_dimensions = (
                    int(width * resize_percentage / 100),
                    int(height * resize_percentage / 100)
                )
                img = img.resize(new_dimensions, Image.Resampling.LANCZOS)
            
            # Save the converted and resized image
            if output_format.lower() == 'jpg':
                img.save(output_path, 'JPEG', quality=quality)
            else:
                img.save(output_path)
            
            print(f"Completed: {os.path.basename(input_path)}")
    except Exception as e:
        print(f"Error converting file: {os.path.basename(input_path)}. Error: {e}")

def convert_images(input_directory, output_directory, resize_percentage=100, quality=85, output_format='jpg'):
    """
    Convert images to specified format, with options to resize and adjust quality.
    :param input_directory: Directory containing images to convert.
    :param output_directory: Directory where converted images will be saved.
    :param resize_percentage: Percentage to resize images by (default is 100, no resize).
    :param quality: JPEG quality for output images (1-95), ignored if output_format is PNG.
    :param output_format: 'jpg' or 'png', the format for the output images.
    """
    # Suppress DecompressionBombWarning and ignore the limit
    Image.MAX_IMAGE_PIXELS = None

    # Ensure the input directory exists
    if not os.path.isdir(input_directory):
        print("The specified input directory does not exist.")
        return

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Prepare arguments for multiprocessing
    args = []
    for filename in os.listdir(input_directory):
        if filename.lower().endswith('.png') or filename.lower().endswith('.jpg'):
            input_path = os.path.join(input_directory, filename)
            output_filename = os.path.splitext(filename)[0] + '.' + output_format
            output_path = os.path.join(output_directory, output_filename)
            args.append((input_path, output_path, resize_percentage, quality, output_format))

    # Use multiprocessing to convert images
    with Pool(processes=cpu_count()) as pool:
        pool.map(convert_and_resize_image, args)

if __name__ == '__main__':


    # Example usage
    input_directory = r"G:\My Drive\Programming\Python VS Code\Dyson Mapper\dyson_maps - Copy"  # Update this to your input directory path
    output_directory = r"G:\My Drive\Programming\Python VS Code\Dyson Mapper\dyson_maps_jpg"  # Update this to your output directory path
    resize_percentage = 100  # Example: Resize to 50% of the original size
    quality = 90  # Example: Set JPEG quality to 90
    output_format = 'JPG'  # Choose 'JPG' or 'PNG' for the output format

    convert_images(input_directory, output_directory, resize_percentage, quality, output_format)
