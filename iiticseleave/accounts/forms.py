from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
import accounts.models


class UserCreationForm(forms.ModelForm):

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)    
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)    

    class Meta:
        model = accounts.models.User
        fields = ('firstName', 'lastName', 'email', 'active', 'supervisor', 'recommender', 'admin', 'approver')

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
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = accounts.models.User
        fields = ('firstName', 'lastName', 'email', 'password', 'active', 'supervisor', 'recommender', 'admin', 'approver')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form =    UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('firstName', 'lastName', 'email', 'active', 'supervisor', 'recommender', 'admin', 'approver')

    list_filter = ('admin','supervisor','approver','recommender')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('firstName','lastName')}),
        ('Permissions', {'fields': ('admin','supervisor','approver','recommender')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('firstName', 'lastName', 'email', 'password1', 'password2', 'active', 'supervisor', 'recommender', 'admin', 'approver')}
        ),
    )
    search_fields = ('firstName', 'lastName', 'email', 'active', 'supervisor', 'recommender', 'admin', 'approver')
    ordering = ('email',)
    filter_horizontal = ()
