# hurricane-tts
A repository hosting code to produce text to speech with deep learning and large language models on the topic of tropical storms.

# Install
Linux, Windows, MacOS, Android

1. Please install the latest Python 3 and Pip.
2. Clone the repository and navigate into the directory.
3. Set the `AZURE_OPENAI_API_KEY` and `AZURE_REDIS_KEY`.
4. Open up a terminal with the latest Python and Pip in the path and enter in the following,

```
pip install -r requirements.txt
```

It's also recommended to run the tests to make sure everything is working.
If we execute `python test.py`, it will run the unit and integration tests.

# Quickstart
When you have setup a compute environment with a GPU and access to a Jupyter
Notebook, we can utilize `hurricane_tts.ipynb` to generate the audio in 
production. It will produce examples, [click here for a previous output example](https://github.com/hammad93/hurricane-tts/issues/2#issuecomment-180639837). Note that this requires additional setup.

# Docker

```bash
cd docker
docker build -t hurricane-tts --build-arg AZURE_OPENAI_API_KEY=🔑 --build-arg AZURE_REDIS_KEY=🔑 .
docker run -it hurricane-tts
```