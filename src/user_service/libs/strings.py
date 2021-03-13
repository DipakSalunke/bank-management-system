"""
libs.strings

By default, uses `en-gb.json` file inside the `strings` top-level folder.    

If language changes, set `libs.strings.default_locale` and run `libs.strings.refresh()`

"""
    
import json

default_locale = "ja-jp"
cached_strings  = {}

def refresh():
    global cached_strings
    with open(f"src/user_service/strings/{default_locale}.json",encoding="utf8") as f:
        cached_strings = json.load(f)


#caching
def gettext(name):
    return cached_strings[name]
refresh()