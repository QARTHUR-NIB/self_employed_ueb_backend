from modules.application.repositories.UEAApplication import UEAApplication
from modules.application.repositories.TourismUEAApplication import TourismUEAApplication
from modules.application.repositories.NonTourismUEAApplication import NonTourismUEAApplication
from modules.application.repositories.UEAAppPayment import UEAAppPayment
from modules.application.repositories.UEAAppPaymentDTO import UEAAppPaymentDTO
from modules.application.repositories.UEAAppPaymentDetail import UEAAppPaymentDetail
from modules.application.repositories.UEAAppPaymentDetailDTO import UEAAppPaymentDetailDTO
from datetime import date

class LumpSumCheckRun:
    def __init__(self):
        pass

    def generateLumpSumPayments(self):
        paymentStatus = "Pending"
        beginingPaymentPeriod = date(2020,4,7)
        endingPaymentPeriod = date(2020,7,1)
        listTourismApplications = []
        listNonTourismApplications = []
        ueaApp = UEAApplication()
        listTourismApplications = ueaApp.getTourismApplicationsPaidLessThan12Weeks()
        for tourismApplication in listTourismApplications:
            tourismApp = TourismUEAApplication(tourismApplication)
            tourismApp.getNumberofWeeksRemaining()
            tourismApp.calculateRemainingBalance()
            tourismApp.getApplicationPaymentType()
            tourismApp.getLastPaymentDate()
            payment = UEAAppPayment(UEAAppPaymentDTO(tourismApp.applicationID,tourismApp.paymentType,paymentStatus,
                                                     tourismApp.remainingBalance,beginingPaymentPeriod,endingPaymentPeriod,
                                                     tourismApp.lastPaymentDate,endingPaymentPeriod))
            payment.getNextPaymentID()
            listPaymentDetailDTO = []
            for i in range(tourismApp.numWeeksRemaining):
                paymentDetailDTO = UEAAppPaymentDetailDTO(payment.paymentID,tourismApp.weeklyAssistanceAmount,tourismApp.weeklyBenefitPenaltyAmount,
                                                    (tourismApp.weeklyAssistanceAmount - tourismApp.weeklyBenefitPenaltyAmount),payment.beginingPaymentPeriod,
                                                    payment.endingPaymentPeriod)
                listPaymentDetailDTO.append(paymentDetailDTO)
            paymentDetail = UEAAppPaymentDetail()
            payment.save()
            paymentDetail.saveAll(listPaymentDetailDTO)
            tourismApp.markApplicationCompleted()

        listNonTourismApplications = ueaApp.getNonTourismApplicationsPaidLessThan11Weeks()
        for nonTourismApplication in listNonTourismApplications:
            nonTourismApp = NonTourismUEAApplication(nonTourismApplication)
            nonTourismApp.getNumberofWeeksRemaining()
            nonTourismApp.calculateRemainingBalance()
            nonTourismApp.getApplicationPaymentType()
            nonTourismApp.getLastPaymentDate()
            payment = UEAAppPayment(UEAAppPaymentDTO(nonTourismApp.applicationID,nonTourismApp.paymentType,paymentStatus,
                                                     nonTourismApp.remainingBalance,beginingPaymentPeriod,endingPaymentPeriod,
                                                     nonTourismApp.lastPaymentDate,endingPaymentPeriod))
            payment.getNextPaymentID()
            listPaymentDetailDTO = []
            for i in range(nonTourismApp.numWeeksRemaining):
                paymentDetailDTO = UEAAppPaymentDetailDTO(payment.paymentID,nonTourismApp.weeklyAssistanceAmount,nonTourismApp.weeklyBenefitPenaltyAmount,
                                                    (nonTourismApp.weeklyAssistanceAmount - nonTourismApp.weeklyBenefitPenaltyAmount),payment.beginingPaymentPeriod,
                                                    payment.endingPaymentPeriod)
                listPaymentDetailDTO.append(paymentDetailDTO)
            paymentDetail = UEAAppPaymentDetail()
            payment.save()
            paymentDetail.saveAll(listPaymentDetailDTO)
            nonTourismApp.markApplicationCompleted()
