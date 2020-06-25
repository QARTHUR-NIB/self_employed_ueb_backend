from modules.application.repositories.UEAAppPaymentDTO import UEAAppPaymentDTO
from modules.application.repositories.oracle_db import OracleDB
import cx_Oracle

class UEAAppPayment(OracleDB):
    def __init__(self,UEAAppPaymentDTO):
        super().__init__()
        self.paymentID = None
        self.applicationID = UEAAppPaymentDTO.applicationID
        self.paymentType = UEAAppPaymentDTO.paymentType
        self.paymentStatus = UEAAppPaymentDTO.paymentStatus
        self.paymentAmount = UEAAppPaymentDTO.paymentAmount
        self.beginingPaymentPeriod = UEAAppPaymentDTO.beginingPaymentPeriod
        self.endingPaymentPeriod = UEAAppPaymentDTO.endingPaymentPeriod
        self.lastPaymentDate = UEAAppPaymentDTO.lastPaymentDate
        self.nextPaymentDate = UEAAppPaymentDTO.nextPaymentDate
    
    def getNextPaymentID(self):
        nextPaymentID = self.cursor.var(cx_Oracle.NUMBER,20) if not None else ''
        success = self.cursor.var(cx_Oracle.STRING,1) if not None else ''
        message = self.cursor.var(cx_Oracle.STRING,250) if not None else ''
        self.cursor.callproc("client.getNextPaymentID",[nextPaymentID,success,message])
        if success.getvalue() == "N":
            raise Exception(f"Error Retrieving Next Payment ID: {message.getvalue()}")
        self.paymentID = nextPaymentID.getvalue()

    def save(self):
        self.insertOneRecord("createPaymentMaster.sql",(self.paymentID,self.applicationID,self.paymentType,self.paymentStatus,self.paymentAmount,
                                                        self.beginingPaymentPeriod,self.endingPaymentPeriod,self.lastPaymentDate,self.nextPaymentDate))