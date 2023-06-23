import json
import time
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Sms, PhoneNumber, Activation
from .serializers import SmsSerializer, NumberSerializer
import requests
from collections import defaultdict
from django.conf import settings


def remove_plus_sign(text):
    if "+" in text:
        text = text.replace("+", "")
    return text

class SmsCreateView(APIView):
    def post(self, request):
        serializer = SmsSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data.get('phone')
            try:
                phone_number = PhoneNumber.objects.get(phone=phone)
                phone_from = serializer.validated_data.get('phone_from')
                phone_from = remove_plus_sign(phone_from)
                sms = Sms(phone_number=phone_number, phone_from=phone_from,
                          text=serializer.validated_data.get('text'))
                sms.save()
                '''response = send_sms_to_hub(text=sms.text, phone=int(phone), phone_from=sms.phone_from,
                                           sms_id=int(sms.id))
                if response.get('status') == 'SUCCESS':
                    sms.sended = True
                    sms.save()
                else:
                    while response.get('status') != 'SUCCESS':
                        time.sleep(10)
                        response = send_sms_to_hub(text=sms.text, phone=sms.phone, phone_from=sms.phone_from,
                                                   sms_id=sms.id)
                    sms.sended = True
                    sms.save()'''
                return Response({'status': 'success'}, status=201)
            except PhoneNumber.DoesNotExist:
                return Response({'status': 'error', 'message': 'Phone number does not exist'},
                                status=400)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class NumberView(APIView):
    def post(self, request):
        serializer = NumberSerializer(data=request.data)
        if serializer.is_valid():
            key = serializer.validated_data.get('key')
            if key != settings.PROTOCOL_KEY:
                return Response({"status": "ERROR", "error": "Ошибка в ключе протокола"})
            activation_id = None
            phone = None
            status_response = ''
            action = serializer.validated_data.get('action')
            if action == 'GET_NUMBER':
                activation = start_activation(serializer)
                if activation:
                    activation_id = activation.id
                    phone = activation.phone_number.phone
                    status_response = "SUCCESS"
                    return Response({"number": int(phone), "activationId": activation_id, "status": status_response},
                                    status=201)
                else:
                    status_response = "NO_NUMBERS"
                    return Response({"status": status_response},
                                    status=201)
            elif action == 'GET_SERVICES':
                all_numbers = get_all_numbers()
                status_response = "SUCCESS"
                return Response({"countryList": all_numbers, "status": status_response})
            elif action == 'FINISH_ACTIVATION':
                status = serializer.validated_data.get('status')
                activation_id = serializer.validated_data.get('activationId')
                if (status == 3) or (status == 1) or (status == 5):
                    try:
                        activation = Activation.objects.get(id=activation_id)
                        if not activation.finished:
                            activation.finished = True
                            if status == 3:
                                activation.paid = True
                            else:
                                activation.paid = False
                            activation.save()
                        status_response = "SUCCESS"
                        return Response({"status": status_response},
                                        status=201)
                    except Activation.DoesNotExist:
                        status_response = "ERROR"
                        return Response({"status": status_response, "error": "Активации не существует"})
                if status == 4:
                    try:
                        activation = Activation.objects.get(id=activation_id)
                        if not activation.finished:
                            phone_number = activation.phone_number
                            services = json.loads(phone_number.services)
                            for service_data in services:
                                if activation.service in service_data:
                                    if service_data["try"] > 0:
                                        service_data[activation.service] = True
                                        service_data["try"] -= 1
                                break
                            phone_number.services = json.dumps(services)
                            phone_number.save()

                            activation.finished = True
                            activation.save()

                        status_response = "SUCCESS"
                        return Response({"status": status_response}, status=201)
                    except Activation.DoesNotExist:
                        status_response = "ERROR"
                        return Response({"status": status_response, "error": "Активации не существует"})

        else:
            return Response(serializer.errors, status=400)


def check_phone_number(country, phone_number, phone_operator):
    matching_numbers = PhoneNumber.objects.filter(country=country, phone=phone_number, operator=phone_operator)
    if matching_numbers.exists():
        return True
    else:
        return False


def get_all_numbers():
    phone_numbers = PhoneNumber.objects.all()

    country_operator_map = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

    for phone_number in phone_numbers:
        country = phone_number.country
        operator = phone_number.operator
        service_list = json.loads(phone_number.services)

        for service_data in service_list:
            for service, value in service_data.items():
                if service != "try":
                    country_operator_map[country][operator][service] += int(value)
    country_list = []
    for country, operator_map in country_operator_map.items():
        country_entry = {
            'country': country,
            'operatorMap': {}
        }

        for operator, service_map in operator_map.items():
            service_counts = {
                service: count
                for service, count in service_map.items()
            }

            operator_entry = {
                operator: service_counts
            }

            country_entry['operatorMap'].update(operator_entry)

        country_list.append(country_entry)

    print(country_list)
    return country_list

def send_sms_to_hub(text, phone, phone_from, sms_id):
    url = 'https://mysite.com/api/'  # Укажите корректный URL вашего API на mysite.com
    data = {
        'text': text,
        'phone': phone,
        'phoneFrom': phone_from,
        'smsId': sms_id,
        'action': 'PUSH_SMS',
        'key': settings.PROTOCOL_KEY
    }

    # Выполняем POST-запрос на mysite.com
    response = requests.post(url, data=data)
    return response


def start_activation(serializer):
    operator = serializer.validated_data.get('operator')
    country = serializer.validated_data.get('country')
    service = serializer.validated_data.get('service')
    profit = serializer.validated_data.get('sum')
    exception_phone_set = serializer.validated_data.get('exceptionPhoneSet', [])
    phone_numbers = PhoneNumber.objects.filter(operator=operator, country=country)

    for phone_number in phone_numbers:
        if phone_number.phone in exception_phone_set:
            continue
        services = phone_number.services
        if services:
            services_list = json.loads(services)

            for service_data in services_list:
                if service in service_data:
                    if service_data[service]:
                        service_data[service] = False
                        phone_number.services = json.dumps(services_list)
                        phone_number.save()
                        activation = Activation(phone_number=phone_number, service=service, profit=profit)
                        activation.save()
                        return activation

    return None

