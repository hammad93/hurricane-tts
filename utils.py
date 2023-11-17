import config

import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO
import redis
import os
import json

def supported_langs_df(url):
    '''
    Returns the currently support langs based on the website.
    '''
    # Make a request to the website
    r = requests.get(url)
    
    # Raise an exception if the request was unsuccessful
    r.raise_for_status()
    
    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # Find the first table in the HTML
    table = soup.find('table')
    
    # Read the table into a Pandas DataFrame
    table_html = StringIO(str(table))
    df = pd.read_html(table_html, encoding='utf-8')[0]
    
    return df

def tts_langs():
    '''
    Provides a list of language codes in a Dataframe
    '''
    all_supported = supported_langs_df(config.supported_langs_html)
    tts_supported = all_supported.query('TTS.notna()')
    # supported_langs_out_cols specifies which columns should be output
    return tts_supported[config.supported_langs_out_cols]

def transform_storm_data():
    '''
    Takes in the data from the API and transforms it.
    '''
    track = requests.get(config.api_url_track).json()
    forecast = requests.get(config.api_url_forecast).json()

    # create data structure to return the storms lat lons and whether
    # it's history or forecast
    results = {}

    # merge data sources into one data structure
    for record in track :
        entry = {
            'type' : 'history',
            'lat' : record['lat'],
            'lon' : record['lon'],
            'time' : record['time'],
            'wind_speed' : record['wind_speed'] # knots
        }
        if record['id'] not in results.keys() :
            results[record['id']] = [entry]
        elif len(results[record['id']]) < config.max_storm_history :
            results[record['id']].append(entry)
    for record in forecast :
        entry = {
            'type' : 'forecast',
            'lat' : record['lat'],
            'lon' : record['lon'],
            'time' : record['time'],
            'wind_speed' : record['wind_speed'] # knots
        }
        # there shouldn't be forecasts for a storm that's not there
        results[record['id']].append(entry)
    
    return results

def llm_response_transform(resp, supported_langs, num_langs = 2):
  '''
  The response is supposed to be a list at least 2 delimited by a comma.
  This function takes in the raw text and returns the Python data structure.

  Input
  -----
  resp string
    The response text from the large language model, e.g. ChatGPT
  supported_langs list[string]
    Each item in the response list has to be also in this list
  Output
  -----
  list or False
    A list of size 3 or False if its invalid
  '''
  try: # see if it can be loaded like python or json
      langs = eval(resp)
      print(langs)
  except Exception as e:
      print(e)
      # cleans string by removing spaces and .'s
      langs = resp.strip().replace(" ","").replace(".","").split(',')
      print(langs)
  if len(langs) <= num_langs: # e.g. needs to be 3 languages
      return False
  for lang in langs: # check if its supported
      if lang not in supported_langs:
          print(f'{lang} is not in the supported language list.')
          return False
  return langs
