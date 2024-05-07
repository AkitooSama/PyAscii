import cv2
import numpy as np


def image_to_video(input_image_path, output_video_path, duration_sec=5, fps=10):
    # Load the input image
    image = cv2.imread(input_image_path)

    # Get image width and height
    height, width, _ = image.shape

    # Define video codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(
        *"mp4v"
    )  # Video codec (can be changed based on file extension)
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    # Write the image frames to the video for the specified duration
    for _ in range(int(duration_sec * fps)):
        out.write(image)  # Write the same image frame for each frame of the video

    # Release VideoWriter and close the output video file
    out.release()


# Example usage
input_image_path = (
    r"C:\Users\DigiTronic\Downloads\backiee-84981-landscape.jpg"
)
output_video_path = "sakura_video.mp4"
image_to_video(input_image_path, output_video_path, duration_sec=2, fps=10)
