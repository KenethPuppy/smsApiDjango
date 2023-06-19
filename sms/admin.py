from django.contrib import admin
from django.contrib.auth.models import Group, User

from sms.models import Sms, PhoneNumber, Activation

# Register your models here.
admin.site.unregister(User)
admin.site.unregister(Group)

# admin.site.register(Sms)
@admin.register(PhoneNumber)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ("phone", "operator", "country",)
    search_fields = ("phone", "operator", "country",)
    exclude = ('services',)

@admin.register(Sms)
class SmsAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "phone_from", "text", "sended")
    search_fields = ("phone_number", "phone_from", "text")

    def has_add_permission(self, request):
        return False

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("phone", "phone_from", "text", "sended")
        return self.readonly_fields

@admin.register(Activation)
class ActivationAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "service", "finished", "paid", "profit")
    search_fields = ("phone_number", "service", "finished", "paid", "profit")

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("phone_number", "service", "finished", "paid", "profit")
        return self.readonly_fields

    def has_add_permission(self, request):
        return False