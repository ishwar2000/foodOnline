from django import forms 
from .models import user, userProfile
from .validators import allow_extension_validatotr

class registerUserForm(forms.ModelForm):
    password = forms.CharField(max_length=30,widget=forms.PasswordInput())
    confirmPassword = forms.CharField(max_length=30,widget=forms.PasswordInput())
    class Meta:
        model = user
        fields = ["first_name","last_name","username","email","phone_number"]
    
    def clean(self, *args, **kwargs):
        cleaned_data = super(registerUserForm, self).clean(*args, **kwargs)

        password = cleaned_data.get("password")
        confPassword = cleaned_data.get("confirmPassword")

        if password != confPassword:
            raise forms.ValidationError("password does not match!")

class userProfileForm(forms.ModelForm):
    profile_picture = forms.FileField(validators=[allow_extension_validatotr])
    cover_profile = forms.FileField(validators=[allow_extension_validatotr])
    class Meta:
        model = userProfile
        fields = ["profile_picture","cover_profile","address_line","country","state","city","pin_code","latitude","longitude"]
    
    def __init__(self,*args, **kwargs):
        super(userProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field == "latitude" or field == "longitude":
                self.fields[field].widget.attrs["readonly"] = "readonly"