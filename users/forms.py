from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

## User Registration Form

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'autocomplete': 'Email'})
    )
    bio = forms.CharField(
        label="Biografia",
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False
    )
    avatar = forms.ImageField(
        label="Avatar de perfil",
        required=False
    )

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)
        labels = {
            'username': 'Nome de usuário',
            'password': 'Senha',
            'password2': 'Confirmação de senha',
        }
        help_texts = {
            'username': 'Obrigatório. 150 caracteres ou menos. Letras, dígitos e @/./+/-/_ apenas.',
            'password': 'Sua senha não pode ser muito parecida com suas outras informações pessoais.',
            'password2': 'Digite a mesma senha para verificação.',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Esse email já está em uso.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                bio=self.cleaned_data['bio'],
                avatar=self.cleaned_data['avatar']
            )
        return user
    

## Profile Update Form

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4})
        }