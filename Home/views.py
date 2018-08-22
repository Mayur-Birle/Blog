from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.urls import reverse
from .models import Users
# from .form import SignUpForm

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

# Create your views here.
def index(request):
	if 'session_id' not in request.session:
		return render(request,'Home/index1.html',{});
	else:
		user_id = request.session['session_id'];
		user = Users.objects.get(id=user_id);
		return render(request,'Home/index2.html',{'User':user})

def reg_form(request):
	return render(request,'Form/signup.html',{});

class SignUp(View):
	def get(self,request):
		return render(request,'Form/signup.html',{});
	def post(self,request):
		if not is_mail_exist(request.POST['email']):
			u = Users();
			u.user_name = request.POST['name']
			u.user_email = request.POST['email']
			u.user_phone = request.POST['phone']
			u.user_pass = request.POST['pass']
			u.save()
			return HttpResponse('Data Saved :)')
		else:
			return HttpResponse('Enter Other Email :/')
		return HttpResponse('Nothing Run :(')

class LogIn(View):
	def get(self,request):
		return render(request,'Home/index.html',{});
	def post(self,request):
		if is_mail_exist(request.POST['email']):
			mail = request.POST['email'];
			user = Users.objects.get(user_email = mail);
			if(request.POST['pass'] == user.user_pass):
				request.session['session_id'] = user.id;
				return HttpResponseRedirect(reverse('Home'))
		return HttpResponse('You Enter Wrong Email or Password');

def logout(request):
    try:
        del request.session['session_id']
    except KeyError:
        pass
    return HttpResponseRedirect(reverse('Home'))

def is_mail_exist(mail):
	mail_list = Users.objects.values('user_email')
	for item in mail_list:
		if item['user_email'] == mail:
			return True;
	return False;