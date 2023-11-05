import config

import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO

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