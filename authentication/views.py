from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from validate_email import  validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import token_generator





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
            user.is_active = False
            user.save()
            # send email verification link
            # - geting domain we are on
            # - relative url to verification
            #- encode uid
            # - token
            uidb64 =urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            link = reverse('activate',kwargs={'uidb64':uidb64,'token':token_generator.make_token(user)})
            activate_url = 'http://'+domain+link
            email_subject = 'Activate your account'
            email_body = 'Hi '+user.username+' please use this link to verify your account\n'+activate_url
            email = EmailMessage(
                email_subject,
                email_body,
                "noreply@income-expenses.com",
                [email]
            )
            email.send(fail_silently=False)
            messages.success(request,'Account successfuly created')
            

        return render(request, 'authentication/register.html')
class VerificationView(View):
    def get(self,request,uidb64,token):
        return redirect('login')


"""

        messages.success(request,'successfully registered sucess')
        messages.warning(request,'successfully registered warning')
        messages.info(request,'successfully registered info')
        messages.error(request,'successfully registered erro')"""