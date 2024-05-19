#--kind python:default
#--web true

import importlib
import os.path
import sys


def getModel(args):
  modelName = args.get("model")
  payload = args.get("payload")
  toInsert = args.get("toInsert", False)

  if modelName is None:
    return {"body": {"data": "Missing model", "error": True}}

  try:
    syspath = sys.path
    curpath = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, curpath)
    model = importlib.import_module(modelName)

    modelArgs = {
      "payload": payload,
      "toInsert": toInsert
    }

    resp = model.getModel(modelArgs)

    if resp is None:
      return {"body": {"data": "Model not supported", "error": True }}

    return resp

  except Exception as e:
    return {"body": {"data": "Error: " + f"{repr(e)}" + " sys path is: " + f"{repr(syspath)}" + " - curpath is: " + f"{repr(curpath)}", "error": True}}