from modules.application.background_jobs.mailer.Email import Email

class Employee_Registration_Email(Email):
    def __init__(self,template):
        self.recipient = "registration@nib-bahamas.com"
        self.sender = "register@nib-bahamas.com"
        self.subject = "Employee Registration Notice"
        self.template = template
        Email.__init__(self,self.sender,self.recipient,self.subject,self.template)
