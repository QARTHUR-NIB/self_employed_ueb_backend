from dataclasses import dataclass 
from datetime import date
@dataclass(frozen=True)
class UEADTO(object):
    applicationID: int
    firstName: str
    lastName: str
    dob: date
    eeni: str
    erni: str
    email: str
    primaryContact: str
    secondaryContact: str
    placeOfOperation: str
    islandOfOperation: str
    estimatedWeeklyEarnings: float
    status: str
    approvalDate: date
    insertedBy: str
    insertedDate: date
    updatedBy: str
    updatedDate: date
    approvedBy: str
    deniedBy: str
    userComment: str
    denialDate: date
    natureOfEmployment: str
    routedTo: str
    routedDate: date
    sunCashOptIn: str
    tourismIndustryFlag: str