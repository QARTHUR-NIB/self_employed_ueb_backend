from dataclasses import dataclass
from datetime import date
@dataclass(frozen=True)
class UEAAppPaymentDTO(object):
    applicationID: int
    paymentType: str
    paymentStatus: str
    paymentAmount: float
    beginingPaymentPeriod: date
    endingPaymentPeriod: date
    lastPaymentDate: date
    nextPaymentDate: date