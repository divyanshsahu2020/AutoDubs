from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
from transformers import pipeline
import pandas as pd
def convert(orignal_text,destination_lang):
    lang_dict = {'afrikaans': 'af', 'amharic': 'am', 'arabic': 'ar', 'asturian': 'ast', 'azerbaijani': 'az',
                 'bashkir': 'ba', 'belarusian': 'be', 'bulgarian': 'bg', 'bengali': 'bn', 'breton': 'br',
                 'bosnian': 'bs', 'catalan valencian': 'ca', 'cebuano': 'ceb', 'czech': 'cs', 'welsh': 'cy',
                 'danish': 'da', 'german': 'de', 'greeek': 'el', 'english': 'en', 'spanish': 'es', 'estonian': 'et',
                 'persian': 'fa', 'fulah': 'ff', 'finnish': 'fi', 'french': 'fr', 'western frisian': 'fy',
                 'irish': 'ga', 'gaelic scottish gaelic': 'gd', 'galician': 'gl', 'gujarati': 'gu', 'hausa': 'ha',
                 'hebrew': 'he', 'hindi': 'hi', 'croatian': 'hr', 'haitian; haitian creole': 'ht', 'hungarian': 'hu',
                 'armenian': 'hy', 'indonesian': 'id', 'igbo': 'ig', 'iloko': 'ilo', 'icelandic': 'is', 'italian': 'it',
                 'japanese': 'ja', 'javanese': 'jv', 'georgian': 'ka', 'kazakh': 'kk', 'central khmer': 'km',
                 'kannada': 'kn',
                 'korean': 'ko', 'luxembourgish letzeburgesch': 'lb', 'lingala': 'ln', 'lao': 'lo', 'lithuanian': 'lt',
                 'latvian': 'lv', 'malagasy': 'mg', 'macedonian': 'mk', 'malayalam': 'ml', 'mongolian': 'mn',
                 'marathi': 'mr',
                 'malay': 'ms', 'burmese': 'my', 'nepali': 'ne', 'dutch; flemish': 'nl', 'norwegian': 'no',
                 'northern sotho': 'ns',
                 'occitan': 'post 1500', 'oriya': 'or', 'panjabi; punjabi': 'pa', 'polish': 'pl', 'pashto': 'ps',
                 'portuguese': 'pt',
                 'romanian; moldavian; moldovan': 'ro', 'russian': 'ru', 'sindhi': 'sd', 'sinhala; sinhalese': 'si',
                 'slovak': 'sk',
                 'slovenian': 'sl', 'somali': 'so', 'albanian': 'sq', 'serbian': 'sr', 'swati': 'ss', 'sundanese': 'su',
                 'swedish': 'sv',
                 'swahili': 'sw', 'thai': 'th', 'tagalog': 'tl', 'tswana': 'tn', 'turkish': 'tr', 'ukrainian': 'uk',
                 'urdu': 'ur', 'uzbek': 'uz',
                 'vietnamese': 'vi', 'wolof': 'wo', 'xhosa': 'xh', 'yiddish': 'yi', 'yoruba': 'yo', 'chinese': 'zh',
                 'zulu': 'zu'}
    if not destination_lang.lower() in lang_dict:
        return pd.DataFrame([])
    orignal_text=list(orignal_text)
    code=lang_dict[destination_lang.lower()]
    pipe=pipeline(task='text2text-generation',model="facebook/m2m100_418M")
    for i in range(len(orignal_text)):
        orignal_text[i] = pipe(orignal_text[i],forced_bos_token_id=pipe.tokenizer.get_lang_id(code))[0]['generated_text']
    return pd.DataFrame(orignal_text)