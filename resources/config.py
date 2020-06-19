import importlib
import os
import sys

TG_TOKEN = '1022139618:AAFsAJ0qYdRGl7lI43HRWDqJXIdQ3tOFRhc'
TG_API_URL = "https://telegg.ru/orig/bot"
def load_config():
    conf_name = os.environ.get("TG_CONF")
    if conf_name is None:
        conf_name = "development"
    try:
        r = importlib.import_module("settings.{}".format(conf_name))
        return r
    except (TypeError, ValueError, ImportError):
        sys.exit(1)
