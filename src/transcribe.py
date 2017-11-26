import speech_recognition as sr
import os, glob
import pandas as pd
import pprint as pp

frame_rate = 1

df = pd.DataFrame(columns = ['time.start', 'time.end','frame.start', 'frame.end', 'text'])


for filename in glob.glob("../data/*.wav"):
    print(filename)

    from os import path
    AUDIO_FILE = "../data/" + filename

    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source) # read the entire audio fileA

    BING_KEY="f745fdb731c84c25bfe437be220e0be6"

    try:
        text = r.recognize_bing(audio, key=BING_KEY)
    except sr.UnknownValueError:
        text = ""    
    except sr.RequestError as e:
        print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e)) 

    # Parse the file name

    id = int(os.path.splitext(os.path.basename(filename))[0][5:])

    d = {'time.start': [max(5*id-5, 0)], 'time.end': [5*id], 'frame.start': [frame_rate*5*id - 5], 'frame.end': [frame_rate*5*id], 'text': [text]}
    df2 = pd.DataFrame(data = d) 
    #pp.pprint(df2)

    df = df.append(df2) 
 
df.to_json("../data/data.json", orient = "table")
