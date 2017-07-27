web server based on django-1.6 and django-restframework2.4.8.
using bootstrap and Jquery to demonstrate the data.

required package:
1. django 1.6.X
2. django-rest-framework-2.X.X
3. other modules

The remote terminal hasn't been uploaded. So you can design it on your own.

INSTALL GUIDE:
step 1: git clone xxxx
step 2: cd to project dir, using "pip install -r requirements.txt" to install required package
step 3: using "python manage.py syncdb" to create your own database.
step 4: run test server or deploy the server in apache/nginx.

-----------------------------
function:
1. MAC-IP bind and management
2. devices params management
3. user management.

in develop:
1. verify api-key in exposed json-api.
2. UX adjustment.
3. remote terminal registration and management.

todo:
1. migrate to vue.js
2. design a module which can auto-generate bootstrap-style tempelates by models.