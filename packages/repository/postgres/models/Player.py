import json

class Player(dict):
  def __init__(self,args,toInsert):

    model = {
      "id": None,
      "uid": "uuid_nil()",
      "firstName": "defVal",
      "lastName": "defVal",
      "position": "defVal",
      "roleId": "defVal",
      "teamId": "defVal",
      "serieaPlayer": "defVal",
    }

    managed_model = {}
    for attr in model.keys():
      attr_cond = attr.lower() if toInsert else attr
      managed_model[f"{attr_cond}"] = args.get(attr, args.get(attr.lower()))
    # costretto ad usare il minuscolo (non camelCase) per get nome colonne db postgres

    # => non posso usare la notazione di seguito
    # model["id"] = args.get("id", None)
    # model["firstName"] = args.get("firstname", "defVal")
    # model["..."] = args.get("...", "...")

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
    records = json.loads(records) # tbc

  for record in records:
    recordsToReturn.append(Player(record,toInsert).get("args"))
  return recordsToReturn