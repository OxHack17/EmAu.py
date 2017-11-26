from __future__ import print_function
import numpy as np
import time 
import requests
import cv2
import operator
import pandas as pd
import glob, os
import speech_recognition as sr
import pprint as pp

_url = 'https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize'
_key = 'e0ca0fede7a6421a90d27dfec5fb008f'
_maxNumRetries = 10

#%%
def frames_to_paths(frames_dir, frames):
    paths = []
    for frame in frames: 
        paths.append(frames_dir + "/frame-" + format(frame,'05') + '.jpg')
    return paths
#%%
    
#%%
def processRequest( json, data, headers, params ):

    """
    Helper function to process the request to Project Oxford

    Parameters:
    json: Used when processing images from its URL. See API Documentation
    data: Used when processing image read from disk. See API Documentation
    headers: Used to pass the key information and the data type request
    """

    retries = 0
    result = None

    while True:

        response = requests.request( 'post', _url, json = json, data = data, headers = headers, params = params )

        if response.status_code == 429: 

            print( "Message: %s" % ( response.json()['error']['message'] ) )

            if retries <= _maxNumRetries: 
                time.sleep(1) 
                retries += 1
                continue
            else: 
                print( 'Error: failed after retrying!' )
                break

        elif response.status_code == 200 or response.status_code == 201:

            if 'content-length' in response.headers and int(response.headers['content-length']) == 0: 
                result = None 
            elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str): 
                if 'application/json' in response.headers['content-type'].lower(): 
                    result = response.json() if response.content else None 
                elif 'image' in response.headers['content-type'].lower(): 
                    result = response.content
        else:
            print( "Error code: %d" % ( response.status_code ) )
            print( "Message: %s" % ( response.json()['error']['message'] ) )

        break
        
    return result
#%%
    
#%%    
def paths_to_emo(paths):
	headers = dict()
	headers['Ocp-Apim-Subscription-Key'] = _key
	headers['Content-Type'] = 'application/octet-stream'

	json = None
	params = None

	api_result = []
	for path in paths:
		with open(path, 'rb' ) as f:
		    data = f.read()
                    try: 
			api_result.append(processRequest( json, data, headers, params ))
                        break
                    except: ValueError
                            
	return api_result
#%%


#%%
def mean_emo(result):
    sum_all = np.zeros(len(result[0][0]['scores']))
    for frame in result:
        x =  frame[0]['scores'].values() 
        a = np.fromiter(iter(x), dtype=float)
        sum_all = sum_all + a
    mean_of_frames = sum_all/len(result)
    return mean_of_frames
#%%

#%%
def frames_to_change(frames_dir, frames_before, frames_after):    
    paths_before = frames_to_paths(frames_dir, frames_before)
    paths_after = frames_to_paths(frames_dir, frames_after)
    result_before = paths_to_emo(paths_before)
    result_after = paths_to_emo(paths_after)
    emo_before = mean_emo(result_before)
    emo_after = mean_emo(result_after)
    emo_change = emo_after-emo_before
    return emo_change
  
#%%  
#shit just works
#frames_to_change("frames_fake",range(1,6),range(5,11))  
#%%

# This generates the time stamps and words

def process_audio(path = "../data/", frame_rate = 1):

    df = pd.DataFrame(columns = ['frame.before.start','frame.start', 'frame.end', 'frame.after.end', 'time.start', 'time.end', 'text', 'id'])

    for filename in glob.glob(path +"*.wav"):
        print(filename)

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

        d = {'frame.before.start': [max(5*id-5, 0)], 'frame.start': [max(5*id, 0)], 'frame.end': [5*id+5], 'frame.after.end': [5*id+10], 'time.start': [max(frame_rate*5*id, 0)], 'time.end': [frame_rate*5*id+5], 'text': [text], 'id': [id]}
        df2 = pd.DataFrame(data = d) 
        #pp.pprint(df2)

        df = df.append(df2) 
        
    df.sort_values(by = "frame.start", inplace = True)
    df.reset_index(drop = True, inplace = True) 
    return df
      

#take cole's data
#x = pd.DataFrame(np.random.randn(6,4), columns=list("ABCD"))
x = process_audio()

pp.pprint(x)

#add emotion columns
emo_names = ['happiness', 'sadness', 'neutral', 'anger', 'surprise', 'disgust', 'contempt', 'fear']
for n, t in enumerate(emo_names):    
    x[t] = None    
#print(x)

#fill 'em up row by row    
for k, v in x.iterrows():
    set_before = list(range(v["frame.before.start"], v["frame.start"] + 1)) 
    set_after = list(range(v["frame.end"], v["frame.after.end"] + 1))
    x.loc[k,emo_names] = frames_to_change("../frames",set_before, set_after)
    #print(v)
    print("\n" + str(k) + ":")
    print(set_before)
    print(set_after)
    #print(v["frame.start"])
    #print(v["frame.end"])

#print(x)
