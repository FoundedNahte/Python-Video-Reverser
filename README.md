# Python Video Reverser
 
To reverse videos, one common solution is to simply use ffmpeg's "reverse" filter. However, since ffmpeg buffers the the entire video into memory, memory is overloaded and the program crashes. This python program utilizes parallel processing to splice the target video into chunks, reverse them, and compile it all back together into a reversed video.