import os
from rich import print as cprint
from PIL import Image, ImageFont, ImageDraw
import time
import ffmpeg


class ArgumentError(Exception):
    def __init__(self, error):
        self.error = error
        super().__init__(self.error)


class Convertor:
    def __init__(
        self,
        extract_frames_path: str = "extracted-frames",
        video_path: str = None,
        ascii_frames_path: str = "ascii-frame",
        text_frames_path: str = "text-frame",
        output_video_path: str = "output-video.mp4",
        output_audio_name="output-audio.mp3",
        png_quality: int = 1,
        intensity_level: int = 16,
        scale_factor: int = 0.09,
        one_char_width: int = 10,
        one_char_height: int = 18,
        character: str = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[
            ::-1
        ],
        original_vid_ratio: bool = False,
        hardware_acceleration: bool = False,
    ):
        self.hardware_acceleration = hardware_acceleration
        self.extract_frames_path = extract_frames_path
        self.png_quality = png_quality
        self.video_path = video_path
        self.ascii_frames_path = ascii_frames_path
        self.text_frames_path = text_frames_path
        self.scale_factor = scale_factor
        self.one_char_width = one_char_width
        self.one_char_height = one_char_height
        self.character = character
        self.output_video_path = output_video_path
        self.intensity_level = intensity_level
        self.original_vid_ratio = original_vid_ratio
        self.output_audio_path = output_audio_name

    def extract_frames(
        self, save_path: str = None, video_path: str = None, png_quality: int = None
    ):
        if save_path == None:
            save_path = self.extract_frames_path
        if png_quality == None:
            png_quality = self.png_quality
        if video_path == None:
            video_path = self.video_path
        if video_path is None:
            cprint('[bright_red]ERROR: "video path" not provided')
            raise ArgumentError(error='ERROR: "video path" not provided')

        if not os.path.exists(save_path):
            os.makedirs(save_path)
            print("Directory Successfully Made!")

        (
            ffmpeg.input(video_path)
            .output(f"{save_path}/frame%d.png", q=png_quality, start_number=0)
            .run()
        )

    def get_video_fps(self, video_path: str = None) -> float:
        if video_path == None:
            video_path = self.video_path
        if video_path is None:
            cprint('[bright_red]ERROR: "video path" not provided')
            raise ArgumentError(error='ERROR: "video path" not provided')

        probe = ffmpeg.probe(video_path)
        video_info = next(
            stream for stream in probe["streams"] if stream["codec_type"] == "video"
        )

        duration = float(video_info["duration"])
        total_frames = int(video_info["nb_frames"])

        if duration > 0:
            fps = total_frames / duration
            return fps
        else:
            return None

    def getChar(
        self, input_int: int = None, character: str = None, intensity_level: int = None
    ) -> int:
        if input_int is None:
            cprint('[bright_red]ERROR: "input_int" not provided')
            raise ArgumentError(error='ERROR: "input_int" not provided')
        if character == None:
            character = self.character
        if intensity_level == None:
            intensity_level = self.intensity_level
        char_array = list(character)
        char_length = len(char_array)

        intensity_levels = intensity_level

        intensity_step = 256 / intensity_levels
        intensity_index = int(input_int / intensity_step)

        index = min(
            intensity_index * (char_length - 1) // intensity_levels, char_length - 1
        )
        return char_array[int(index)]

    def ascii_converter(
        self,
        extract_frames_path: str = None,
        ascii_frames_path: str = None,
        text_frames_path: str = None,
    ):
        if ascii_frames_path == None:
            ascii_frames_path = self.ascii_frames_path
        if text_frames_path == None:
            text_frames_path = self.text_frames_path
        if extract_frames_path == None:
            extract_frames_path = self.extract_frames_path
        try:
            os.makedirs(ascii_frames_path, exist_ok=True)
            os.makedirs(text_frames_path, exist_ok=True)
            print("Directories Successfully Made!\n")
        except OSError as e:
            print(f"Error: Creating directory of data - {e}\n")

        font = ImageFont.truetype("C:\\Windows\\Fonts\\lucon.ttf", 10)

        items_no = len(os.listdir(extract_frames_path))
        max_iter = items_no + 0

        for iteration in range(max_iter):
            text_file = open(f"{self.text_frames_path}/Text_Frame{iteration}.txt", "w")

            im = Image.open(f"{extract_frames_path}/frame{iteration}.png").convert(
                "RGB"
            )
            width, height = im.size
            im = im.resize(
                (
                    int(self.scale_factor * width),
                    int(
                        self.scale_factor
                        * height
                        * (self.one_char_width / self.one_char_height)
                    ),
                ),
                Image.NEAREST,
            )
            width, height = im.size
            pix = im.load()

            output_image = Image.new(
                "RGB",
                (self.one_char_width * width, self.one_char_height * height),
                color=(0, 0, 0),
            )
            d = ImageDraw.Draw(output_image)

            for i in range(height):
                for j in range(width):
                    r, g, b = pix[j, i]
                    h = int(r / 3 + g / 3 + b / 3)
                    char = self.getChar(h)
                    text_file.write(char)
                    d.text(
                        (j * self.one_char_width, i * self.one_char_height),
                        char,
                        font=font,
                        fill=(r, g, b),
                    )
                text_file.write("\n")

            output_image.save(f"{self.ascii_frames_path}/ascii_frame{iteration}.png")
            print(f"Ascii-Frame Converted- #{iteration}", end="\r")

    def get_video_dimensions(self, video_path: str = None) -> int:
        if video_path == None:
            video_path = self.video_path
        if video_path is None:
            cprint('[bright_red]ERROR: "video path" not provided')
            raise ArgumentError(error='ERROR: "video path" not provided')

        probe = ffmpeg.probe(video_path)
        video_info = next(
            (stream for stream in probe["streams"] if stream["codec_type"] == "video"),
            None,
        )

        if video_info:
            width = int(video_info["width"])
            height = int(video_info["height"])
            return width, height
        else:
            return None

    def img_seq_to_video(
        self,
        frames_seq_folder: str = None,
        output_video_path: str = None,
        vid_width: int = None,
        vid_height: int = None,
        fps: float = None,
        audio: str = None,
    ):
        if output_video_path == None:
            output_video_path = self.output_video_path
        if frames_seq_folder == None:
            frames_seq_folder = self.ascii_frames_path

        if not os.path.exists(frames_seq_folder):
            raise FileNotFoundError(f"Directory '{frames_seq_folder}' not found.")

        input_images_pattern = os.path.join(frames_seq_folder, "ascii_frame%d.png")

        if not os.path.exists(input_images_pattern % 0):
            raise FileNotFoundError(f"No image found in '{frames_seq_folder}'.")

        if fps == None:
            fps = self.get_video_fps()

        if vid_width == None and vid_height == None:
            width, height = self.get_video_dimensions()
        else:
            width = vid_width
            height = vid_height

        self.extract_audio()
        video = ffmpeg.input(input_images_pattern, framerate=fps)

        audio = ffmpeg.input(self.output_audio_path)
        (
            ffmpeg.output(
                video,
                audio,
                output_video_path,
                crf=18,
                vcodec="libx264",
                pix_fmt="yuv420p",
                vf=f"scale={width}:{height}, eq=saturation=2.5",
            )
            .overwrite_output()
            .run()
        )

    def extract_audio(
        self, input_video_path: str = None, output_audio_path: str = None
    ):
        if input_video_path == None:
            input_video_path = self.video_path
        if output_audio_path == None:
            output_audio_path = self.output_audio_path
        try:
            (
                ffmpeg.input(input_video_path)
                .output(output_audio_path, format="mp3")
                .overwrite_output()
                .run()
            )
            return True
        except:
            return False


# character="@%#*+=-:. "

if __name__ == "__main__":
    frame_path = r"D:\Ascii\sakura_video.mp4"
    convertor = Convertor(
        scale_factor=0.1, hardware_acceleration=True, video_path=frame_path
    )
    convertor.extract_frames()
    convertor.ascii_converter()
