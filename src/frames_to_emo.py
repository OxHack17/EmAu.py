# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 22:29:19 2017

@author: cq
"""
import os
import numpy as np
import time 
import requests
import cv2
import operator
import numpy as np
from __future__ import print_function

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
			api_result.append(processRequest( json, data, headers, params ))
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

def frames_to_change(frames_dir, frames_before, frames_after):    
    paths_before = frames_to_paths(frames_dir, frames_before)
    paths_after = frames_to_paths(frames_dir, frames_after)
    result_before = paths_to_emo(paths_before)
    result_after = paths_to_emo(paths_after)
    emo_before = mean_emo(result_before)
    emo_after = mean_emo(result_after)
    emo_change = emo_after-emo_before
    return emo_change
    
frames_to_change("C:/hack/project/frames_fake",range(1,6),range(5,11))  

#a = paths_to_emo(frames_to_paths("C:/hack/project/frames_fake",[1,2,3,4,5])
#print(a)
#b = mean_emo()


