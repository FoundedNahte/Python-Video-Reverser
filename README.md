# Python-Video-Reverser

To reverse videos, one common solution is to simply use ffmpeg's "reverse" filter.

However, since ffmpeg buffers the entire video into memory, a large video file can overload memory and crash the program.

This python program utilizes parallel processing and ffmpeg to splice the target video into chunks, reverse them, and compile it all back into a reversed video.



## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install required modules.

```bash
pip install -r requirements.txt
```

## Usage

**reverse.py has two ways of running (Both can utilize command line arguments):**

**1. Terminal Drop Down Menu:**
```
Enter mp4 file to reverse:
a: input.mp4
b: input2.mp4
>
```
**2. Command Line Arguments:**

**Optional Flags:**
```
-step [] : change time interval of subclips (default = 10 seconds)
-cpu [] : change number of cores to be used (default = highest amount available)
-i [] : Input Video Path
-o [] : Output file Path
```

**Examples:**

```
python reverse.py -i input.mp4 -o output.mp4

python reverse.py -step 5 -cpu 2

python reverse.py -o output.mp4 -step 2

python reverse.py -i input.mp4 -o output.mp4 -step 5 -cpu 4
```

**Notes:**

*Mores cores = more memory used in execution 

*Higher step = more memory used in execution

*You are able to pass in the input or output video path independently.


