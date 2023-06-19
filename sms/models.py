import json
from django.db import models

# Create your models here.



class PhoneNumber(models.Model):
    class Meta:
        db_table = 'phone_number'
        verbose_name_plural = "Номера телефонов"

    phone = models.BigIntegerField(verbose_name="Номер телефона")
    operator = models.TextField(max_length=100, verbose_name="Мобильный оператор")
    country = models.TextField(max_length=100, verbose_name="Страна")
    services = models.JSONField(default=None)

    def save(self, *args, **kwargs):
        if self.pk is None and self.services is None:
            print(self.pk)
            services_data = [
                {"vk": True, "try": 4},
                {"face": True, "try": 4},
                {"tiktok": True, "try": 4}
            ]
            self.services = json.dumps(services_data)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.phone}"


class Activation(models.Model):
    phone_number = models.ForeignKey(PhoneNumber, on_delete=models.CASCADE, verbose_name="Номер телефона")
    service = models.CharField(max_length=100, verbose_name="Сервис")
    finished = models.BooleanField(default=False, verbose_name="Активация закончена")
    paid = models.BooleanField(default=False, verbose_name="Оплата")
    profit = models.DecimalField(verbose_name="Доход", max_digits=10, decimal_places=2, default=0)
    class Meta:
        db_table = 'activation'
        verbose_name_plural = "Активации"



class Sms(models.Model):
    class Meta:
        db_table = 'sms'
        verbose_name_plural = "Смс"
    #сделать связь с номером телефона
    phone_number = models.ForeignKey(PhoneNumber, on_delete=models.CASCADE, verbose_name="Номер телефона", default=None)
    phone_from = models.TextField(verbose_name="Номер отправителя")
    text = models.TextField(verbose_name="Текст смс")
    sended = models.BooleanField(default=False, verbose_name="Принято")




'''def save(self, *args, **kwargs):
phone = models.BigIntegerField(verbose_name="Номер телефона")
        if self.pk is None and self.services is None:
            print(self.pk)
            services_data = {
                "vk": True,
                "face": True,
                "tiktok": True
            }
            self.services = json.dumps(services_data)
        super().save(*args, **kwargs)'''