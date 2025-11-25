"""
Wave Function Collapse Implementation
Simple tile-based image generation
"""

from PIL import Image
import os


def setup(tile_size=16, output_width=160, output_height=160, input_image_path=None):
   
   
    """
    Setup function to initialize parameters and start the WFC process.
    
    Args:
        tile_size: Size of each tile in pixels (e.g., 16x16)
        output_width: Width of output image in pixels
        output_height: Height of output image in pixels
        input_image_path: Path to the input tileset image
    
    Returns:
        Path to the generated output image
    """


    print(f"Setup: tile_size={tile_size}, output={output_width}x{output_height}")
    
    # Set default input path if none provided
    if input_image_path is None:
        input_image_path = "static/images/WFC/test.png"
    
    # Set output path
    output_path = "static/images/WFC/WFCOutput/output.png"
    
    # Ensure output directory exists
    os.makedirs("static/images/WFC/WFCOutput", exist_ok=True)
    
    # Call draw function to create the image
    draw(tile_size, output_width, output_height, input_image_path, output_path)
    
    return output_path


def draw(tile_size, output_width, output_height, input_path, output_path):
    
    
    """
    Create and save a Pillow image.
    
    Args:
        tile_size: Size of each tile
        output_width: Width of output image
        output_height: Height of output image
        input_path: Path to input image
        output_path: Path to save output image
    """

    
    print(f"Drawing image...")
    print(f"  Input: {input_path}")
    print(f"  Output: {output_path}")
    
    # Create a new image (for now, just a simple colored rectangle as a test)
    img = Image.new('RGB', (output_width, output_height), color='blue')
    
    # TODO: Add WFC algorithm logic here
    # For now, just save the test image
    
    img.save(output_path)
    print(f"Saved image to {output_path}")


if __name__ == "__main__":
    # Test the functions
    print("Testing WFC.py...")
    output = setup(tile_size=16, output_width=160, output_height=160)
    print(f"Done! Check {output}")
