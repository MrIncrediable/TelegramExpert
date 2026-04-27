from .memory import memory_get_lang

ru = {}
en = {}
cn = {}


def GetLang(config=None):
    lang = memory_get_lang()
    if lang == 'ru':
        return ru
    if lang == 'en':
        return en
    if lang == 'cn':
        return cn
    raise ValueError('Lang incorrect')
