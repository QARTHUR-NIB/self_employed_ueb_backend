from modules.application.repositories.UEAApplication import UEAApplication
from modules.application.repositories.UEADTO import UEADTO

class NonTourismUEAApplication(UEAApplication):
    def __init__(self,UEADTO):
        super().__init__()
        self.applicationID = UEADTO.applicationID
        self.maxNumberOfWeeks = 11