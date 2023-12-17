# bmp-converter
This Python script processes BMP image files and generates drawing instructions for the **Waveshare 1.8' LCD Rpico Display**. It works by dividing the images into squares and rectangles, identifying uniform color areas, and then generating commands to draw these areas.
Keep in mind that this script works the best for pixel art and animations as they're limited in colours and are primarily drawn from squares.

## Requirements
- Python 3
- PIL
- NumPy

## Usage
1. Find a gif that you like (preferably of pixel animation).
2. Using a program like Aseprite, scale it down to the size of the LCD display. Adjust the canvas size as needed.
3. Export as bmp. Ensure that each frame is saved in format of: `\[name\]1.bmp, \[name\]2.bmp, ...`
4. Change variables in the script where required.

Run:

    $ python3 bmp-convert.py

The script will generate a Python file (*example*_lib.py) which will contain functions for each frame. These functions, when called, will get the LCD screen to display the corresponding frame.

5. Compile the generated .py file to .mpy using [mpy-cross](https://github.com/micropython/micropython/blob/master/mpy-cross/README.md](https://github.com/micropython/micropython/tree/master/mpy-cross)https://github.com/micropython/micropython/tree/master/mpy-cross). This saves a lot of memory!
6. Import the created file and call the frame functions as required.
7. Copy+paste the code from terminal into main.py or any other file. Comment that section out if not needed. (*Optional*)

## Important!
- Ensure you have the Waveshare provided `lcd.py` driver file saved on our pico.
- Compile the generate file.
- Due to the limited memory space of the Rpico, it can only handle generated instruction files of approximately **~9000 lines**. Otherwise this will lead to a memory allocation error.
- Ensure bmp files of animation frames are all the same name and a number indicating which frame it is. This script can be used for still images, just make sure the image bmp file has a number as well.

## Demo
There is a demo folder which already contains all the required files to test it out!
Just upload:
  - `main.py`
  - `lcd.mpy`
  - `test_lib.mpy`

... to your pico and run main!


`test_lib.py` is an example of a generated file. 

`bmp_files` folder holds the gif and bmp files from which the instructions were generated!

## Other
Feel free to use and change the code as needed! This is not a perfect script by any means but worked for me :)

This approach doesn't take up a lot of storage and allows to hold several different animations on the pico.

If you'd like to simply display bmp images directly, ExcaliburZero has a great repository [here](https://github.com/ExcaliburZero/bmp_file_reader)!
