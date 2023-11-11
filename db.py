import redis
import config
import os
import json

def redis_client():
  '''
  Returns the client based on current configurations
  '''
  return redis.StrictRedis(host = config.redis_host,
                          password = os.environ['AZURE_REDIS_KEY'],
                          port = config.redis_port,
                          ssl = True)
def upload_audio(path):
  '''
  Given, the path, this will upload it to the database
  '''
  filename = path.split('/')[-1]
  with open(path, 'rb') as f:
    data = f.read()
  r = redis_client()
  r.set(filename, data)

def upload_latest_audios(paths):
  '''
  Given the paths of the audio files, we will create other data structures
  '''
  r = redis_client()
  
  # create metadata structure
  metadata = [{
     'filename': path.split('/')[-1],
     'storm': path.split('/')[-1][:-4].split('_')[0],
     'timestamp': path.split('/')[-1][:-4].split('_')[1],
     'language': path.split('/')[-1][:-4].split('_')[2]
  } for path in paths]
  r.set(config.redis_latest_audio_key, json.dumps(metadata))

  # finally, upload audio files
  for path in paths:
     upload_audio(path)
