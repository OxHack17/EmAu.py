.PHONY: all images

all: images data/transcript.json

# This will break down the video into frames which can be analysed.
images: data/video.mp4
	mkdir -p frames
	ffmpeg -i $< -r 5 -f image2 frames/frame-%05d.jpg


data/audio.wav: data/video.mp4
	ffmpeg -i $< -vn -acodec pcm_s16le -ar 44100 -ac 2 $@

data/transcript.json: data/audio.wav
	curl -X POST "https://speech.platform.bing.com/speech/recognition/dictation/cognitiveservices/v1?language=en-us&format=detailed" -H "Transfer-Encoding: chunked" -H "Ocp-Apim-Subscription-Key: f745fdb731c84c25bfe437be220e0be6" -H "Content-type: audio/wav; codec=audio/pcm; samplerate=16000" --data-binary @$<

clean:
	rm -rf frames/
	
