import sys
from PIL import Image


def rgb_to_ansi(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"


grayscale = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1]

def pixel_to_ascii(pixel, gscale):
    r, g, b = pixel[:3]
    gray = int(0.2989 * r + 0.5870 * g + 0.1140 * b)  
    scale_length = len(gscale)
    ascii_char = gscale[gray * scale_length // 256]
    return f"{rgb_to_ansi(r, g, b)}{ascii_char}"

def image_to_ascii(image_path, gscale):
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"Unable to open image file {image_path}: {e}")
        return ""
    

    width, height = image.size
    aspect_ratio = height / width
    new_width = 130
    new_height = int(aspect_ratio * new_width * 0.55)
    image = image.resize((new_width, new_height))
    

    image = image.convert("RGB")
    
    ascii_art = ""
    for y in range(new_height):
        for x in range(new_width):
            ascii_art += pixel_to_ascii(image.getpixel((x, y)), gscale)
        ascii_art += "\033[0m\n" 

    return ascii_art

def string_to_brainfuck(s):
    bf_code = ""
    current_value = 0
    
    for char in s:
        target_value = ord(char)
        diff = target_value - current_value
        
        if diff > 0:
            bf_code += '+' * diff
        elif diff < 0:
            bf_code += '-' * (-diff)
        
        bf_code += '.'
        current_value = target_value

    return bf_code

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <image_path>")
    else:
        image_path = sys.argv[1]
        ascii_art = image_to_ascii(image_path, grayscale)
        

        brainfuck_code = string_to_brainfuck(ascii_art)
        

        output_path = f"{image_path[:-4]}_brainfucked.bf"
        with open(output_path, "w") as f:
            f.write(brainfuck_code)
        
        print(f"Brainfuck code saved to {output_path}")
