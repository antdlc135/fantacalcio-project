import json

class Article(dict):
  def __init__(self,args,toInsert):

    model = {
      "id": None,
      "uid": "uuid_nil()",
      "body": "defVal",
      "author": "defVal"
    }

    managed_model = {}
    for attr in model.keys():
      attr_cond = attr.lower() if toInsert else attr
      managed_model[f"{attr_cond}"] = args.get(attr, args.get(attr.lower()))

    if toInsert:
      del managed_model["id"]
      del managed_model["uid"]

    dict.__init__(self,args=managed_model)

def getModel(args):

  payload = args.get("payload")
  toInsert = args.get("toInsert")

  recordsToReturn = []
  records = payload
  if isinstance(payload, str):
    records = json.loads(records)

  for record in records:
    recordsToReturn.append(Article(record,toInsert).get("args"))
  return recordsToReturn