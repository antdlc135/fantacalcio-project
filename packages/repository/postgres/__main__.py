#--kind python:default
#--web true

from BaseRepository import BaseRepository
import sys
import os
import importlib

def main(args):

    db = BaseRepository()
    method = args.get("method")
    module_name = args.get("module")

    if module_name is None:
      return {"body": {"data": "Missing module", "error": True}}

    if method is None:
      return {"body": {"data": "Missing method", "error": True}}

    curpath = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, curpath)

    api_lib = importlib.import_module(module_name)
    class_ = getattr(api_lib, module_name)

    repo = class_(db,args)
    method = getattr(repo, method)
    response = method(args)

    return response