from modules.application.repositories.oracle_db import OracleDB
from modules.application.repositories.UEADTO import UEADTO

class UEAApplication(OracleDB):
    def __init__(self):
        super().__init__()
        self.applicationID = None
        self.weeklyAssistanceAmount = 200
        self.weeklyBenefitPenaltyAmount = 0
        self.maxNumberOfWeeks = 0
        self.numWeeksPaid = 0
        self.numWeeksRemaining = 0
        self.remainingBalance = 0
        self.paymentType = None
        self.lastPaymentDate = None
    
    def getNumberOfWeeksPaid(self):
        params = {"app_id":self.applicationID}
        super().executeQuery("getNumberOfWeeksPaid.sql",params)
        if self.resultSet is not None:
            for row in self.resultSet:
                self.numWeeksPaid = row["numWeeksPaid"] if row["numWeeksPaid"] is not None else 0

    def getLatestBenefitPenalty(self):
        params = {"app_id":self.applicationID}
        super().executeQuery("getLatestBenefitPenalty.sql",params)
        if self.resultSet is not None:
            for row in self.resultSet:
                self.weeklyBenefitPenaltyAmount = row["benefitPenalty"] if row["benefitPenalty"] is not None else 0
    
    def getNumberofWeeksRemaining(self):
        self.getNumberOfWeeksPaid()
        self.numWeeksRemaining = self.maxNumberOfWeeks - self.numWeeksPaid

    def calculateRemainingBalance(self):
        self.getLatestBenefitPenalty()
        self.remainingBalance = self.numWeeksRemaining * (self.weeklyAssistanceAmount - self.weeklyBenefitPenaltyAmount)

    def getApplicationPaymentType(self):
        params = {"app_id":self.applicationID}
        super().executeQuery("getApplicationPaymentType.sql",params)
        if self.resultSet is not None:
            for row in self.resultSet:
                self.paymentType = row["appPaymentType"]

    def getLastPaymentDate(self):
        params = {"app_id":self.applicationID}
        super().executeQuery("getLastPaymentDate.sql",params)
        if self.resultSet is not None:
            for row in self.resultSet:
                self.lastPaymentDate = row["lastPaymentDate"]
    
    def markApplicationCompleted(self):
        params = {"app_id":self.applicationID,"status":"Completed"}
        super().updateRecord("updateUEAApplicationStatus.sql",params)

    def getTourismApplicationsPaidLessThan12Weeks(self):
        listTourismApplications = []
        super().executeQuery("getTourismAppPaidLessThan12weeks.sql")
        if self.resultSet is not None:
            for row in self.resultSet:
                listTourismApplications.append(UEADTO(row["applicationID"],row["firstName"],
                                               row["lastName"],row["dob"],row["eeni"],row["erni"],
                                               row["email"],row["primaryContact"],row["secondaryContact"],
                                               row["placeOfOperation"],row["islandOfOperation"],
                                               row["estimatedWeeklyEarnings"],row["status"],row["approvalDate"],
                                               row["insertedBy"],row["insertedDate"],row["updatedBy"],row["updatedDate"],
                                               row["approvedBy"],row["deniedBy"],row["userComment"],row["denialDate"],
                                               row["natureOfEmployment"],row["routedTo"],row["routedDate"],row["sunCashOptIn"],
                                               row["tourismIndustryFlag"]
                ))
        return listTourismApplications

    def getNonTourismApplicationsPaidLessThan11Weeks(self):
        listNonTourismApplications = []
        super().executeQuery("getNonTourismAppPaidLessThan11weeks.sql")
        if self.resultSet is not None:
            for row in self.resultSet:
                listNonTourismApplications.append(UEADTO(row["applicationID"],row["firstName"],
                                               row["lastName"],row["dob"],row["eeni"],row["erni"],
                                               row["email"],row["primaryContact"],row["secondaryContact"],
                                               row["placeOfOperation"],row["islandOfOperation"],
                                               row["estimatedWeeklyEarnings"],row["status"],row["approvalDate"],
                                               row["insertedBy"],row["insertedDate"],row["updatedBy"],row["updatedDate"],
                                               row["approvedBy"],row["deniedBy"],row["userComment"],row["denialDate"],
                                               row["natureOfEmployment"],row["routedTo"],row["routedDate"],row["sunCashOptIn"],
                                               row["tourismIndustryFlag"]
                ))
        return listNonTourismApplications