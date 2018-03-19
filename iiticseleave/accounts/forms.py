from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
import accounts.models

def log(f):
    def logged(*args, **kwargs):
        print(f, "called")
        ans = f(*args, **kwargs)
        print(f, "successfully returned")
        return ans
    return logged


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = accounts.models.User
        fields = ('firstName',
                  'lastName',
                  'email',
                  'user_type',
                  'active',
                  'applicant')
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = accounts.models.User
        fields = ('firstName',
                  'lastName',
                  'email',
                  'password',
                  'active',
                  'user_type',
                  'applicant')

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):

    def get_queryset(self, request):
        """Returns only  rows"""
        result = super(UserAdmin, self).get_queryset(request)
        if not (request.user.is_admin or request.user.is_supervisor):
            result = result.filter(id=request.user.id)
        return result


    def get_readonly_fields(self, request, obj=None):
        if obj and not request.user.is_admin: # editing an existing object
            return list(self.readonly_fields) + ['recommender', 'applicant', 'user_type']
        return self.readonly_fields


    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('firstName',
                    'lastName',
                    'email',
                    'user_type',
                    'active',
                    'applicant')


    fieldsets = (
        (None, {'fields': ('email', 'recommender',)}),
        ('Personal info', {'fields': ('firstName',
                                      'lastName',
                                      'department',
                                      'designation')
                          }
        ),
        ('Permissions', {'fields': ('user_type','applicant')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('firstName', 'lastName', 'email', 'password1', 'password2', 'user_type', 'active', 'applicant','recommender')}
        ),
    )

    list_filter = ('user_type',
                   'applicant',
                   'active')

    search_fields = ('firstName',
                     'lastName',
                     'email',
                     'user_type')

    readonly_fields = ['department']
    ordering = ('firstName','lastName')
    filter_horizontal = ()
