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
snapshots：
![main page](https://github.com/watermelonharry/django-ipmanage/blob/master/introduction/main_page.png)

-----------------------------
function:
1. MAC-IP bind and management(in reformatting)
2. devices params management
3. user management.
4. quick tools
5. file download management(the download requests will be redirected by nginx directly)
6. terminal api modules.

structure:
------
--basepkg: public modules
--dnstest: (disused) dns test module
--feedback: feedback module, prototype.
--filemanage: manage the download url.
--iottest: iot test module, using vue.
--ipcmanage: (in reformatting)
--ipcset: manage the devices' params.
--mySiteD: base folder, contains the django config files.
--static: static files, such as *.js *.ico *.css
--terminalReg: manage the terminal's registration.
--userManage: manage the users' profiles, providing user signup/verification services.
--terminalapi: a simple terminal dispatch module, contains a registration thread, a receiver thread(simple http server) and a mission-dispatcher thread.
-manage.py: django's powerful tool.
-requirement.txt: required packages.

todo:
1. verify api-key in exposed json-api.[done]
2. UX adjustment.[partly done]
3. remote terminal registration and management.[done]
4. reformatting ipmanage model.
5. migrate to vue.js[partly done].
6. design a module which can auto-generate bootstrap-style tempelates by models.
7. using the django(or nginx)'s cache system.
8. unittest for each module.