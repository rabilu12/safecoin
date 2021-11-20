from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
#from django.contrib.staticfiles.templatetags.staticfiles import static


class Profile(models.Model):
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_CHOICES = [
        (GENDER_MALE, _("Male")),
        (GENDER_FEMALE, _("Female")),
    ]

    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="members/profiles/avatars/", null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    number = models.CharField(max_length=32, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    zip = models.CharField(max_length=30, null=True, blank=True)
    

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    @property
    def get_avatar(self):
        return self.avatar.url if self.avatar else ('assets/img/team/default-profile-picture.png')


class Vpp(models.Model):
    user = models.OneToOneField(User, related_name="Vpp", on_delete=models.CASCADE)
    country = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=32, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True, default='Newyork')
    zip = models.CharField(max_length=30, null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Vpp')
        verbose_name_plural = _('Vpps')

    @property
    def get_selfie(self):
        return self.selfie.url if self.selfie else ('assets/img/team/default-profile-picture.png')

class Vpp_verified(models.Model):
    user = models.OneToOneField(User, related_name="Vpp_verified", on_delete=models.CASCADE)
    id_card_front = models.ImageField(upload_to="members/idcard", null=True, blank=True)
    id_card_back = models.ImageField(upload_to="members/idcard", null=True, blank=True)
    selfie = models.ImageField(upload_to="members/selfie", null=True, blank=True)
    id_number = models.CharField(max_length=32, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Vpp_verified')
        verbose_name_plural = _('Vpps_verified')

class Vpp_bank(models.Model):
    user = models.OneToOneField(User, related_name="Vpp_bank", on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=255, null=True, blank=True)
    acct_number = models.CharField(max_length=32, null=True, blank=True)
    acct_name = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Vpp_bank')
        verbose_name_plural = _('Vpps_bank')


class Paid(models.Model):
    username = models.CharField(max_length=32, null=True, blank=True)
    vpp = models.CharField( max_length=32, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('payment')
        verbose_name_plural = _('payments')
    

class Agent(models.Model):
    Qualification_masters = 1
    Qualification_B_degree = 2
    Qualification_Diploma = 3
    Qualification_High_school = 4
    Qualification_CHOICES = [
        (Qualification_masters, _("Masters Degree")),
        (Qualification_B_degree, _("Bachelor Degree")),
        (Qualification_Diploma, _("National Diploma")),
        (Qualification_High_school, _("High School")),
    ]
    Category_Voluntary = 1
    Category_Paid = 2
    Category_CHOICES = [
        (Category_Voluntary, _("Voluntary")),
        (Category_Paid, _("Paid")),
    ]
    user = models.OneToOneField(User, related_name="agent", on_delete=models.CASCADE, null=False, blank=False)
    username = models.CharField(max_length=255, null=False, blank=False)
    phone = models.CharField(max_length=32, null=False, blank=False)
    country = models.CharField(max_length=255, null=False, blank=False)
    state = models.CharField(max_length=32, null=False, blank=False)
    city = models.CharField(max_length=50, null=False, blank=False)
    category = models.PositiveSmallIntegerField(choices=Category_CHOICES, null=False, blank=False)
    qualification = models.PositiveSmallIntegerField(choices=Qualification_CHOICES, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    task = models.CharField(max_length=1000, null=True, blank=True)
    taskaddress = models.CharField(max_length=1000, null=True, blank=True)
    taskreward = models.IntegerField(null=True, blank=True)
    balance = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = _('Agent')
        verbose_name_plural = _('Agents')

    @property
    def get_selfie(self):
        return self.selfie.url if self.selfie else ('assets/img/team/default-profile-picture.png')


class Agent_verified(models.Model):
    user = models.OneToOneField(User, related_name="Agent_verified", on_delete=models.CASCADE)
    id_card_front = models.ImageField(upload_to="members/fidcard", null=True, blank=True)
    id_card_back = models.ImageField(upload_to="members/bidcard", null=True, blank=True)
    selfie = models.ImageField(upload_to="members/selfie", null=True, blank=True)
    qualification = models.ImageField(upload_to="members/certificate", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Agent_verified')
        verbose_name_plural = _('Agents_verified')

class vppsub(models.Model):
    
    partner = models.CharField(max_length=32, null=True, blank=True)
    walletid = models.CharField(max_length=32, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('vppsub')
        verbose_name_plural = _('vppsubs')
def __str__(self):
        return self.vppsub,self.username

class vpp_balance(models.Model):
    vpp = models.OneToOneField(User, related_name="balance", on_delete=models.CASCADE)
    unit = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)


    def __int__(self):
        return self.vpp_id,self.unit
    
    
class orphanage(models.Model):
    agent = models.CharField(max_length=36, null=True, blank=True)
    oname = models.CharField(max_length=300, null=True, blank=True)
    oaddress = models.CharField(max_length=500, null=True, blank=True)
    headfullname = models.CharField(max_length=35, null=True, blank=True)
    headcontact = models.CharField(max_length=32, null=True, blank=True)
    numberofchildren = models.IntegerField(null=True, blank=True)
    image1 = models.ImageField(upload_to="members/ocenter/pics", null=True, blank=True)
    image2 = models.ImageField(upload_to="members/ocenter/pics", null=True, blank=True)
    image3 = models.ImageField(upload_to="members/ocenter/pics", null=True, blank=True)

    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Orphanage')
        verbose_name_plural = _('Orphanagess')

    @property
    def get_avatar(self):
        return self.avatar.url if self.avatar else ('assets/img/team/default-profile-picture.png')

   

        

class Transaction(models.Model):
    username = models.CharField(max_length=36, null=True, blank=True)
    amount = models.PositiveIntegerField(null=True, blank=True)
    viapps = models.CharField( max_length=32, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('transaction')
        verbose_name_plural = _('transactionss')
    
    
class Circle(models.Model):
    rootuser = models.CharField(max_length=36, null=True, blank=True)
    user = models.CharField(max_length=36, null=True, blank=True)

    date = models.DateTimeField(auto_now_add=True)

        
