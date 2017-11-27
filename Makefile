.PHONY: all images

time := $(shell ffprobe -v error -select_streams v:0 -show_entries stream=duration -of default=noprint_wrappers=1:nokey=1 data/video.mp4)
time_up := $(shell printf "%.0f\n" $(time)) 

all: data/video.mp4 images audio


data/video.mp4: data/video.MOV
	ffmpeg -i $< -qscale 0 $@

# This will break down the video into frames which can be analysed.
images: data/video.mp4
	mkdir -p frames
	ffmpeg -i $< -r 1 -f image2 frames/frame-%05d.jpg


audio: data/video.mp4
	ffmpeg -i $< -vn -acodec pcm_s16le -f segment -segment_time 5 -ac 2 data/audio%03d.wav

data/data.json: audio
	python3 src/transcribe.py 
	
time: data/video.mp4
	echo $(time_up)

clean:
	rm -rf frames/
	rm data/transcript.json
	rm data/*.wav
	rm data/video.mp4
	
