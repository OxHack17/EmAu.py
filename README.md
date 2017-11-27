# Emotion Augmentation by Key Words and Phrases
### Using Microsoft Cognitive Services to find words which alter emotional response in doctor-patient interactions. 

**Authors**: Chris Eijsbouts (@cqgd), Chris Cole (@Chris1221), Wilder Wohns (@awohns).

This project was created as a part of [Oxford Hack 2017](http://oxfordhack.com/) as a part of the Microsoft Cognitive API challenge. 

#### Short Description

As a part of medical education, students recieve precious little genuine interaction with patients in which to try different approaches to delivering bad news. Time spent with simulated patients is expensive and limited by class sizes, and interactions with real patients are high-stakes and high-stress. We aim to combat this by quantitatively analyzing doctor-patient interactions using the Microsoft Cognitive services API to better understand how key words and phrases influence emotional reponse. Our software provides a change value for each of the 8 orthogonal traits retrieved by Microsoft from raw video files which can be used in further analysis. At large n this approach may lend itself to predictive approaches and further software development centering around understand how doctor's delivery of clinical information influences patient's reactions. 

### Quick Start

For a quick analysis using default options, place the video file named `video.MOV` in the `data/` directory, and invoke

```
make
```

That's it! Our software will:

- Break the video into frames
- Send the frames to Microsoft API for emotional analysis
- Extract audio from the video and chunk into sensible pieces
- Transcribe the audio
- Perform Sentiment analysis on the transcript (TODO) 
- Weave together the audio and video time stamps and derive "delivery" and "response" periods
- Find the change in emotion state betwee these periods. 

This will be written into a JSON file at `results/response.json` for further analysis by researchers. 

### More information

Please see `src/` for the code, which we have made every effort to be as readable as possible.  

---

© `$AUTHORS`, MIT License 


