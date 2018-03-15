from django import forms
from django.contrib import admin
import leave.models

class ApplicationCreationForm(forms.ModelForm):

    # class Meta:
    #     model = leave.models.Application
    #     fields = ('typeOfLeave', 'startDate', 'endDate', 'prefix', 'suffix', 'availLTC',  'reason', 'address', 'submitted')
    

class ApplicationAdmin(admin.ModelAdmin):
    

    form = ApplicationCreationForm
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
            print(db_field.name)
            if db_field.name == 'applicant':
                kwargs['initial'] = request.user.id
                return db_field.formfield(**kwargs)
            return super(ApplicationAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    list_display = ('applicant', 'startDate', 'endDate', 'submitted', 'recommended', 'approved')
    # readonly_fields = ('applicant',)
    list_filter = ('approved', 'recommended')
    search_fields = ('startDate', 'endDate', 'reason', 'address', 'submitted', 'recommended', 'approved')
    ordering = ('startDate',)
    filter_horizontal = ()
