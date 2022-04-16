from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.views import View
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .forms import *
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .models import UserValidation

class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/sign/login'

class CheckValidationCodeView(View):
    def get(self, request, *args, **kwargs):
        form=ValidationForm()
        return render(request, 'flatpages/check_validation_code.html', {
                      'form': form # Übergabe der form als Parameter. Das ganze Prinzip müssen wir uns noch mal anschauen
                  })
    def post(self, request, *args, **kwargs):
        enteredCode=request.POST['validationCode']
        uv= UserValidation.objects.filter(user=request.user)
        if uv.exists():
            uvo=uv[0]
            print(uvo.validationCode)
            print(enteredCode)
            if uvo.validationCode.strip()==enteredCode.strip():
                print("match")
                if not uvo.isValidated:
                    uvo.isValidated=True
                    uvo.save()
                    print("Saved")

        return redirect('/category/')

# Create your views here.
