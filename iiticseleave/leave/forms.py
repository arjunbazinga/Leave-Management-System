from django import forms
from django.contrib import admin
import leave.models

class ApplicationCreationForm(forms.ModelForm):

    class Meta:
        model = leave.models.Application
        fields = ['applicant', 'typeOfLeave', 'startDate', 'endDate', 'prefix', 'suffix', 'availLTC',  'reason', 'address', 'submitted', 'recommended', 'approved', 'recommender_comments', 'approver_comments', 'approved_by', 'recommended_by']

    def clean(self):
        start_date = self.cleaned_data.get("startDate")
        end_date = self.cleaned_data.get("endDate")
        if end_date is not None and end_date < start_date:
            msg = u"End date should be greater than start date."
            self._errors["end_date"] = self.error_class([msg])
            raise forms.ValidationError(msg, code='invalid')


class ApplicationAdmin(admin.ModelAdmin):
    form = ApplicationCreationForm
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def get_readonly_fields(self, request, obj=None, **kwargs):
        if obj is None or request.user.is_admin:
            self.readonly_fields = []
            return self.readonly_fields
        if obj and obj.applicant == request.user: # editing an existing object
            return list(set(self.readonly_fields))
        elif request.user.is_recommender:
            self.readonly_fields = ['applicant', 'typeOfLeave', 'startDate', 'endDate', 'prefix', 'suffix', 'availLTC',  'reason', 'address',]
            return list(set(self.readonly_fields))
        elif request.user.is_approver:
            self.readonly_fields = ['applicant', 'typeOfLeave', 'startDate', 'endDate', 'prefix', 'suffix', 'availLTC',  'reason', 'address', 'recommender_comments', 'recommended_by',]
            return list(set(self.readonly_fields))
        return list(set(self.readonly_fields))
    
    def get_queryset(self, request):
        qs = super(ApplicationAdmin, self).get_queryset(request)
        a = qs.filter(applicant=request.user)
        if request.user.is_admin or request.user.is_supervisor:
            return qs
        if request.user.is_recommender:
            qs = qs.filter(submitted=True)
        elif request.user.is_approver:
            qs = qs.filter(recommended=True)
        elif request.user.is_standard:
            qs = qs.filter(submitted=False, recommended=True)
        if request.user.is_applicant:
            qs = (qs | a).distinct()
        return qs


    def get_form(self, request, obj=None, **kwargs):
        if obj:
            if request.user.is_recommender:
                kwargs['exclude'] = ['applicant', 'typeOfLeave', 'startDate', 'endDate', 'prefix', 'suffix', 'availLTC',  'reason', 'address','approved','submitted', 'approver_comments', 'approved_by', 'recommended_by']
            elif request.user.is_approver:
                kwargs['exclude'] = ['applicant', 'typeOfLeave', 'startDate', 'endDate', 'prefix', 'suffix', 'availLTC',  'reason', 'address', 'recommender_comments', 'recommended_by','recommended','submitted', 'approved_by',]
        elif not request.user.is_admin:
                kwargs['exclude'] = ['applicant', 'approved', 'recommender_comments', 'approver_comments', 'recommended_by', 'typeOfLeave', 'recommended', 'approved_by',]
        return super(ApplicationAdmin, self).get_form(request, obj, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'applicant':
            kwargs['initial'] = request.user.id
            return db_field.formfield(**kwargs)
        return super(ApplicationAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'applicant', None) is None:
            obj.applicant = request.user
        if request.user.is_recommender:
            obj.recommended_by = request.user
        if request.user.is_approver:
            obj.approved_by = request.user
        obj.save()
    # fieldsets = ((None, {'fields': form._meta.get_all_field_names()}),)
    #readonly_fields = ('applicant',)# 'typeOfLeave', 'startDate', 'endDate', 'prefix', 'suffix', 'availLTC',  'reason', 'address', 'submitted', 'recommended', 'approved', 'recommender_comments', 'approver_comments', 'approved_by', 'recommended_by']
    list_display = ['applicant', 'startDate', 'endDate', 'submitted', 'recommended', 'approved']
    list_filter = ['approved', 'recommended']
    search_fields = ['startDate', 'endDate', 'reason', 'address', 'submitted', 'recommended', 'approved']
    ordering = ['startDate',]
    filter_horizontal = ()
