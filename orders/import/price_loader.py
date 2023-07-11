import yaml
from pprint import pprint
from orders.backend_app.models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter


from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

with open("../../shop1.yaml", 'r', encoding='utf-8') as file:
    try:
        data = load(file, Loader=Loader)
    except yaml.YAMLError as exc:
        print(exc)

# print(type(data))
# pprint(data)
for obj, attr in data.items():
    if obj == 'shop':
        shop = Shop.objects.create(id=attr['id'],
                                       name=attr['name'])
        shop.save()
        print(f'{shop} сохранен в базе')
        print()

    if obj == 'categories':
        for ctg in obj:
            category = Category.objects.create(id=ctg['id'],
                                               name=ctg['name'])
            category.save()
            print(f'{category} сохранен в базе')
            print()
    print('Загрузка прайс-листа завершена')
