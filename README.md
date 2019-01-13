## Django ecommerce platform

Purley learning project, it features:
* prices have validity start date, always newest price is used
* promotion is bound to price
* images are stored separetly, one image can be used for many products
* each order has delivery calculated basing of weight of products

App is splited into two parts:
* webstore - which is basic models and store front views
* dashboard - custom admin panel for store managment


### Running the project:

Assuming you have  docker / docker-compose installed:

```
docker-compose up --build
```

After docker downloads the images and creates containers:

```
docker exec -ti django_webstore bash
./manage.py migrate --settings=config.settings.docker
./manage.py createsuperuser --settings=config.settings.docker
exit
```

Webstore will be avaliable at:
*http://localhost:8000*

Custom admin panel:
*http://localhost:8000/dashboard/users_panel/login*

Default django admin panel:
*http://localhost:8000/admin*

Making and order in test project
* Each product needs to have at least one category - create it before adding a product
* Product withouth price won`t be avaliable in store - add a price after creating a product
* Images are stored independently from products - add a picutre, and attach it to product
* Set up and delivery option from the dashboard/admin panel

### Running the tests

First start the app in seperate terminal

Tests for dashboard 
```
docker exec -ti django_webstore bash
./manage.py test dashboard --settings=config.settings.docker
```
Testing for webstore
```
docker exec -ti django_webstore bash
./manage.py test webstore --settings=config.settings.docker
```