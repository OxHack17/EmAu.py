.PHONY: all images

all: images

# This will break down the video into frames which can be analysed.
images: data/video.mp4
	mkdir -p frames
	ffmpeg -i $< -r 5 -f image2 frames/frame-%05d.jpg

audio:

clean:
	rm -rf frames/
	
