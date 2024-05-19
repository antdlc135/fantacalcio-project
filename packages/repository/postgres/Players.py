from models import getModel
class Players:

  MODEL = "Player"
  DB_TABLE = 'Players'
  # when replicating the class for new models,
  # you should always modify these variables and not the query strings

  response = {}

  def __init__(self,conn,cur):
    self.conn = conn
    self.cur = cur

  def getAll(self, args):

    query = f"SELECT * FROM {Players.DB_TABLE}"
    # if you want to change the actual query sent to the db,
    # this is where you should do it

    playerRecords = self.toList(
      self.cur.execute(
      f"""SELECT (row_to_json(t)::jsonb) FROM ({query}) t""").fetchall()
    )
    # you will generally almost never have to change this expression

    # e.g.
    # records = [
    # ({'id': '63c1c6a9-2ddd-4d8d-8264-e4f52b1a7b02', 'roleid': None, 'teamid': None, 'lastname': 'pluto', 'position': None, 'firstname': 'pippo', 'serieaplayer': True},),
    # ({'id': '5327c9a9-8411-4b85-a9a1-9d16339a77b6', 'roleid': None, 'teamid': None, 'lastname': 'pluto', 'position': None, 'firstname': 'pippo', 'serieaplayer': True},)
    # ]

    response = getModel({"model": Players.MODEL, "payload": playerRecords})
    # generally, before exposing the data outside this class, they will always have to be first parsed by a model

    self.response["body"] = response
    return self.response

  def getRecordsByIds(self, args):

    if args.get("idList") is None:
      return {"body": {"data": "Missing idslist param", "error": True}}

    idList = list(args.get("idList").split(","))
    query = f"SELECT * FROM {Players.DB_TABLE} WHERE id = ANY(%s)"

    playerRecords = self.toList(
      self.cur.execute(
      f"""SELECT (row_to_json(t)::jsonb) FROM ({query}) t""", [idList]).fetchall()
    )
    response = getModel({"model": Players.MODEL, "payload": playerRecords})

    self.response["body"] = response
    return self.response

  def insertRecords(self, args):

    jsonSerializedObjString = args.get("recordsToInsert")

    if jsonSerializedObjString is None:
      return {"body": {"data": "Provide JSON recordsToInsert param", "error": True}}


    recordsToInsert = getModel({"model": Players.MODEL, "payload": jsonSerializedObjString, "toInsert": True})

    columns = str(tuple([column for column in recordsToInsert[0].keys()])).replace("'","")

    insert = f"INSERT INTO {Players.DB_TABLE}{columns} VALUES "

    for recordValues in recordsToInsert:
      values =  recordValues.values()
      valueList = tuple([value if value != None else "" for value in values])

      pgCmd = insert + str(valueList)
      print("pg insert cmd: " + pgCmd)

      self.cur.execute(pgCmd)

    self.response["body"] = "Records correctly inserted"
    return self.response

  def updateRecords(self, args):
    # todo
    self.response["body"] = "Records correctly updated"
    return self.response

  def deleteRecords(self, args):
    # todo
    self.response["body"] = "Records correctly deleted"
    return self.response

  def toList(self, fetchedList):
    playerRecords = []
    for record in fetchedList:
      playerRecords.append(record[0])
    return playerRecords








  # test methods
  def createTableTest(self, args):

    # jsonSerializedObjString = args.get("recordsToInsert")
    jsonSerializedObjString = "[{\"firstName\": \"test_firstName\", \"lastName\": \"test_lastName\", \"serieaPlayer\": \"true\", \"position\": \"test_position\", \"roleId\": 1, \"teamId\": 2}]"

    recordsToInsert = getModel({"model": "Player", "payload": jsonSerializedObjString, "toInsert": True})
    print("getModel Player to Insert Model: " + str(recordsToInsert))

    self.cur.execute(f"""
      CREATE EXTENSION IF NOT EXISTS "pgcrypto";
      CREATE TABLE IF NOT EXISTS {Players.DB_TABLE} (
        id INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
        uid UUID DEFAULT gen_random_uuid(),
        firstName VARCHAR,
        lastName VARCHAR,
        position VARCHAR,
        roleId INT,
        teamId INT,
        serieaPlayer BOOLEAN NOT NULL DEFAULT TRUE
      );
      """
    )

    columns = str(tuple([column for column in recordsToInsert[0].keys()])).replace("'","")

    insert = f"INSERT INTO {Players.DB_TABLE}{columns} VALUES "

    for recordValues in recordsToInsert:
      values =  recordValues.values()
      valueList = tuple([value if value != None else "" for value in values])

      pgCmd = insert + str(valueList)
      print("pg insert cmd: " + pgCmd)

      self.cur.execute(pgCmd)

    response = self.getAll(None)

    return response

  def deleteTableTest(self,args):
    self.cur.execute(f"DROP TABLE {Players.DB_TABLE}")
    self.conn.commit()
    self.response["body"] = f"{Players.DB_TABLE} Table Deleted."
    return self.response