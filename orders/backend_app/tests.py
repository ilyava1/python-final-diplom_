from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from backend_app.models import Company, User, Product, Order, Contact


# Для запука теста из командной строки терминала находясь в директории
# python-final-project\orders набрать:
# python manage.py test backend_app.tests

class RegisterNewAccountTests(APITestCase):
    def setUp(self):
        self.company = Company.objects.create(company_name='Mobilka')

    def test_register_correct_accounts(self):
        print()
        print(f'---- START test_register_correct_accounts ----')

        url = reverse('registration')
        data = {
            "first_name": "Alex",
            "last_name": "Alekseev",
            "middle_name": "Ivanovich",
            "username": "aalex",
            "email": "aalex1@mail.ru",
            "password": "1qaz2wsx",
            "position": "Purchase manager",
            "phone": "8-926-123-44-55",
            "company_name": "Mobilka",
            "adress": "Moscow, Brateevskaya, 4"
        }
        my_response = self.client.post(url, data, format='json')
        self.assertEqual(my_response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'aalex')
        new_user = User.objects.get(username='aalex')
        print(f'Shop user registrated: id={new_user.id}, username - {new_user.username}')
        print(f'---- FINISHED test_register_correct_accounts ----')
        print()


    def test_register_uncorrect_accounts_with_incomplete_data(self):
        print(f'---- START test_register_uncorrect_accounts_with_incomplete_data ----')
        url = reverse('registration')
        data = {
            "first_name": "Alex",
            "last_name": "Alekseev",
            "middle_name": "Ivanovich",
            "username": "aalex"
        }
        my_response = self.client.post(url, data, format='json')
        self.assertEqual(my_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        print('Incomplete data, registration denied')
        print(f'---- FINISHED test_register_uncorrect_accounts_with_incomplete_data ----')
        print()

    def test_register_uncorrect_accounts__with_empty_data(self):
        print(f'---- START test_register_uncorrect_accounts__with_empty_data ----')
        url = reverse('registration')
        data = {
            "first_name": "Ivan",
            "last_name": "Ivanov",
            "middle_name": "Ivanovich",
            "username": "",
            "email": "iivan@mail.ru",
            "password": "1qaz2wsx",
            "position": "Ivanovo branch director",
            "phone": "",
            "company_name": "",
            "adress": "Ivanova, Moskovskay ul, 8"
        }
        my_response = self.client.post(url, data, format='json')
        self.assertEqual(my_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        print('Empty registration data, registration denied')
        print(f'---- FINISHED test_register_uncorrect_accounts__with_empty_data ----')
        print()

class RegisterExistAccountTests(APITestCase):
    def setUp(self):
        self.company = Company.objects.create(company_name='Mobilka')
        self.user = User.objects.create(first_name="Alex",
                                        last_name="Alekseev",
                                        username="aalex",
                                        email="aalex1@mail.ru",
                                        password="1qaz2wsx")
        self.contact = Contact.objects.create(company = self.company,
                                              user = self.user)

    def test_register_exist_accounts(self):
        print(f'---- START test_register_exist_accounts ----')
        url = reverse('registration')
        data = {
            "first_name": "Alex",
            "last_name": "Alekseev",
            "middle_name": "Ivanovich",
            "username": "aalex",
            "email": "aalex1@mail.ru",
            "password": "1qaz2wsx",
            "position": "Purchase manager",
            "phone": "8-926-123-44-55",
            "company_name": "Mobilka",
            "adress": "Moscow, Brateevskaya, 4"
        }
        my_response = self.client.post(url, data, format='json')
        self.assertEqual(my_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        print(f'Contact already exists, registration denied')
        print(f'---- FINISHED test_register_exist_accounts ----')
        print()


class AuthorizationTests(APITestCase):
    def setUp(self):
        self.company = Company.objects.create(company_name='reStore',
                                              type='supplier')
        url = reverse('registration')
        data = {
            "first_name": "Igor",
            "last_name": "Korolev",
            "middle_name": "Ivanovich",
            "username": "ikorol",
            "email": "ikorol@mail.ru",
            "password": "1qaz2wsx",
            "position": "Sales manager",
            "phone": "8-926-443-23-43",
            "company_name": "reStore",
            "adress": "Moscow, Brateevskaya, 44"
        }
        self.client.post(url, data, format='json')


    def test_authorization(self):
        print()
        print(f'---- START test_authorizations ----')
        new_user = User.objects.get(id=1)
        print(f'Supplier user: id={new_user.id}, username - {new_user.username}')
        url = reverse('api_token_auth')
        data = {
            "username": new_user.username,
            "password": "1qaz2wsx"
        }
        my_response = self.client.post(url, data, format='json')
        self.assertEqual(my_response.status_code, status.HTTP_200_OK)
        print(f'Received token: {my_response.data}')
        print(f'---- FINISHED test_authorizations ----')
        print()


class LoadPriceTests(APITestCase):
    def setUp(self):
        self.company = Company.objects.create(id=2, company_name='reStore',
                                              type='supplier')
        url = reverse('registration')
        data = {
            "first_name": "Igor",
            "last_name": "Korolev",
            "middle_name": "Ivanovich",
            "username": "ikorol",
            "email": "ikorol@mail.ru",
            "password": "1qaz2wsx",
            "position": "Sales manager",
            "phone": "8-926-443-23-43",
            "company_name": "reStore",
            "adress": "Moscow, Brateevskaya, 44"
        }
        self.client.post(url, data, format='json')

        new_user = User.objects.get(id=1)
        url = reverse('api_token_auth')
        data = {
            "username": new_user.username,
            "password": "1qaz2wsx"
        }
        my_response = self.client.post(url, data, format='json')
        self.token = my_response.data['token']
        self.user = new_user

    def test_load_price(self):
        print()
        print(f'---- START test_load_price ----')
        url = reverse('price_import')
        responce = self.client.post(url, format='json', HTTP_AUTHORIZATION='Token ' + self.token)
        self.assertEqual(responce.status_code, status.HTTP_200_OK)
        print(f'Price list uploaded successfully')
        supplier = Company.objects.get(company_name='reStore')
        print(f'Supplier: id={supplier.id}, {supplier.company_name}')
        queryset = Product.objects.all()
        print('Products:')
        for product in queryset:
            print(product)
        print(f'---- FINISHED test_load_price ----')
        print()


class BrowseCatalogTests(APITestCase):
    def setUp(self):
        self.company = Company.objects.create(id=2, company_name='reStore',
                                              type='supplier')
        url = reverse('registration')
        data = {
            "first_name": "Igor",
            "last_name": "Korolev",
            "middle_name": "Ivanovich",
            "username": "ikorol",
            "email": "ikorol@mail.ru",
            "password": "1qaz2wsx",
            "position": "Sales manager",
            "phone": "8-926-443-23-43",
            "company_name": "reStore",
            "adress": "Moscow, Brateevskaya, 44"
        }
        self.client.post(url, data, format='json')

        new_user = User.objects.get(id=1)
        url = reverse('api_token_auth')
        data = {
            "username": new_user.username,
            "password": "1qaz2wsx"
        }
        my_response = self.client.post(url, data, format='json')
        self.token = my_response.data['token']
        self.user = new_user

        url = reverse('price_import')
        responce = self.client.post(url, format='json', HTTP_AUTHORIZATION='Token ' + self.token)


    def test_browse_catalog(self):
        print()
        print(f'---- START test_browse_catalog ----')
        url = 'http://127.0.0.1:8000/api/product/catalog/'
        responce = self.client.get(url, format='json', HTTP_AUTHORIZATION='Token ' + self.token)
        self.assertEqual(responce.status_code, status.HTTP_200_OK)
        print('Catalog displayed')
        print(f'---- FINISHED test_browse_catalog ----')
        print()

class AddProductToOrderTests(APITestCase):
    def setUp(self):
        self.company = Company.objects.create(id=2, company_name='reStore',
                                              type='supplier')
        url = reverse('registration')
        data = {
            "first_name": "Igor",
            "last_name": "Korolev",
            "middle_name": "Ivanovich",
            "username": "ikorol",
            "email": "ikorol@mail.ru",
            "password": "1qaz2wsx",
            "position": "Sales manager",
            "phone": "8-926-443-23-43",
            "company_name": "reStore",
            "adress": "Moscow, Brateevskaya, 44"
        }
        self.client.post(url, data, format='json')

        new_user = User.objects.get(id=1)
        url = reverse('api_token_auth')
        data = {
            "username": new_user.username,
            "password": "1qaz2wsx"
        }
        my_response = self.client.post(url, data, format='json')
        self.token = my_response.data['token']
        self.user = new_user

        url = reverse('price_import')
        responce = self.client.post(url, format='json', HTTP_AUTHORIZATION='Token ' + self.token)


    def test_add_product_to_order(self):
        print()
        print(f'---- START add_product_to_order ----')
        url = 'http://127.0.0.1:8000/api/product/order/add/4216292/2/2/'
        responce = self.client.post(url, format='json', HTTP_AUTHORIZATION='Token ' + self.token)
        self.assertEqual(responce.status_code, status.HTTP_200_OK)
        product = Product.objects.get(id=4216292)
        order = Order.objects.get()
        print(f'Product "{product.name}" added to order with id={order.id}')
        print(f'---- FINISHED add_product_to_order ----')
        print()

class DeleteProductFromOrderTests(APITestCase):
    def setUp(self):
        self.company = Company.objects.create(id=2, company_name='reStore',
                                              type='supplier')
        url = reverse('registration')
        data = {
            "first_name": "Igor",
            "last_name": "Korolev",
            "middle_name": "Ivanovich",
            "username": "ikorol",
            "email": "ikorol@mail.ru",
            "password": "1qaz2wsx",
            "position": "Sales manager",
            "phone": "8-926-443-23-43",
            "company_name": "reStore",
            "adress": "Moscow, Brateevskaya, 44"
        }
        self.client.post(url, data, format='json')

        new_user = User.objects.get(id=1)
        url = reverse('api_token_auth')
        data = {
            "username": new_user.username,
            "password": "1qaz2wsx"
        }
        my_response = self.client.post(url, data, format='json')
        self.token = my_response.data['token']
        self.user = new_user

        url = reverse('price_import')
        responce = self.client.post(url, format='json', HTTP_AUTHORIZATION='Token ' + self.token)

        url = 'http://127.0.0.1:8000/api/product/order/add/4216292/2/2/'
        responce = self.client.post(url, format='json', HTTP_AUTHORIZATION='Token ' + self.token)

    def test_del_product_from_order(self):
        print()
        print(f'---- START test_del_product_from_order ----')
        url = 'http://127.0.0.1:8000/api/product/order/delete/1/4216292/2/1/'
        responce = self.client.delete(url, format='json', HTTP_AUTHORIZATION='Token ' + self.token)
        self.assertEqual(responce.status_code, status.HTTP_200_OK)
        product = Product.objects.get(id=4216292)
        order = Order.objects.get()
        print(f'Product "{product.name}" deleted from order with id={order.id}')
        print(f'---- FINISHED test_del_product_from_order ----')
        print()


class ViewOrderTests(APITestCase):
    def setUp(self):
        self.company = Company.objects.create(id=2, company_name='reStore',
                                              type='supplier')
        url = reverse('registration')
        data = {
            "first_name": "Igor",
            "last_name": "Korolev",
            "middle_name": "Ivanovich",
            "username": "ikorol",
            "email": "ikorol@mail.ru",
            "password": "1qaz2wsx",
            "position": "Sales manager",
            "phone": "8-926-443-23-43",
            "company_name": "reStore",
            "adress": "Moscow, Brateevskaya, 44"
        }
        self.client.post(url, data, format='json')

        new_user = User.objects.get(username='ikorol')
        url = reverse('api_token_auth')
        data = {
            "username": new_user.username,
            "password": "1qaz2wsx"
        }
        my_response = self.client.post(url, data, format='json')
        self.token = my_response.data['token']
        self.user = new_user

        url = reverse('price_import')
        responce = self.client.post(url, format='json', HTTP_AUTHORIZATION='Token ' + self.token)

        url = 'http://127.0.0.1:8000/api/product/order/add/4216292/2/2/'
        responce = self.client.post(url, format='json', HTTP_AUTHORIZATION='Token ' + self.token)

    def test_view_order(self):
        print()
        print(f'---- START test_view_order ----')
        url = 'http://127.0.0.1:8000/api/product/order/view_order/1/'
        responce = self.client.get(url, format='json', HTTP_AUTHORIZATION='Token ' + self.token)
        self.assertEqual(responce.status_code, status.HTTP_200_OK)
        print(f'Order displayed')
        print(f'---- FINISHED test_view_order ----')
        print()

class ViewOrderHistoryTests(APITestCase):
    def setUp(self):
        self.company = Company.objects.create(id=2, company_name='reStore',
                                              type='supplier')
        url = reverse('registration')
        data = {
            "first_name": "Igor",
            "last_name": "Korolev",
            "middle_name": "Ivanovich",
            "username": "ikorol",
            "email": "ikorol@mail.ru",
            "password": "1qaz2wsx",
            "position": "Sales manager",
            "phone": "8-926-443-23-43",
            "company_name": "reStore",
            "adress": "Moscow, Brateevskaya, 44"
        }
        self.client.post(url, data, format='json')

        new_user = User.objects.get(username='ikorol')
        url = reverse('api_token_auth')
        data = {
            "username": new_user.username,
            "password": "1qaz2wsx"
        }
        my_response = self.client.post(url, data, format='json')
        self.token = my_response.data['token']
        self.user = new_user

        url = reverse('price_import')
        responce = self.client.post(url, format='json', HTTP_AUTHORIZATION='Token ' + self.token)

        url = 'http://127.0.0.1:8000/api/product/order/add/4216292/2/2/'
        responce = self.client.post(url, format='json', HTTP_AUTHORIZATION='Token ' + self.token)

    def test_view_order_history(self):
        print()
        print(f'---- START test_view_order_history ----')
        url = 'http://127.0.0.1:8000/api/product/order/view_order_history/'
        responce = self.client.get(url, format='json', HTTP_AUTHORIZATION='Token ' + self.token)
        self.assertEqual(responce.status_code, status.HTTP_200_OK)
        print(f'Order history displayed')
        print(f'---- FINISHED test_view_order_history ----')
        print()