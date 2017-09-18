# -*- coding: utf-8 -*-

from django.shortcuts import render
from forms import FeedBackForm

# Create your views here.


def write_contact(request):
	if request.method =='GET':
		firstTitle = u'留下你的建议'
		firstTitle_content = u'可以报告BUG，提出需求和改进点。:D'
		return render(request, 'feedback_contact.html', {'firstTitle': firstTitle, 'firstTitle_content': firstTitle_content})

	if request.method == 'POST':
		feedback_form = FeedBackForm(request.POST)
		if feedback_form.is_valid():
			feedback_form.save()
			firstTitle = u'提交成功'
			firstTitle_content = u'即将跳转至主页...'
			return render(request, 'feedback_success.html', {'firstTitle': firstTitle, 'firstTitle_content': firstTitle_content,
			                                       'next_url':'/'})
		else:
			firstTitle = u'留下你的建议'
			k=feedback_form.errors
			d=k.get('user_email',"")
			firstTitle_content = u'可以报告BUG，提出需求和改进点。:D'
			return render(request, 'feedback_contact.html', {'firstTitle': firstTitle, 'firstTitle_content': firstTitle_content,
			                                         'next_url': '/', 'fb_form': feedback_form})