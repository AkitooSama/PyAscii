import os
from rich import print as cprint
from PIL import Image, ImageDraw, ImageFont
import ffmpeg


class Convertor:
    def __init__(
        self,
        video_path,
        output_video_path="output-video.mp4",
        output_audio_path="output-audio.mp3",
    ):
        self.video_path = video_path
        self.output_video_path = output_video_path
        self.output_audio_path = output_audio_path

    def extract_frames(self, extract_frames_path="extracted-frames", png_quality=1):
        if not os.path.exists(extract_frames_path):
            os.makedirs(extract_frames_path)

        (
            ffmpeg.input(self.video_path)
            .output(f"{extract_frames_path}/frame%d.png", q=png_quality, start_number=0)
            .run()
        )

    def ascii_converter(
        self, extract_frames_path="extracted-frames", ascii_frames_path="ascii-frame"
    ):
        if not os.path.exists(ascii_frames_path):
            os.makedirs(ascii_frames_path)

        char_array = (
            "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[
                ::-1
            ]
        )
        font = ImageFont.load_default()

        for i, filename in enumerate(os.listdir(extract_frames_path)):
            image = (
                Image.open(os.path.join(extract_frames_path, filename))
                .convert("L")
                .resize((120, 68))
            )
            pixels = image.getdata()
            ascii_image = ""
            for p in pixels:
                ascii_image += char_array[int(p / 32)]
                if len(ascii_image) % 120 == 0:
                    ascii_image += "\n"

            # Create an image with the ASCII art
            ascii_img = Image.new("RGB", (120, 68), color=(0, 0, 0))
            draw = ImageDraw.Draw(ascii_img)
            draw.text((0, 0), ascii_image, font=font, fill=(255, 255, 255))

            # Save the ASCII art image
            ascii_img.save(os.path.join(ascii_frames_path, f"ascii_frame{i}.png"))
            print(f"Ascii-Frame Converted- #{i}", end="\r")

    def img_seq_to_video(self, ascii_frames_path="ascii-frames", fps=60):
        input_images_pattern = os.path.join(ascii_frames_path, "ascii_frame%d.png")

        video = ffmpeg.input(input_images_pattern, format="image2", framerate=fps)
        audio = (
            ffmpeg.input(self.video_path)
            .audio.filter("aformat", sample_fmts="s16:48000")
            .output(self.output_audio_path, format="mp3")
        )

        ffmpeg.concat(video, audio, v=1, a=1).output(
            self.output_video_path, crf=18, vcodec="libx264", pix_fmt="yuv420p"
        ).overwrite_output().run()


if __name__ == "__main__":
    frame_path = r"D:\Ascii\sakura_video.mp4"
    convertor = Convertor(video_path=frame_path)
    convertor.extract_frames()
    convertor.ascii_converter()
    # convertor.img_seq_to_video()
