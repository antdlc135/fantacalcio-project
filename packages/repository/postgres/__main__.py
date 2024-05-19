#--kind python:default
#--param POSTGRES_URL $POSTGRES_URL

import psycopg
import importlib
import traceback
import sys
import os

def main(args):
  module_name = args.get("module")
  method = args.get("method")

  if module_name is None:
    return {"body": {"data": "Missing module", "error": True}}

  if method is None:
    return {"body": {"data": "Missing method", "error": True}}

  try:

    syspath = sys.path
    curpath = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, curpath)

    api_lib = importlib.import_module(module_name)
    class_ = getattr(api_lib, module_name)

    with psycopg.connect(args.get("POSTGRES_URL")) as conn:
      with conn.cursor() as cur:

        query = class_(conn,cur)
        method = getattr(query, method)
        response = method(args)

        conn.commit()
        conn.close()

    return response

  except Exception as e:
    traceback.print_exc()
    return {"body": {

        "data": "Error: "
          + f"{repr(e)}" + " sys path is: " + f"{repr(syspath)}" + " - curpath is: " + f"{repr(curpath)}",

        "error": True
      }
    }