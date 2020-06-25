from dataclasses import dataclass
from datetime import date
@dataclass(frozen=True)
class UEAAppPaymentDetailDTO(object):
    paymentID: int
    weeklyAssitanceAmount: float
    weeklyBenefitPenaltyAmount: float
    weeklyPaymentAmount: float
    beginingPaymentPeriod: date
    endingPaymentPeriod: date