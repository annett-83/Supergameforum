from django.contrib.auth.decorators import permission_required
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.views.generic import ListView
from django.views import View
from .forms import *
from .models import Category, Post, Answer,MediaAttachment
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
import uuid
import pathlib
from django.conf import settings

EMAIL_LINK_DOMAIN = 'http://127.0.0.1:8000'



class CategoryList(ListView): # Die Übersichstsseite mit den Artikeln
    model = Category # Referenz auf das Modell
    template_name = 'flatpages/game_board.html' # Angabe des Template
    paginate_by = 1
    context_object_name = 'categories'


class user_content_view(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.UserValidation.isValidated:
                user = request.user
                posts = Post.objects.filter(user=user)
                form= user_subscription_form({'user':user,'category':Category})
                return render(request, 'flatpages/user_content_page.html', {
                    'user': user,
                    'posts': posts,
                    'form': form,
                })
            else:
                return HttpResponseRedirect(reverse('checkvalidationcode'))
        else:
            return HttpResponseRedirect(reverse('login'))

    def post(self, request, *args, **kwargs):
        request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
        if request.user.is_authenticated:
            if request.user.UserValidation.isValidated:
                user = request.user
                sub_req=[]
                for entry in request.POST:
                    if entry.startswith('category_'):
                        sub_req.append(int(str(entry[9:])))
                for e in SubUser.objects.filter(sub_user=user):
                    if e.category_id in sub_req:
                        sub_req.remove(e.category_id)
                    else:
                        e.delete()
                for cat_id in sub_req:
                    su=SubUser(category_id=cat_id, sub_user=user)
                    su.save()
        return HttpResponseRedirect(request.session['login_from'])


def handle_uploaded_file(f):
    suffix=pathlib.Path(f.name).suffix
    new_name=str(uuid.uuid4())
    save_name=new_name + suffix
    with open("media/" + save_name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return save_name

class post_edit_view(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.UserValidation.isValidated:
                request.session['login_from'] = request.META.get('HTTP_REFERER', '/')  # schicke mich zuruck
                action=kwargs['action']
                if action=='new':
                    category = Category.objects.get(id=kwargs['pk'])
                    form = NewPostForm()
                else:
                    post = Post.objects.get(id=kwargs['pk'])
                    category=post.category
                    form = NewPostForm({'title':post.title,'text':post.text})

                if action == "delete":
                    post.delete()
                    return HttpResponseRedirect(request.session['login_from'])
                else:
                    return render(request, 'flatpages/post_edit_page.html', {
                            'form': form, # Übergabe der form als Parameter. Das ganze Prinzip müssen wir uns noch mal anschauen
                            'category': category,  # Übergabe der form als Parameter. Das ganze Prinzip müssen wir uns noch mal anschauen
                            'action': action,

                    })
            else:
                return HttpResponseRedirect(reverse('checkvalidationcode'))
        else:
            return HttpResponseRedirect(reverse('login'))

    def post(self, request, *args, **kwargs):
        action = kwargs['action']
        if action=="new":
            category=Category.objects.get(id=kwargs['pk'])
            post = Post()
            post.user = request.user
            post.category = category
        else:
            post = Post.objects.get(id=kwargs['pk'])

        post.title = request.POST['title']
        post.text =  request.POST['text']

        post.save()
        files = request.FILES.getlist('file_field')
        for f in files:
            name=handle_uploaded_file(f)
            ma=MediaAttachment()
            ma.post=post
            ma.fileName=name
            ma.fileType=f.content_type
            ma.save()

        return HttpResponseRedirect(request.session['login_from'])

class answer_edit_view(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.UserValidation.isValidated:
                request.session['login_from'] = request.META.get('HTTP_REFERER', '/') # 1=2 1:2 Vorherige seite und 1 Zwischenspeicher
                action=kwargs['action']
                if action=='new':
                    post=Post.objects.get(id=kwargs['pk'])
                    form = NewAnswerForm()
                else:
                    answer=Answer.objects.get(id=kwargs['pk'])
                    post=answer.post

                    form = NewAnswerForm({'text':answer.text})

                if action == 'accept' or action == 'delete' :
                    if action == 'accept':
                        answer.isAccepted=True
                        answer.save()
                    else:
                        answer.delete()
                    return HttpResponseRedirect(request.session['login_from']) # geht da hin wo er gewese ist
                else:

                    return render(request, 'flatpages/answer_edit_page.html', {
                        'form': form,
                        'post': post,
                        'action': action,
                    })
            else:
                return HttpResponseRedirect(reverse('checkvalidationcode'))
        else:
            return HttpResponseRedirect(reverse('login'))

    def post(self, request, *args, **kwargs):
        action=kwargs['action']
        if action=='new':
            post=Post.objects.get(id=kwargs['pk'])
            answer = Answer()
            answer.post = post
            answer.user = request.user
            if answer.user == post.user:
                answer.isAccepted=True
        else:
            answer=Answer.objects.get(id=kwargs['pk'])

        answer.text = request.POST['text']
        answer.save()

        return HttpResponseRedirect(request.session['login_from'])




