# -*- coding: utf-8 -*-

from django.shortcuts import render
from forms import FeedBackForm


# Create your views here.


def write_contact(request):
    if request.method == 'GET':
        firstTitle = u'留下你的建议'
        firstTitle_content = u'可以报告BUG，提出需求和改进点。:D'
        return render(request, 'feedback_contact.html',
                      {'firstTitle': firstTitle, 'firstTitle_content': firstTitle_content})

    if request.method == 'POST':
        feedback_form = FeedBackForm(request.POST)
        if feedback_form.is_valid():
            feedback_form.save()
            firstTitle = u'提交成功'
            firstTitle_content = u'即将跳转至主页...'
            return render(request, 'feedback_success.html',
                          {'firstTitle': firstTitle, 'firstTitle_content': firstTitle_content,
                           'next_url': '/'})
        else:
            firstTitle = u'留下你的建议'
            reply_dict = {}
            error_dict = feedback_form.errors
            reply_dict['feedback_content'] = feedback_form.cleaned_data.get("feedback_content",
                                                                    error_dict.get("feedback_content", [""])[0])
            reply_dict['user_email'] = feedback_form.cleaned_data.get("user_email", error_dict.get("user_email", [""])[0])
            reply_dict['errors'] = 1 if len(error_dict) > 0 else 0
            firstTitle_content = u'可以报告BUG，提出需求和改进点。:D'
            return render(request, 'feedback_contact.html',
                          {'firstTitle': firstTitle, 'firstTitle_content': firstTitle_content,
                           'next_url': '/', 'reply_dict': reply_dict})
