from django.db import models

class Application(models.Model):
    startDate = models.DateField()
    endDate = models.DateField()
    reason = models.TextField()
    address = models.TextField()
    applicant = models.ForeignKey('accounts.User',on_delete=models.CASCADE,null=True)
    choices = (
        ('EL', 'Earned Leave'),
        ('HPL', 'Half Pay Leave'),
        ('OT', 'Other Leave'),
        )
    typeOfLeave = models.CharField(choices=choices,max_length=3, default='OT')
    prefix = models.IntegerField(default=0)
    suffix = models.IntegerField(default=0)
    availLTC = models.BooleanField(default=False)

    submitted = models.BooleanField(default=False)
    recommended = models.BooleanField(default=False)
    recommended_by = models.ForeignKey('accounts.User',on_delete=models.CASCADE, blank=True, null=True, related_name="Recommended_by")
    recommender_comments = models.TextField(blank=True, null=True)

    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey('accounts.User',on_delete=models.CASCADE, blank=True, null=True, related_name="Approved_by")
    approver_comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.applicant.get_full_name()) + " from " + str(self.startDate) + " - " + str(self.endDate)

    @property
    def is_submitted(self):
        return self.submitted

    @property
    def full_name(self):
        return self.applicant.get_full_name()

    @property
    def is_recommended(self):
        return self.recommended

    @property
    def is_approved(self):
        return self.approved
