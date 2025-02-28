from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from validate_email import  validate_email
from django.contrib import messages
# Create your views here.

class EmailValidationView(View):
    def post(self,request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error':'Email is invalid'},status=400)
        if User.objects.filter(email=email).exists() :
            return JsonResponse({'email_error':'sorry email is use ,choose another one'},status=409)
        
        return JsonResponse({'email_valid':True})


@method_decorator(csrf_exempt, name='dispatch')
class UsernameValidationView(View):
    def post(self,request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error':'username should only contain alphabetic characters'},status=400)
        if User.objects.filter(username=username).exists() :
            return JsonResponse({'username_error':'sorry username is use ,choose another one'},status=409)
        
        return JsonResponse({'username_valid':True})

        

class RegistrationView(View):
    def get(self,request):
        return render(request, 'authentication/register.html')
    def post(self,request):
        #GET USER DATA
        #VALIDATE
        #create a user account
        username = request.POST['username']
        email= request.POST['email']
        password = request.POST['password']
        context = {
            'fieldsValues':request.POST
        }
        if not User.objects.filter(email=email).exists() :
            if len(password) < 6 :
                messages.error(request,'Password must be at least 6 characters long')
                return render(request, 'authentication/register.html',context)
            user = User.objects.create(username=username, email=email)
            user.set_password(password)
            user.save()
            messages.success(request,'Account successfuly created')
            

        return render(request, 'authentication/register.html')


"""

        messages.success(request,'successfully registered sucess')
        messages.warning(request,'successfully registered warning')
        messages.info(request,'successfully registered info')
        messages.error(request,'successfully registered erro')"""