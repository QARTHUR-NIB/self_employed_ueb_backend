from modules.application.background_jobs.mailer.Email import Email

class Payment_Notice_Email(Email):
    def __init__(self,recipient,template):
        self.recipient = recipient
        self.sender = "claimsltb@nib-bahamas.com"
        self.subject = "Government Assistance: Payment Generated"
        self.template = template
        Email.__init__(self,self.sender,self.recipient,self.subject,self.template)
