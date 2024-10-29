from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Race
from datetime import datetime
from django.forms.widgets import Select
from .models import Comment
from django.forms.widgets import SelectDateWidget

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)  
# Обязательное поле для ввода электронной почты
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')  

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email

class CustomAuthenticationForm(AuthenticationForm):
    # индивидуальнsq интерфейс входа в систему.
    class Meta:
        model = User
        fields = ['username', 'password']

class CommentForm(forms.ModelForm):
    # Класс формы для создания и редактирования комментариев.
    class Meta:
        model = Comment
        fields = ['content'] 

class RaceForm(forms.ModelForm):
    # Класс формы для создания и редактирования гонок.
    class Meta:
        model = Race
        fields = ['name', 'date', 'organizer', 'path']

    def __init__(self, *args, **kwargs):
        # формы с кастомизациями
        super(RaceForm, self).__init__(*args, **kwargs)
        self.fields['date'] = forms.DateField(
            widget=SelectDateWidget(
                empty_label=("Выберите день", "Выберите месяц", "Выберите год" ),
                years=range(datetime.now().year, datetime.now().year + 10)
            ),
            label='Дата гонки',
            input_formats=['%d-%m-%Y', '%d/%m/%Y'] 
        )