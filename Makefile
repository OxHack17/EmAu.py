.PHONY: all images

all: images

# This will break down the video into frames which can be analysed.
images: data/video.mp4
	mkdir -p frames
	ffmpeg -i $< -r 20 -f image2 frames/frame-%05d.jpg

clean:
	rm -rf frames/
	
