from django.contrib import admin

from members.models import Agent, Agent_verified, Profile, Paid, Vpp, vpp_balance, vppsub

admin.site.register(Profile)
admin.site.register(Agent)
admin.site.register(Paid)
admin.site.register(Vpp)
admin.site.register(vpp_balance)
admin.site.register(vppsub)
admin.site.register(Agent_verified)




