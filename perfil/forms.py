from django import forms
from django.contrib.auth.models import User
from . import models


class PerfilForm(forms.ModelForm):
    class Meta:
        model = models.Perfil
        fields = '__all__'
        exclude = ('usuario', )

class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Senha',
    )

    password_confirm = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Confirme a senha',
    )

    def __init__(self, usuario=None,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.usuario = usuario

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'password_confirm', 'email')

    def clean(self, *args, **kwargs):
        data = self.data
        cleaned = self.cleaned_data
        validation_error_msgs = {}

        usuario_data = cleaned.get('username')
        email_data = cleaned.get('email')
        password_data = cleaned.get('password')
        password_data_confirm = cleaned.get('password_confirm')

        usuario_db = User.objects.filter(username=usuario_data).first()
        email_db = User.objects.filter(email=email_data).first()

        error_msg_user_exists = 'Usuário já cadastrado'
        error_msg_email_exists = 'Email já cadastrado'
        error_password_match = 'As senhas digitadas devem ser iguais'
        error_password_short = 'A senha deve possuir pelo menos 6 caracteres'
        error_password_required = 'A senha é obrigatória'

        if self.usuario:
            if usuario_db:
                if usuario_data != usuario_db.username:
                    validation_error_msgs['username'] = error_msg_user_exists
            
            if email_db:
                if email_data != email_db.email:
                    validation_error_msgs['email'] = error_msg_email_exists

            if password_data:            
                if password_data != password_data_confirm:
                    validation_error_msgs['password'] = error_password_match
                    validation_error_msgs['password_confirm'] = error_password_match
            
                if len(password_data) < 6:
                    validation_error_msgs['password'] = error_password_short
        else:
            print(usuario_data)
            if usuario_db:
                validation_error_msgs['username'] = error_msg_user_exists
            
            if email_db:
                validation_error_msgs['email'] = error_msg_email_exists

            if not password_data:
                validation_error_msgs['password'] = error_password_required

            if not password_data_confirm:
                validation_error_msgs['password'] = error_password_required

            if password_data != password_data_confirm:
                validation_error_msgs['password'] = error_password_match
                validation_error_msgs['password'] = error_password_match

            if len(password_data) < 6:
                validation_error_msgs = error_password_short
        
        if validation_error_msgs:
            raise(forms.ValidationError(validation_error_msgs))