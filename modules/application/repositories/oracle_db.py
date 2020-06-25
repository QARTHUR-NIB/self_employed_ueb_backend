import os
import cx_Oracle
from config import oraDB
from modules.application import app

class OracleDB:
    def __init__(self):
        self.resultSet = []
        self.connection = cx_Oracle.connect(f"{oraDB.user_name}/{oraDB.password}@{oraDB.db}")
        self.cursor = self.connection.cursor()
    
    def getColumnNames(self):
        columnNames = [row[0] for row in self.cursor.description]
        return columnNames
    
    def createRowObject(self,columnNames,row):
        rowObj = {}
        for i in range(len(row)):
            rowObj[columnNames[i]] = row[i]
        return rowObj

    def executeQuery(self,sqlFileName,params=None):
        self.resultSet = []
        sqlPath = os.path.join(app.config['SCRIPT_FOLDER'],sqlFileName)
        with open(sqlPath,"r") as sqlFile:
            if params is None:
                results = self.cursor.execute(sqlFile.read())
            else:
                results = self.cursor.execute(sqlFile.read(),params)
            columnNames = self.getColumnNames()
            while True:
                rows = results.fetchall()
                if not rows:
                    break
                for row in rows:
                    self.resultSet.append(self.createRowObject(columnNames,row))

    def insertOneRecord(self,sqlFileName,params):
        sqlPath = os.path.join(app.config['SCRIPT_FOLDER'],sqlFileName)
        with open(sqlPath,"r") as sqlFile:
            self.cursor.execute(sqlFile.read(),params)
            self.connection.commit()

    def insertMultipleRecords(self,sqlFileName,params):
        sqlPath = os.path.join(app.config['SCRIPT_FOLDER'],sqlFileName)
        with open(sqlPath,"r") as sqlFile:
            self.cursor.executemany(sqlFile.read(),params)
            self.connection.commit()

    def updateRecord(self,sqlFileName,params):
        sqlPath = os.path.join(app.config['SCRIPT_FOLDER'],sqlFileName)
        with open(sqlPath,"r") as sqlFile:
            self.cursor.execute(sqlFile.read(),params)
            self.connection.commit()

    def disposeDBConnections(self):
        self.connection.close()
        self.cursor.close()