import utils
import os
import config
import openai

def unique_lang_list(col = 'Language Name'):
    langs = utils.tts_langs()
    return set(langs[col])

def generate_prompts():
    # extract and transform data structures
    langs = unique_lang_list()
    storms = utils.transform_storm_data()

    # load prompts
    with open('prompts/system-prompt.txt', 'r') as file:
        system_prompt = file.read()
    with open('prompts/localization-prompt.txt', 'r') as file:
        localization_prompt = file.read()
    
    # transform data into prompts
    system = system_prompt.format(langs=langs)
    localizations = [localization_prompt.format(storm=storms[storm]) for storm in storms]

    return {
        'system' : system,
        'storms' : localizations,
    }

def chat(message, history=None, system=None):
    '''
    Parameters
    ----------
    message string
        The prompt to send to the large language model
    history list (default None, optional)
        A list of messages corresponding to the chat history.
    system string (optional)
        The system prompt for the large language model
    '''    
    prompt = {
        "role" : "user",
        "content" : message
    }

    if history :
        messages = history + [prompt]
    else :
        messages = [
            {
                "role" : "system",
                "content" : system if system else config.default_system
            },
            prompt
        ]
    
    # gets the API Key from environment variable AZURE_OPENAI_API_KEY
    # https://learn.microsoft.com/en-us/azure/ai-services/openai/reference#rest-api-versioning
    # https://learn.microsoft.com/en-us/azure/cognitive-services/openai/how-to/create-resource?pivots=web-portal#create-a-resource
    print(f"Here are the constructed messages: {messages}")
    client = openai.AzureOpenAI(
        api_version="2023-07-01-preview",
        azure_endpoint="https://live.openai.azure.com/",
    )

    return client.chat.completions.create(
        model="live",
        messages = messages
    ).choices[0].message.content
