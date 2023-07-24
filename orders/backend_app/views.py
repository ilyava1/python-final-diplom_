from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Category, Company, Contact
from .serializers import ContactSerializer, CompanySerializer, UserSerializer


class RegisterAccount(APIView):
    """
    Класс для регистрации покупателей
    """
    def post(self, request, *args, **kwargs):
        contact_save_ready_status = True
        contact_save_dict = {}
        # Сначала проверяем компанию
        if {'company_name'}.issubset(request.data):
            exist_company = Company.objects.filter(company_name=request.data['company_name'])
            if exist_company.exists() == False:
                contact_save_dict['Company_check'] = f'Info: Company ' \
                                                 f'{request.data["company_name"]}' \
                                                 f' doesnt exist in the database yet'
            else:
                contact_save_dict['Company_check'] = f'Info: Company ' \
                                                     f'{request.data["company_name"]}' \
                                                     f' already exists in the database'
        else:
            contact_save_ready_status = False
            contact_save_dict['Company_check'] = 'Error! Company_name required'

        # Далее проверяем пользователя
        if {'first_name', 'last_name', 'username', 'email'}.issubset(request.data):
            exist_user = User.objects.filter(email=request.data['email'])
            if exist_user.exists() == False:
                contact_save_dict['User_check'] = f'Info: User ' \
                                              f'{request.data["username"]}' \
                                              f' doesnt exist in the database yet'
            else:
                contact_save_dict['User_check'] = f'Info: User ' \
                                                  f'{request.data["username"]}' \
                                                  f' already exists in the database'
        else:
            contact_save_ready_status = False
            contact_save_dict['User_check'] = 'Error! one of required ' \
                                              'fields is empty '

        # Далее проверяем контакт
        if exist_user.exists() == True and exist_company.exists() == True:
            if Contact.objects.filter(user=exist_user[0].id,
                                  company=exist_company[0].id).exists() == False:
                contact_save_dict['Contact_check'] = f'Info: Contact ' \
                                                 f'{request.data["username"]}' \
                                                 f' from {request.data["company_name"]}' \
                                                 f' doesnt exist in the database yet'
            else:
                contact_save_ready_status = False
                contact_save_dict['Contact_check'] = f'Error! Contact ' \
                                                 f'{request.data["username"]}' \
                                                 f' from {request.data["company_name"]}' \
                                                 f' already exists in the database'
        else:
            contact_save_dict['Contact_check'] = f'Info: Contact ' \
                                                 f'{request.data["username"]}' \
                                                 f' from {request.data["company_name"]}' \
                                                 f' doesnt exist in the database yet'

        if contact_save_ready_status == False:
            return JsonResponse({'Status': False, 'Detailes': contact_save_dict})

        #-----------------------------------------------------------------------------------

        # Если проверки компании и пользователя пройдены, то сохраняем новые объекты в базе
        input_data = request.data

        # Сохраняем компанию
        company_serializer = CompanySerializer(data=request.data)
        if company_serializer.is_valid():
            if exist_company.exists() == False:
                new_company = company_serializer.save()
                input_data['company'] = new_company.id
            else:
                input_data['company'] = exist_company[0].id
        else:
            contact_save_dict['Company_serializer'] = company_serializer.errors
            return JsonResponse({'Status': False, 'Detailes': contact_save_dict})

        # Сохраняем пользователя
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            if exist_user.exists() == False:
                new_user = user_serializer.save()
                new_user.set_password(request.data['password'])
                new_user.save()
                input_data['user'] = new_user.id
            else:
                input_data['user'] = exist_user[0].id
        else:
            contact_save_dict['User_serializer'] = user_serializer.errors
            return JsonResponse({'Status': False, 'Detailes': contact_save_dict})

        # Сохраняем контакт
        contact_serializer = ContactSerializer(data=input_data)
        if contact_serializer.is_valid():
           new_contact = contact_serializer.save()
           return JsonResponse({'Status': True,
                                'Final Message': f'Registration of contact id={new_contact.id},'
                                           f'user_name={new_user.username}, '
                                           f'company={new_company.company_name} '
                                                 f'completed successfully'})
        else:
            contact_save_dict['Contact_serializer'] = contact_serializer.errors
            return JsonResponse({'Status': False, 'Detailes': contact_save_dict})
