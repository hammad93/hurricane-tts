import redis
import config
import os
import json
import boto3

def upload_file_s3(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        with open(file_name, "rb") as f:
           response = s3_client.upload_obj(f, bucket, file_name.split('/')[-1])
           print(response.content)
    except Exception as e:
        print(e)
        return False
    return True

def download_file_s3(file_name, bucket, path):
  '''
  Parameters
  ----------
  path string
    In order to have space, we check if we have already downloaded it in this path
   
  '''
  # check if we have already downloaded it and can pass the data
  
  full_path = path + file_name
  if os.path.exists(full_path):
     print('The file exists already')
  else:
     # download the file
     s3 = boto3.client('s3')
     s3.download_file(bucket, file_name, full_path)

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

def upload_latest_audios(paths, metadata):
  '''
  Given the paths of the audio files, we will create other data structures
  '''
  r = redis_client()
  
  # create metadata structure
  metadata = [{
     'filename': path.split('/')[-1],
     'storm': path.split('/')[-1][:-4].split('_')[0],
     'timestamp': path.split('/')[-1][:-4].split('_')[1],
     'language': path.split('/')[-1][:-4].split('_')[2],
     'metadata': metadata[path]
  } for path in paths]
  r.set(config.redis_latest_audio_key, json.dumps(metadata))

  # finally, upload audio files
  for path in paths:
     upload_file_s3(path, config.s3_audio_bucket)
