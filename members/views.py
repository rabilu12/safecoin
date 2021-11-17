from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.api import MessageFailure
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.template import loader
from django import template

from members.forms import ProfileForm, form_validation_error
from members.models import Agent_verified, Profile, Agent, Paid, Vpp, Vpp_verified, vpp_balance, vppsub

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.http import HttpResponse
from .forms import AgentForm, LoginForm, orphanageForm, PaidForm, SignUpForm, transactionForm, vpp_balanceForm, vppsubForm, iduploadForm, ProfileForm


@login_required(login_url="log_in")
def index(request):
    context = {'segment': 'index'}
    html_template = loader.get_template('index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="log_in")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        context['segment'] = load_template

        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))



def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/members/profile/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "members/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created - please <a href="/login">login</a>.'
            success = True

            return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "members/register.html", {"form": form, "msg": msg, "success": success})



@method_decorator(login_required(login_url='user:log_in'), name='dispatch')
class ProfileView(View):
    profile = None

    def dispatch(self, request, *args, **kwargs):
        self.profile, __ = Profile.objects.get_or_create(user=request.user)
        return super(ProfileView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {'profile': self.profile, 'segment': 'profile'}
        return render(request, 'members/profile.html', context)

    def post(self, request):
        form = ProfileForm(request.POST, request.FILES, instance=self.profile)

        if form.is_valid():
            profile = form.save()
            profile.user.first_name = form.cleaned_data.get('first_name')
            profile.user.last_name = form.cleaned_data.get('last_name')
            profile.user.email = form.cleaned_data.get('email')
            profile.user.save()

            messages.success(request, 'Profile saved successfully')
        else:
            messages.error(request, form_validation_error(form))
        return redirect('userprofile')


@(login_required(login_url='user:log_in'))
def agent_register(request):
    form = AgentForm()
    context = {'form':form}
    if request.method == 'POST':
        form = AgentForm(request.POST)
        if form.is_valid():
            agent = form.save(commit=False)
            user = request.user.username
            if Agent.objects.filter(username=user).exists():
                messages.warning(request, 'You have already applied for Agent, kindly login to see your status')
                return redirect('/log-in')

            else:
                agent.username = user
                form.save()
            
        return redirect('/awelcome')
        
    return render (request, 'members/agent_register.html',  context)

@(login_required(login_url='user:log_in'))
def invoice(request):
    return render(request,'members/invoice.html')

@(login_required(login_url='user:log_in'))
def checkidupload(request):
    user = request.user.username
    if  Paid.objects.filter(username=user).exists():
       return redirect  ('/members/documents/upload')
    else:
        messages.warning(request, 'Your payment has not been procesed contact your PPS.')
    return redirect  ('/members/verification/invoice')

@(login_required(login_url='user:log_in'))
def idupload(request):
    form = iduploadForm()
    context = {'form':form}
    if request.method == 'POST':
        form = iduploadForm(request.POST, request.FILES)
        if form.is_valid():
            verified = form.save( commit=False)
            verified.user_id = request.user.id
            verified.save()
            return redirect ('/members/documents/uploadsuccess')
    return render(request,'members/idupload.html', context)

@method_decorator(login_required(login_url='user:log_in'), name='dispatch')
class UserProfile(View):
    userprofile = None

    def dispatch(self, request, *args, **kwargs):
        self.profile, __ = Profile.objects.get_or_create(user=request.user)
        return super(UserProfile, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {'profile': self.profile, 'segment': 'profile'}
        
        return render(request,'members/userprofile.html', context)

@(login_required(login_url='user:log_in'))
def agentprofile(request):
    ver = request.user.id
    user = request.user.username
    if Paid.objects.filter(username=user).exists() and Agent.objects.filter(username=user).exists() and Agent_verified.objects.filter(user_id=ver).exists():
        return redirect  ('/members/agent/profile')
    elif Agent.objects.filter(username=user).exists():
        messages.warning(request, 'Your agent account is not verified, make sure you verify your account before the deadline.')
        return redirect  ('/awelcome')
    else:
        messages.warning(request, 'You have not applied for an Agent.')
        return redirect  ('/members/user/profile')

@method_decorator(login_required(login_url='user:log_in'), name='dispatch')
class AProfile(View):
    userprofile = None

    def dispatch(self, request, *args, **kwargs):
        self.profile, __ = Profile.objects.get_or_create(user=request.user)
        return super(AProfile, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {'profile': self.profile, 'segment': 'profile'}
        
        return render(request,'members/agentprofile.html', context)
    
@(login_required(login_url='user:log_in'))
def topup(request):
    return render(request,'members/topup.html')

@(login_required(login_url='user:log_in'))
def topup60(request):
    return render(request,'members/topup60.html')

@(login_required(login_url='user:log_in'))
def topup130(request):
    return render(request,'members/topup130.html')

@(login_required(login_url='user:log_in'))
def topup270(request):
    return render(request,'members/topup270.html')   

@(login_required(login_url='user:log_in'))
def topup550(request):
    return render(request,'members/topup550.html') 

@(login_required(login_url='user:log_in'))
def usdttopup60(request):
    return render(request,'members/usdttopup60.html')

@(login_required(login_url='user:log_in'))
def usdttopup130(request):
    return render(request,'members/usdttopup130.html')

@(login_required(login_url='user:log_in'))
def usdttopup270(request):
    return render(request,'members/usdttopup270.html')

@(login_required(login_url='user:log_in'))
def usdttopup550(request):
    return render(request,'members/usdttopup550.html')

@(login_required(login_url='user:log_in'))
def bnbtopup60(request):
    return render(request,'members/bnbtopup60.html')

@(login_required(login_url='user:log_in'))
def bnbtopup130(request):
    return render(request,'members/bnbtopup130.html')

@(login_required(login_url='user:log_in'))
def bnbtopup270(request):
    return render(request,'members/bnbtopup270.html')

@(login_required(login_url='user:log_in'))
def bnbtopup550(request):
    return render(request,'members/bnbtopup550.html')


@(login_required(login_url='user:log_in'))
def give(request):
    user = request.user.id
    if  Vpp.objects.filter(user_id=user).exists():
       return redirect  ('/members/agent/feeverify')
    else:
        messages.warning(request, 'Only VPP get Access to this page.')
    return redirect  ('/members/user/profile/')
    
@(login_required(login_url='user:log_in'))
def feeverify(request):
    vid = request.user.id
    pbalance=vpp_balance.objects.get(vpp_id=vid)
    balance = int(pbalance.unit)
    form1 = vpp_balanceForm()
    form = PaidForm()
    context = {'form':form, 'balance':balance}
    if request.method == 'POST':
        form = PaidForm(request.POST)
        if form.is_valid():
            cagent = form.cleaned_data['username']
            paid = form.save(commit=False)
            vid=request.user.id
            pbalance=vpp_balance.objects.get(vpp_id=vid)
            bal = int(pbalance.unit) - 6
            pbalance.unit=bal
            user = request.user.username
            if Paid.objects.filter(username=cagent).exists():
                 messages.warning(request, 'The username you entered was verified previously.')
                 
            elif bal < 0:
                messages.error(request, 'Your unit balance is low.')
            else:
                paid.vpp = user
                paid.save()
                form1 = form1.save(commit=False)
                pbalance.save()
                print(bal)
                messages.success(request, 'Verification successful.')
    return render(request,'members/feeverify.html', context)

@(login_required(login_url='user:log_in'))
def paywithvictor(request):
    return render(request,'members/paywithvictor.html')

@(login_required(login_url='user:log_in'))
def ray(request):
    return render(request,'members/ray.html')

@(login_required(login_url='user:log_in'))  
def qrb(request):
    return render(request,'members/qareeb.html')

@(login_required(login_url='user:log_in'))
def msn(request):
    return render(request,'members/msn.html')

@(login_required(login_url='user:log_in'))
def msa(request):
    return render(request,'members/msa.html')

@(login_required(login_url='user:log_in'))
def busy(request):
    return render(request,'members/busy.html')            

@(login_required(login_url='user:log_in'))
def vppsubs(request):
    form = vppsubForm()
    context = {'form':form}
    if request.method == 'POST':
        form = vppsubForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data['walletid']
            user = request.user.username
            suber = form.save(commit=False)
            if vppsub.objects.filter(partner=user).exists():
                 messages.warning(request, 'you have already submitted your payment details for confirmation, Check your unit balance')
            else:
                suber.partner = user
                suber.walletid = id
                suber.save()
        messages.success(request, 'Your units have been deposited into your account.')
        return redirect  ('/members/agent/feeverify')
    return render(request,'members/subswallet.html', context)

@(login_required(login_url='user:log_in'))
def iduploadsuccess(request):
    return render(request,'members/iduploadsuccess.html')

@(login_required(login_url='user:log_in'))
def agentoruser(request):
    user = request.user.username
    if  Agent.objects.filter(username=user).exists():
        return redirect('/members/agt/profile')
    else: 
        return redirect('/members/user/profile')

@(login_required(login_url='user:log_in'))
def odata(request):
    form = orphanageForm()
    context = {'form':form}
    if request.method == 'POST':
        form = orphanageForm(request.POST, request.FILES)
        if form.is_valid():
            odata = form.save( commit=False)
            odata.agent = request.user.username
            
            odata.save()
            return HttpResponse('Orphanage Data Uploaded Successfully!')
    return render(request,'members/orphanage.html', context)

@method_decorator(login_required(login_url='user:log_in'), name='dispatch')
class Task(View):
    task = None

    def dispatch(self, request, *args, **kwargs):
        self.profile, __ = Profile.objects.get_or_create(user=request.user)
        return super(Task, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {'profile': self.profile, 'segment': 'profile'}
        
        return render(request,'members/task.html', context)

@method_decorator(login_required(login_url='user:log_in'), name='dispatch')
class Outvoice(View):
    outvoice = None

    def dispatch(self, request, *args, **kwargs):
        self.profile, __ = Profile.objects.get_or_create(user=request.user)
        return super(Outvoice, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {'profile': self.profile, 'segment': 'profile'}
        
        return render(request,'members/outvoice.html', context)
    
@(login_required(login_url='user:log_in'))
def outray(request):
    user = request.user.username
    vid = request.user.id
    sender = Profile.objects.get(user_id=vid)
    sbalance = int(sender.balance)
    
    form = transactionForm()
    form1 = vpp_balanceForm()
    form2 = ProfileForm()
    context = {'form':form, 'sbalance':sbalance}
    if request.method == 'POST':
        form = transactionForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            withdraw = form.save(commit=False)
            remain = int(sbalance) - int(amount)

            
                 
            if remain < 0:
                messages.error(request, 'Insufficient balance.')
            else:
                receiver = vpp_balance.objects.get(vpp_id = 1)
                addbalance = int(receiver.unit) + int(amount)
                (receiver.unit) = addbalance
                


                withdraw.username = user
                withdraw.viapps = 'Raymas'
                withdraw.save()
                
            
                form1 = form1.save(commit=False)
                receiver.save()
               
                form2 = form2.save(commit=False)
                (sender.balance) = remain
                sender.save()
                messages.success(request, 'Your transfer was successful.')
    return render(request,'members/outray.html', context)

@(login_required(login_url='user:log_in'))
def contray(request):
        return render(request, 'members/contray.html') 

@(login_required(login_url='user:log_in'))
def outmsa(request):
    user = request.user.username
    vid = request.user.id
    sender = Profile.objects.get(user_id=vid)
    sbalance = int(sender.balance)
    
    form = transactionForm()
    form1 = vpp_balanceForm()
    form2 = ProfileForm()
    context = {'form':form, 'sbalance':sbalance}
    if request.method == 'POST':
        form = transactionForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            withdraw = form.save(commit=False)
            remain = int(sbalance) - int(amount)

            
                 
            if remain < 0:
                messages.error(request, 'Insufficient balance.')
            else:
                receiver = vpp_balance.objects.get(vpp.id = 3)
                addbalance = int(receiver.unit) + int(amount)
                (receiver.unit) = addbalance
                


                withdraw.username = user
                withdraw.viapps = 'M.Musa'
                withdraw.save()
                
            
                form1 = form1.save(commit=False)
                receiver.save()
               
                form2 = form2.save(commit=False)
                (sender.balance) = remain
                sender.save()
                messages.success(request, 'Your transfer was successful.')
    return render(request,'members/outmsa.html', context)


@(login_required(login_url='user:log_in'))
def contmsa(request):
        return render(request, 'members/contmsa.html') 


@(login_required(login_url='user:log_in'))
@(login_required(login_url='user:log_in'))
def outvic(request):
    user = request.user.username
    vid = request.user.id
    sender = Profile.objects.get(user_id=vid)
    sbalance = int(sender.balance)
    
    form = transactionForm()
    form1 = vpp_balanceForm()
    form2 = ProfileForm()
    context = {'form':form, 'sbalance':sbalance}
    if request.method == 'POST':
        form = transactionForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            withdraw = form.save(commit=False)
            remain = int(sbalance) - int(amount)

            
                 
            if remain < 0:
                messages.error(request, 'Insufficient balance.')
            else:
                receiver = vpp_balance.objects.get(vpp_id = 2)
                addbalance = int(receiver.unit) + int(amount)
                (receiver.unit) = addbalance
                


                withdraw.username = user
                withdraw.viapps = 'Victory'
                withdraw.save()
                
            
                form1 = form1.save(commit=False)
                receiver.save()
               
                form2 = form2.save(commit=False)
                (sender.balance) = remain
                sender.save()
                messages.success(request, 'Your transfer was successful.')
    return render(request,'members/outvic.html', context)


@(login_required(login_url='user:log_in'))
def contvic(request):
        return render(request, 'members/contvic.html') 


@(login_required(login_url='user:log_in'))
def outmsn(request):
    user = request.user.username
    vid = request.user.id
    sender = Profile.objects.get(user_id=vid)
    sbalance = int(sender.balance)
    
    form = transactionForm()
    form1 = vpp_balanceForm()
    form2 = ProfileForm()
    context = {'form':form, 'sbalance':sbalance}
    if request.method == 'POST':
        form = transactionForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            withdraw = form.save(commit=False)
            remain = int(sbalance) - int(amount)

            
                 
            if remain < 0:
                messages.error(request, 'Insufficient balance.')
            else:
                receiver = vpp_balance.objects.get(vpp.id = 4)
                addbalance = int(receiver.unit) + int(amount)
                (receiver.unit) = addbalance
                


                withdraw.username = user
                withdraw.viapps = 'Muhsin'
                withdraw.save()
                
            
                form1 = form1.save(commit=False)
                receiver.save()
               
                form2 = form2.save(commit=False)
                (sender.balance) = remain
                sender.save()
                messages.success(request, 'Your transfer was successful.')
    return render(request,'members/outmsn.html', context)


@(login_required(login_url='user:log_in'))
def contmsn(request):
        return render(request, 'members/contmsn.html')     
    


