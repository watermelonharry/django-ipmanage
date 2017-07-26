# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from userManage.models import ApiKeyModel, UserApiModel


# from django.db.models.fields.related




# from django.contrib.auth.models import User




def user_login(request):
	if request.user.is_authenticated():
		return render(request, 'user_success.html', {'notice': u'您已登陆，即将跳转到主页...', 'next_url': u'/hello/'})

	if request.method == 'GET':
		return render(request, 'user_login.html', {'notice': u'欢迎登陆'})

	if request.method == 'POST':
		user_name = request.POST.get('user_name')
		password = request.POST.get('password')
		next = request.GET.get('next', '/')
		verified_user = authenticate(username=user_name, password=password)

		if verified_user is not None:
			if verified_user.is_active:
				login(request, verified_user)

				return render(request, 'user_success.html', {'notice': u'登陆成功！即将跳转...', 'next_url': next})
			else:
				pass
		else:
			return render(request, 'user_login.html', {'notice': u'请输入正确的用户名密码'})


def user_register(request):
	if request.method == 'GET':
		return render(request, 'user_register.html', {'notice': u'新用户注册'})
	if request.method == 'POST':
		user_name = request.POST.get('user_name')
		password = request.POST.get('password')
		email_addr = request.POST.get('inputEmail')
		real_name = request.POST.get('real_name')
		try:
			new_user = UserApiModel.objects.create_user(username=user_name,
			                                            password=password,
			                                            email=email_addr,
			                                            first_name=real_name)
			new_user.is_staff = True
			# new_user.save()
			new_user.generate_api_key()
			new_user.save()
			return render(request, 'user_success.html', {'notice': u'注册成功！即将跳转...', 'next_url': '/user/login/'})
		except Exception as e:
			if 'username is not unique' in e.message:
				return render(request, 'user_register.html', {'notice': u'注册失败:用户名已存在'})


@login_required
def user_logout(request):
	logout(request)
	return render(request,
	              'user_success.html',
	              {'notice': u'注销成功,即将跳转到主页...',
	               'next_url': '/hello/'})


class ProfileView(DetailView):
	template_name = "user_profile.html"
	model = UserApiModel
	content = {'firstTitle': u'查看用户详情',
	           'firstTitle_content': u''}

	@method_decorator(login_required)
	def get(self, request):
		user = request.user.username
		api_key_list = self.get_queryset()
		api_key = api_key_list.get(username=user).api_key_model
		self.content['api_key'] = api_key
		return render(request, self.template_name, self.content)

	@method_decorator(login_required)
	def post(self, request):
		user = request.user.username
		user_model = self.get_queryset().get(username=user)
		if user_model.update_api_key():
			self.content['firstTitle_content'] = u''
			self.content['api_key'] = user_model.api_key_model
			return render(request, self.template_name, self.content)
		else:
			self.content['firstTitle_content'] = u'error:更新失败，请检查网络连接'
			return render(request, self.template_name, self.content)
