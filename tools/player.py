import os
import time
from pygame import mixer

def player(text_file_path, music_file_path, fps, loop=True, num_loops=None):
    mixer.init()
    mixer.music.load(music_file_path)

    file_list = os.listdir(text_file_path)
    num_files = len([f for f in file_list if f.endswith('.txt')])

    if loop:
        if num_loops is None:
            num_loops = float('inf')
        else:
            num_loops = min(num_loops, float('inf'))
    else:
        num_loops = 1

    loop_count = 0
    while loop_count < num_loops:
        mixer.music.play()
        start_time = time.time()
        for i in range(num_files):
            with open(os.path.join(text_file_path, f"Text_Frame{i}.txt"), "r") as f:
                file_contents = f.read()
                print(file_contents)

            # Calculate the duration of each frame
            elapsed_time = time.time() - start_time
            frame_duration = (i + 1) * (1 / fps) - elapsed_time

            if frame_duration > 0:
                time.sleep(frame_duration)

        loop_count += 1
        
        
if __name__ == "__main__":
    text_files_path = r"D:\Ascii\text-frame"
    music_file_path = r"D:\Ascii\output-audio.mp3"
    fps = 60
    player(text_files_path, music_file_path, fps, loop=True)