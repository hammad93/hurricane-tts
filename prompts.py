import utils

def lang_list(col = 'Language Name'):
    langs = utils.tts_langs()
    return set(x[col])

def generate_prompts():
    # extract and transform data structures
    langs = lang_list()
    storms = utils.transform_storm_data()