#--kind python:default
#--web true

from BaseRepository import BaseRepository
import sys
import os
import importlib

def main(args):
    db = BaseRepository(args)
    method = args.get("method", "GET")
    module_name = args.get("module", "GET")

    curpath = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, curpath)

    api_lib = importlib.import_module(module_name)
    class_ = getattr(api_lib, module_name)

    repo = class_(db)
    method = getattr(repo, method)
    response = method(args)

    return response