from django import forms
from members.models import Agent, Profile, Vpp, Paid, vpp_balance, vppsub, Agent_verified, orphanage, Transaction
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Username",                
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",                
                "class": "form-control"
            }
        ))

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Username",                
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder" : "Email",                
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",                
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password check",                
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')



class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']


def form_validation_error(form):
    msg = ""
    for field in form:
        for error in field.errors:
            msg += "%s: %s \\n" % (field.label if hasattr(field, 'label') else 'Error', error)
    return msg


class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ('phone','country','state','city','category','qualification')
        exclude = ['username']
        



def form_validation_error(form):
    msg = ""
    for field in form:
        for error in field.errors:
            msg += "%s: %s \\n" % (field.label if hasattr(field, 'label') else 'Error', error)
    return msg


class VppForm(forms.ModelForm):
    class Meta:
        model = Vpp
        fields = '__all__'
        exclude = ['user', 'v_status', 'point']


def form_validation_error(form):
    msg = ""
    for field in form:
        for error in field.errors:
            msg += "%s: %s \\n" % (field.label if hasattr(field, 'label') else 'Error', error)
    return msg



class PaidForm(forms.ModelForm):
    class Meta:
        model = Paid
        field = '__All__'
        exclude = ['vpp', 'date']

class vpp_balanceForm(forms.ModelForm):
    
    class Meta:
        model = vpp_balance
        field = '__All__'
        exclude = ['vpp','date']


class vppsubForm(forms.ModelForm):
    class Meta:
        model = vppsub
        field = '__All__'
        exclude = ['partner', 'date']
        

class iduploadForm(forms.ModelForm):
    class Meta:
        model = Agent_verified
        field = '__All__'
        exclude = ['user']
        
        
class orphanageForm(forms.ModelForm):
    class Meta:
        model = orphanage
        field = '__All__'
        exclude = ['date', 'agent'] 

class circleForm(forms.ModelForm):
    class Meta:
        model = Circle
        field = '__All__'
        exclude = ['date', 'rootuser']


class transactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        field = '__All__'
        exclude = ['date', 'viapps', 'username']                
            
        
        
        
        
    
