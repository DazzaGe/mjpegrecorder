import requests
import sys
import threading
import time




def get_video(link):
    location = link + "/video"
    r = requests.get(location, stream=True)
    start_time = time.time()
    video_file = open("out.mjpeg", "ab")

    r = r.raw
    while True:
        # verify chunk integrity
        chunk = r.read(128)
        lines = chunk.split(b"\r\n")

        assert len(lines) > 5, "Malformed response"
        assert lines[1].startswith(b"--"), "Malformed response"
        assert lines[2].startswith(b"Content-Type"), "Malformed response"
        assert lines[3].startswith(b"Content-Length"), "Malformed response"
        assert lines[5].startswith(b"\xFF\xD8\xFF\xE0")

        # get data
        data_pos = chunk.find(b"\xFF\xD8\xFF\xE0")
        length = int(lines[3][16:]) - (128 - data_pos)

        data = chunk[data_pos:] + r.read(length)
        print("JPG Received!")

        # store data
        data = bytes(str(time.time() - start_time), "ascii") + b"\n" + lines[3][16:] + b"\n" + data
        video_file.write(data)
        
    video_file.close()



def main(argv):
    try:
        ip = argv[0]
        out = argv[1]
    except:
        print("Usage: record.py <ip:port> <outfile>")
        return
    
    link = "http://" + ip

    get_video(link)



if __name__ == "__main__":
    main(sys.argv[1:])
