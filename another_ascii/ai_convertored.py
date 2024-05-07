from PIL import Image, ImageDraw, ImageFont
import os
import numpy as np

class AsciiConverter:
    def __init__(self, character="$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1], intensity_level=10, scale_factor=0.1, one_char_width=10, one_char_height=18, extract_frames_path='extracted-frames', ascii_frames_path='ascii_frames4'):
        self.character = character
        self.intensity_level = intensity_level
        self.scale_factor = scale_factor
        self.one_char_width = one_char_width
        self.one_char_height = one_char_height
        self.extract_frames_path = extract_frames_path
        self.ascii_frames_path = ascii_frames_path

    def getChar(self, input_int):
        char_array = list(self.character)
        char_length = len(char_array)
        intensity_step = 256 / self.intensity_level
        intensity_index = int(input_int / intensity_step)
        index = min(intensity_index * (char_length - 1) // self.intensity_level, char_length - 1)
        return char_array[int(index)]

    def ascii_converter(self):
        os.makedirs(self.ascii_frames_path, exist_ok=True)
        print("Directories Successfully Made!\n")

        font = ImageFont.truetype("C:\\Windows\\Fonts\\lucon.ttf", 10)
        items_no = len(os.listdir(self.extract_frames_path))
        max_iter = items_no + 0

        for iteration in range(max_iter):
            im = Image.open(f"{self.extract_frames_path}/frame{iteration}.png").convert("RGB")
            width, height = im.size
            im = im.resize((int(self.scale_factor * width), int(self.scale_factor * height * (self.one_char_width / self.one_char_height))), Image.NEAREST)
            width, height = im.size
            pix = np.array(im)

            output_image = Image.new("RGB", (self.one_char_width * width, self.one_char_height * height), color=(0, 0, 0))
            d = ImageDraw.Draw(output_image)

            for i in range(height):
                for j in range(width):
                    r, g, b = pix[i, j]
                    h = int(np.mean(pix[i, j]))
                    char = self.getChar(h)
                    d.text((j * self.one_char_width, i * self.one_char_height), char, font=font, fill=(r, g, b))

            output_image.save(f"{self.ascii_frames_path}/ascii_frame{iteration}.png")
            print(f"Ascii-Frame Converted- #{iteration}", end='\r')

if __name__=='__main__':
    convertor = AsciiConverter()
    convertor.ascii_converter()