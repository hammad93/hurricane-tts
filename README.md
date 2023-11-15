# hurricane-tts
A repository hosting code to produce text to speech with deep learning and large language models on the topic of tropical storms. The notebook is deployed part of hourly reports, please reference `hurricane-deploy` for details. The deployment is designed to be serverless through container registries and constainer instances or services. 

# Install (Linux)
Please note that this repository may need a Redis database setup with the appropriate connection parameters. We can open up the notebook and go from there or we can utilize a local containerized environment.

## Docker

```bash
cd docker
docker build -t hurricane-tts --build-arg AZURE_OPENAI_API_KEY=🔑 --build-arg AZURE_REDIS_KEY=🔑 .
docker run -it hurricane-tts
```

# Quickstart
When you have setup a compute environment with a GPU and access to a Jupyter
Notebook, we can utilize `hurricane_tts.ipynb` to generate the audio in 
production. It will produce examples, [click here for a previous output example](https://github.com/hammad93/hurricane-tts/issues/2#issuecomment-180639837). Note that this requires additional setup.
