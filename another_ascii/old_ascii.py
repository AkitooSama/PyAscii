from PIL import Image, ImageDraw, ImageFont, ImageFile
import moviepy.video.io.ImageSequenceClip
import moviepy.editor as mp
import shutil
import math
import cv2
import os

Frames_Image_Path = "Frames"

# Class_Functions
class convertor:
    def __init__(
        self,
        Path,
        Text_Save=False,
        ScaleFactor=0.09,
        oneCharWidth=10,
        oneCharHeight=18,
        Frames_Save=False,
        AsciiFrames_Save=False,
    ):
        # Variables
        self.Path = Path
        self.Text_Save = Text_Save
        self.Frames_Save = Frames_Save
        self.ScaleFactor = ScaleFactor
        self.oneCharWidth = oneCharWidth
        self.oneCharHeight = oneCharHeight
        self.AsciiFrames_Save = AsciiFrames_Save

    def Frame_Extractor(self):
        vid = cv2.VideoCapture(self.Path)
        Frames_Image_Path = "Frames-Image"
        self.Frames_Image_Path = Frames_Image_Path
        try:
            if not os.path.exists(Frames_Image_Path):
                os.makedirs(Frames_Image_Path)
                print("Directory wasn't found-\n")
                print("Directory Successfully Made!\n")
        except OSError:
            print("Error: Creating directory of data\n")
        currentframe = 0
        while True:
            success, frame = vid.read()
            if success:
                name = f"./{Frames_Image_Path}/frame" + str(currentframe) + ".jpg"
                print("Creating..." + name)
                cv2.imwrite(name, frame)
                currentframe += 1
            else:
                break

    def getChar(self, InputInt):
        Character = (
            "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[
                ::-1
            ]
        )
        charArray = list(Character)
        charLength = len(charArray)
        interval = charLength / 256
        return charArray[math.floor(InputInt * interval)]

    def Ascii_Convertor(self):
        Ascii_Path = "Ascii-Images"
        self.Ascii_Path = Ascii_Path
        try:
            if not os.path.exists(Ascii_Path):
                os.makedirs(Ascii_Path)
                print("Directory Successfully Made!\n")
        except OSError:
            print("Error: Creating directory of data\n")

        Itteration = 0
        Items_No = len(os.listdir(f"./{Frames_Image_Path}"))
        MaxItter = Items_No + 0

        while Itteration < MaxItter:

            Text_Path = "Text-Files"
            self.Text_Path = Text_Path
            try:
                if not os.path.exists(Text_Path):
                    os.makedirs(Text_Path)
                    print("Directory Successfully Made!\n")
            except OSError:
                print("Error: Creating directory of data\n")

            text_file = open(f"./{Text_Path}/Text_Frame{Itteration}.txt", "w")

            im = Image.open(
                f"./{Frames_Image_Path}/frame{Itteration}.jpg"
            ).convert("RGB")
            fnt = ImageFont.truetype("C:\\Windows\\Fonts\\lucon.ttf", 15)

            width, height = im.size
            im = im.resize(
                (
                    int(self.ScaleFactor * width),
                    int(
                        self.ScaleFactor
                        * height
                        * (self.oneCharWidth / self.oneCharHeight)
                    ),
                ),
                Image.NEAREST,
            )
            width, height = im.size
            pix = im.load()

            outputImage = Image.new(
                "RGB",
                (self.oneCharWidth * width, self.oneCharHeight * height),
                color=(0, 0, 0),
            )

            d = ImageDraw.Draw(outputImage)

            for i in range(height):
                for j in range(width):
                    r, g, b = pix[j, i]
                    h = int(r / 3 + g / 3 + b / 3)
                    pix[j, i] = (h, h, h)
                    text_file.write(self.getChar(h))
                    d.text(
                        (j * self.oneCharWidth, i * self.oneCharHeight),
                        self.getChar(h),
                        font=fnt,
                        fill=(r, g, b),
                    )

                text_file.write("\n")

            outputImage.save(f"./{Ascii_Path}/ascii_frame{Itteration}.png")
            print(f"Ascii-Frame Converted- #{Itteration}")
            Itteration += 1
        vidfps = cv2.VideoCapture(self.Path)
        FPS = vidfps.get(cv2.CAP_PROP_FPS)
        print(FPS)

        print(FPS)

        self.Video_Process(
            MaxItter=MaxItter,
            FPS=FPS,
            Text_Path=Text_Path,
            Frames_Image_Path=self.Frames_Image_Path,
            Ascii_Path=Ascii_Path,
        )

    def Video_Process(self, MaxItter, FPS, Text_Path, Frames_Image_Path, Ascii_Path):
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        image_files = []
        for img_number in range(0, MaxItter):
            image_files.append("Ascii-Images/ascii_frame" + str(img_number) + ".png")

        fps = FPS

        clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(
            image_files, fps=fps
        )
        clip.write_videofile("my_new_video.avi", codec="png", threads="3")

        # my_clip = mp.VideoFileClip(self.Path)
        # my_clip.audio.write_audiofile(r"my_result.mp3")

        my_clip2 = mp.VideoFileClip(r"my_new_video.avi")
        # my_resutmp3
        audio_background = mp.AudioFileClip(
            r"C:\Users\DigiTronic\Downloads\SnapInsta.io - Stelore - Mofo (Official Music Video) (320 kbps).mp3"
        )
        final_clip = my_clip2.set_audio(audio_background)
        final_clip.write_videofile(
            "Ascii-Video.avi", fps=fps, codec="png", threads="3"
        )

        Fclip = mp.VideoFileClip("Ascii-Video.avi")
        Fclip.write_videofile("my----video.mp4")

        # """

        # ===Tree-Removing===
        Itteration = 0
        MaxItter = len(os.listdir(f"./{Frames_Image_Path}"))
        while Itteration < MaxItter:
            open(f"./{Frames_Image_Path}/frame{Itteration}.jpg", "r").close()
            open(f"./{Ascii_Path}/ascii_frame{Itteration}.png", "r").close()
            open(f"./{Text_Path}/Text_Frame{Itteration}.txt", "r").close()
            Itteration += 1

        clip.close()
        # my_clip.close()
        my_clip2.close()
        Fclip.close()
        audio_background.close()

        print("Video Processed!")

        os.remove("my_new_video.avi")
        os.remove("my_result.mp3")
        os.remove("Ascii-Video.avi")

        if self.Frames_Save == False:
            shutil.rmtree(Frames_Image_Path)
        if self.AsciiFrames_Save == False:
            shutil.rmtree(Ascii_Path)
        if self.Text_Save == False:
            shutil.rmtree(Text_Path)
        print("Completed-100%!!")
        # """
