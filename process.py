import sys
import time

from PIL import Image
from io import BytesIO
import cv2
import numpy




FPS = 10
SPF = 0.1



def make_image(data):
    img_buf = numpy.frombuffer(data, numpy.uint8) 
    img = cv2.imdecode(img_buf, cv2.IMREAD_COLOR)
    return img


def add_frame(video_writer, data):
    img = make_image(data)
    video_writer.write(img)


def round_special(number, increment):
    mod = number // increment
    up = (mod + 1) * increment
    down = mod * increment

    if up - number > number - down:
        return down
    else:
        return up
    
    
def process_video(video):
    video_writer = cv2.VideoWriter("out.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 20, (1920, 1080))

    # get jpgs from file
    jpgs = []

    while True:
        # verify file integrity
        try:
            time = float(video.readline())
            length = int(video.readline())
        except:
            if video.read(2) == b"":
                break
            else:
                print("Malformed File!")
                exit()
        
        # get data
        data = video.read(length) 
        jpgs.append((time, data))

    # jpgs to mp4
    frame = 0
    jpg_num = 0
    jpg_time = 0

    while True:
        if jpg_num >= len(jpgs):
            break

        time = round(SPF * frame, 3)
        jpg_time = round(round_special(jpgs[jpg_num][0], SPF), 3)

        if jpg_time == time:
            print("Frame: " + str(frame))
            add_frame(video_writer, jpgs[jpg_num][1])
            jpg_num += 1
            frame += 1
        elif jpg_time > time:
            print("Frame: " + str(frame))
            add_frame(video_writer, jpgs[max(jpg_num - 1, 0)][1])
            frame += 1
        elif jpg_time < time:
            jpg_num += 1

    video_writer.release()


def main(argv):
    try:
        video_file = argv[0]
        audio_file = argv[1]
    except:
        print("Usage: process.py <videofile>")
        return

    video = open(video_file, "rb")

    process_video(video)    

    video.close()



if __name__ == "__main__":
    main(sys.argv[1:])
