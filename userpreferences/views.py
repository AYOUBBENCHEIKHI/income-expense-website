from django.shortcuts import render, redirect
import os
import json
from django.conf import settings
from .models import UserPreference
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url='/authentication/login')
def index(request):
    #if request.user.is_authenticated:
        currency_data =[]
        # Read and parse the currencies.json file to get the currency data.
            
        file_path = os.path.join(settings.BASE_DIR, 'currencies.json')

        with open(file_path,'r') as json_file:
                data = json.load(json_file)
                for k,v in data.items():
                    currency_data.append({
                        'name': k,
                        'value': v
                    })
        exists = UserPreference.objects.filter(user = request.user).exists()
        user_preference = None
        if exists:
            user_preference = UserPreference.objects.get(user = request.user)


        if request.method =='GET':
            #import pdb # pdb pour fair un pause de programe
            #pdb.set_trace() # pdb pour fair un pause de programe

            return render(request, 'preferences/index.html',{'currencies':currency_data, 'user_preference':user_preference})
        else:
            currency = request.POST['currency']
            if exists:
                user_preference.currency = currency
                user_preference.save()
            else:
                UserPreference.objects.create(user = request.user, currency = currency)
            messages.success(request,'Changes saved')
            return render(request, 'preferences/index.html',{'currencies': currency_data,'user_preference':user_preference})
    # Rediriger vers la page de connexion si l'utilisateur n'est pas authentifié
   # return redirect('login')