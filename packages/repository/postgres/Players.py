from BaseRepository import BaseRepository
from models import getModel
class Players(BaseRepository):
  def __init__(self,args):
    super.__init__(args)

  MODEL = "Player"
  DB_TABLE = "Players"
  # when replicating the class for new models,
  # you should always modify these variables and not the query strings

  def getAll(self):

    query = f"SELECT * FROM {Players.DB_TABLE}"
    composite_query = f"""SELECT (row_to_json(t)::jsonb) FROM ({query}) t"""
    result = self.execute_query(composite_query)
    print("Query result: " + str(result))
    response = getModel({"model": Players.MODEL, "payload": result})
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