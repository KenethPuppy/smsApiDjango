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
            data = read_json_file('sms/data.json')
            services_data = create_services_data(data)
            print(services_data)
            self.services = json.dumps(services_data)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.phone}"


def create_services_data(data_all_services,):
    services_data = []
    for service in data_all_services:
        service_name = service['name']
        service_data = {service_name: True, "try": 4}
        services_data.append(service_data)
    print(services_data)
    return services_data

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



def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data


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