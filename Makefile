.PHONY: all images

time := $(shell ffprobe -v error -select_streams v:0 -show_entries stream=duration -of default=noprint_wrappers=1:nokey=1 data/video.mp4)
time_up := $(shell printf "%.0f\n" $(time)) 

all: data/video.mp4 images data/transcript.json


data/video.mp4: data/video.MOV
	ffmpeg -i $< -qscale 0 $@

# This will break down the video into frames which can be analysed.
images: data/video.mp4
	mkdir -p frames
	ffmpeg -i $< -r 5 -f image2 frames/frame-%05d.jpg


audio: data/video.mp4
	ffmpeg -i $< -vn -acodec pcm_s16le -ar 44100 -f segment -segment_time 15 -ac 2 data/audio%03d.wav

data/transcript.json: audio
	curl -X POST "https://speech.platform.bing.com/speech/recognition/dictation/cognitiveservices/v1?language=en-us&format=detailed" -H "Transfer-Encoding: chunked" -H "Ocp-Apim-Subscription-Key: f745fdb731c84c25bfe437be220e0be6" -H "Content-type: audio/wav; codec=audio/pcm; samplerate=16000" --data-binary @data/audio000.wav >> $@ 

time: data/video.mp4
	echo $(time_up)

clean:
	rm -rf frames/
	rm data/transcript.json
	rm data/*.wav
	rm data/video.mp4
	
