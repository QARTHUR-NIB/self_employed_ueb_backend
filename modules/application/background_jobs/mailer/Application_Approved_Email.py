from modules.application.background_jobs.mailer.Email import Email

class Application_Approved_Email(Email):
    def __init__(self,recipient,template):
        self.recipient = recipient
        self.sender = "claimsltb@nib-bahamas.com"
        self.subject = "Government Assistance: Self Employed Unemployment Benefit"
        self.template = template
        Email.__init__(self,self.sender,self.recipient,self.subject,self.template)