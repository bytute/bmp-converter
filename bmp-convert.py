from PIL import Image
import numpy as np
import os
from collections import Counter

# Function to check if a square is of uniform color
def is_uniform_color(square):
    return np.all(square == square[0, 0])

def colour(R, G, B):
    # Get RED value
    rp = int(R * 31 / 255)  # range 0 to 31
    if rp < 0: rp = 0
    r = rp * 8
    # Get GREEN value 
    gp = int(G * 63 / 255)  # range 0 - 63
    if gp < 0: gp = 0
    g = 0
    if gp & 1:  g += 8192
    if gp & 2:  g += 16384
    if gp & 4:  g += 32768
    if gp & 8:  g += 1
    if gp & 16: g += 2
    if gp & 32: g += 4
    # Get BLUE value       
    bp = int(B * 31 / 255)  # range 0 - 31
    if bp < 0: bp = 0
    b = bp * 256
    return r + g + b

def find_most_frequent_color(img_array):
    # Flatten the image array and convert to list of (R, G, B) tuples
    flat_img = img_array.reshape(-1, img_array.shape[-1])
    # Convert each pixel to its color value
    color_values = [colour(*pixel) for pixel in flat_img]
    # Count the frequency of each color value
    color_counts = Counter(color_values)
    # Find the most common color value
    most_common_color = color_counts.most_common(1)[0][0]
    return most_common_color

def generate_optimized_instructions_with_color_filter(img_array, ignore_color):
    height, width = img_array.shape[:2]
    processed = np.zeros((height, width), dtype=bool) 
    instructions = []

    for y in range(height):
        x = 0
        while x < width:
            if not processed[y, x]:
                color_value = colour(*img_array[y, x])
                if color_value != ignore_color:  # Skip if the color value is ignored
                    x_end = x + 1
                    while x_end < width and np.all(img_array[y, x_end] == img_array[y, x]) and not processed[y, x_end]:
                        x_end += 1

                    y_end = y + 1
                    valid_extension = True
                    while y_end < height and valid_extension:
                        for xi in range(x, x_end):
                            if not np.all(img_array[y_end, xi] == img_array[y, x]) or processed[y_end, xi]:
                                valid_extension = False
                                break
                        if valid_extension:
                            y_end += 1

                    processed[y:y_end, x:x_end] = True
                    instructions.append(f"lcd.fill_rect({x}, {y}, {x_end - x}, {y_end - y}, {color_value})")

            x += 1

    return instructions

# Process bmp files within a directory
def process_directory(directory_path, output_file_path):
    bmp_files = [f for f in os.listdir(directory_path) if f.endswith('.bmp')]
    sorted_bmp_files = sorted(bmp_files, key=lambda x: int(x.replace(f'{frames_name}', '').replace('.bmp', '')))  # Sorting files

    with open(output_file_path, 'w') as output_file:
        c = 1
        output_file.write(f"import lcd\n")
        output_file.write(f"lcd = lcd.LCD_1inch8()\n")
        for bmp_file in sorted_bmp_files:
            img_path = os.path.join(directory_path, bmp_file)
            img = Image.open(img_path).convert('RGB')  # Convert to RGB mode
            img_array = np.array(img)

            # Find the most frequent color in the image
            most_frequent_color = find_most_frequent_color(img_array)

            # Generate instructions ignoring the most frequent color
            instructions = generate_optimized_instructions_with_color_filter(img_array, most_frequent_color)

            # Output being created for the "lib" file
            output_file.write(f"# {bmp_file}\n")
            output_file.write(f"def frame{c}():\n")
            output_file.write(f"\tlcd.fill({most_frequent_color})\n") # Setting background to ignored colour
            for instruction in instructions:
                output_file.write("\t"+ instruction + '\n')
            output_file.write("\tlcd.show()\n\n")
            final.append(f"frame{c}")
            c += 1

final = []
secs = "0.03"   # Seconds to sleep between each frame (Change if needed)
frames_name = "name-of-your-exported-bmp-files"  # Name of your frame files
                                                 # If you have a gif named Samus.gif, and export frames as Samus1.bmp, Samus2.bmp, etc, 
                                                 # change frames_name to "Samus". 


directory_path = '/path/to/bmp/files' # Path to bmp file directory
output_file_path = '/path/for/output/file' + f'{frames_name}_lib.py'# Path where to save the generated "lib" file 

process_directory(directory_path, output_file_path)

# Prints instructions to copy paste into main or other file
# Can be commented out if not needed

print("""from machine import Pin,SPI,PWM
import time
import gc

BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9
    
    
#=============== MAIN ============

if __name__ == '__main__':""")

print("""\t# Setup the LCD display
\tpwm = PWM(Pin(BL))
\tpwm.freq(1000)
\tpwm.duty_u16(65535)#max 65535

\tgc.collect()
""")

print("\timport " + frames_name + "_lib")
print("\twhile True:")
for i in range(len(final)):
    print(f"\t\t{frames_name}_lib" + "." + f"{final[i]}" + "()")
    print(f"\t\ttime.sleep({secs})")
    print("\t\tgc.collect()")