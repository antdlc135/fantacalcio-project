#--kind python:default
#--param POSTGRES_URL $POSTGRES_URL

import psycopg
import traceback
import sys
import os
curpath = os.path.dirname(os.path.abspath(__file__))

class BaseRepository:

  response = {}

  def __init__(self,args):
    self.conn = None
    self.URL = os.getenv("POSTGRES_URL")
    self.module_name = args.get("module")
    self.method = args.get("method")

  def connect(self):
    if not self.conn:
      self.conn = psycopg.connect(self.URL)

  def close(self):
    if self.conn:
      self.conn.close()
      self.conn = None

  def execute_query(self, query):
    try:

      cur = self.conn.cursor()
      cur.execute(query)

      if query.strip().lower().startswith("select"):
        rows = cur.fetchall()
        result = [dict(zip([desc[0] for desc in cur.description], row)) for row in rows]

      else:
        self.conn.commit()
        result = {"status": "success"}

      cur.close()
      return result

    except Exception as e:
      traceback.print_exc()
      return {
        "body": {
          "data": "Error: "
          + f"{repr(e)}" + " sys path is: " + f"{repr(sys.path)}" + " - curpath is: " + f"{repr(curpath)}",

          "error": True
        }
      }

  def __del__(self):
    self.close()