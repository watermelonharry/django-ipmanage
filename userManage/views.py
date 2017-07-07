from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.template import RequestContext


# Create your views here.


def user_login(request):

	if request.method == 'GET':
		return render(request, 'user_login.html')

	if request.method == 'POST':
		user_name = request.POST.get('user_name')
		password = request.POST.get('password')
		verified_user = authenticate(username= user_name, password=password)

		if verified_user is not None:
			if verified_user.is_active:
				return render(request, '<p>login success</p>')
			else:
				pass
		else:
			return request(request, '<p>invalid combination</p>')