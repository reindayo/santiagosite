from django import forms
from .models import Gender, User

tw = (
    'bg-gray-50 border border-gray-300 text-gray-900 text-sm '
    'rounded-lg focus:ring-blue-500 focus:border-blue-500 '
    'block w-full p-2.5'
)


class GenderForm(forms.ModelForm):
    class Meta:
        model  = Gender
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': tw,
            'placeholder': 'e.g. Male, Female'
        })


class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': tw, 'placeholder': 'Password'
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': tw, 'placeholder': 'Confirm password'
        })
    )

    class Meta:
        model  = User
        fields = ['first_name', 'last_name', 'email', 'gender', 'profile_pic']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'first_name': 'First name',
            'last_name' : 'Last name',
            'email'     : 'Email address',
        }
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': tw})
            if field in placeholders:
                self.fields[field].widget.attrs['placeholder'] = placeholders[field]
        self.fields['gender'].empty_label = 'Select gender'
        self.fields['gender'].queryset = Gender.objects.all()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email

    def clean(self):
        cleaned = super().clean()
        pw  = cleaned.get('password')
        cpw = cleaned.get('confirm_password')
        if pw and cpw and pw != cpw:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned


class UserEditForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': tw,
            'placeholder': 'Leave blank to keep current'
        }),
        required=False
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': tw,
            'placeholder': 'Confirm new password'
        }),
        required=False
    )

    class Meta:
        model  = User
        fields = ['first_name', 'last_name', 'email', 'gender', 'profile_pic']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': tw})
        self.fields['gender'].empty_label = 'Select gender'
        self.fields['gender'].queryset = Gender.objects.all()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('This email is already registered.')
        return email

    def clean(self):
        cleaned = super().clean()
        pw  = cleaned.get('password')
        cpw = cleaned.get('confirm_password')
        if pw or cpw:
            if pw != cpw:
                raise forms.ValidationError('Passwords do not match.')
        return cleaned