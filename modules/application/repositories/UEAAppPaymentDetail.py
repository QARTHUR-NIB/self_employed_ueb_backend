#from modules.application.repositories.UEAAppPaymentDetailDTO import UEAAppPaymentDetailDTO
from modules.application.repositories.oracle_db import OracleDB

class UEAAppPaymentDetail(OracleDB):
    def __init__(self):
        super().__init__()
        # self.paymentID = UEAAppPaymentDetailDTO.paymentID
        # self.weeklyAssistanceAmount = UEAAppPaymentDetailDTO.weeklyPaymentAmount
        # self.weeklyBenefitPenaltyAmount = UEAAppPaymentDetailDTO.weeklyBenefitPenaltyAmount
        # self.weeklyPaymentAmount = UEAAppPaymentDetailDTO.weeklyPaymentAmount
        # self.beginingPaymentPeriod = UEAAppPaymentDetailDTO.beginingPaymentPeriod
        # self.endingPaymentPeriod = UEAAppPaymentDetailDTO.endingPaymentPeriod
    
    def saveAll(self,UEAAppPaymentDetailDTO):
        paymentDetails = []
        for paymentDetail in UEAAppPaymentDetailDTO:
            paymentDetails.append(tuple(paymentDetail.__dict__.values()))
        self.insertMultipleRecords("createPaymentDetail.sql",paymentDetails)

