import utils

def lang_list():
    langs = utils.tts_langs()
    return set(x['Language Name'])