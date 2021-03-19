import os
import subprocess
import argparse
from moviepy.editor import VideoFileClip
from multiprocessing import Pool
import shutil
import time
# input file path, start, calculated time step

ffmpeg_path = "ffmpeg/ffmpeg"
def reverseVideo(_input, step, duration, start):
    #ori = VideoFileClip(_input) 
    #temp = ori.subclip(start, step)
    print(_input)
    print(str(step))
    print(str(start))
    remain = duration % 10
    if step % 10== 0:
        position = (duration - remain) - start
    else:
        position = 0
    #temp.write_videofile("temp/"+str(start)+".mp4")
    temp = "temp/"+str(start)+".mp4"
    p = subprocess.Popen(f"{ffmpeg_path} -ss {start} -i \"{_input}\" -c copy -t {step} {temp} -y")
    p.wait()
    print("done")
    temp2 = "temp/"+str(position)+"temp.mp4" 
    p2 = subprocess.Popen(f"{ffmpeg_path} -i {temp} -vf reverse -af areverse {temp2} -y")
    p2.wait()
    os.remove(temp)

def inputs(i_bool, o_bool):
    if(i_bool == None and not o_bool == None):
        fileList = os.listdir()
        mp4_list = []
        for f in fileList:
            if(".mp4" in f):
                mp4_list.append(f)
        print("Press letter of mp4 file to invert")

        for i in range(len(mp4_list)):
            print(chr(97+i)+": "+mp4_list[i])

        index = input()
        _input = mp4_list[ord(index)-97]
        return _input, o_bool
    elif(o_bool == None and not i_bool == None):
        print("Enter path for output mp4")
        _output = input()
        return i_bool, _output
    else:
        fileList = os.listdir()
        mp4_list = []
        for f in fileList:
            if(".mp4" in f):
                mp4_list.append(f)
        print("Press letter of mp4 file to invert")

        for i in range(len(mp4_list)):
            print(chr(97+i)+": "+mp4_list[i])

        index = input()
        _input = mp4_list[ord(index)-97]
        print("Enter path for output mp4")
        _output = input()
        return _input, _output

def reverseAudio(_input):
    p1 = subprocess.Popen(f"ffmpeg -i {_input} -vn -ar 44100 -ac 2 -ab 192k -f mp3 temp/temp_audio.mp3")
    p1.wait()


if __name__ == "__main__": 
    
    start_time = time.time()

    if os.path.isdir("temp/"):
        shutil.rmtree("temp/")
    os.mkdir("temp/")
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", action="store", dest="input", metavar = "input path", type = str, help = "path to input file", default=None)
    parser.add_argument("-o", action="store", dest="output", metavar = "output path", type = str, help = "path for output file", default=None)
    parser.add_argument("-cpu", action="store", dest="cpu_num", type = str, help="Number of CPU cores to use", default=str(os.cpu_count()))
    parser.add_argument("-step", action="store", dest="_step", type = str, help="time interval of subclips; lower number = less memory used and larger execution time", default=str(10))

    args = parser.parse_args()
    _input = args.input
    _output = args.output
    _processes = int(args.cpu_num)
    temp_videos = []
    
    if(_input == None or _output == None):
        _input, _output = inputs(_input, _output)

    input_video = VideoFileClip(_input)
    step = int(args._step)
    _times = []
    print(step)
    print(_input)
    print(_output)
    print(_processes)
    counter = 0
    _remain = input_video.duration - counter
    while step < _remain:
        _times.append(counter)
        counter += step
        _remain = input_video.duration - counter
    _times.append(input_video.duration - _remain)
    arguments = []
    for time in _times:
        if time == _remain:
            step = input_video.duration-counter
        arguments.append((_input, step, input_video.duration, time))
    with Pool(_processes) as pool:
        video_parts = pool.starmap(reverseVideo, arguments)
    with open("temp/temp.txt", "w+") as out_file:
        parts = os.listdir("temp/")
        parts.remove("temp.txt")
        cases = {}
        for i in range(0, len(parts)):
            cases[int(parts[i].split('.')[0])] = parts[i]
        parts = []
        list(cases.keys())
        for key in sorted(list(cases.keys())):
            parts.append(cases.get(key))
        for i in range(0, len(parts)):
            out_file.write("file "+"'"+parts[i]+"'"+"\n")
    _p = subprocess.Popen(f"{ffmpeg_path} -f concat -i temp/temp.txt -c copy {_output} -y")
    _p.wait()
    try:
        shutil.rmtree("temp/")
        print(f"--- {time.time() - start_time()} seconds ---")
    except Exception as e:
        pass

