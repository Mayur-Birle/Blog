from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.urls import reverse
from .models import Users, Posts
from django.utils import timezone;



def index(request):
	user = check_session(request.session);
	Post = Posts.objects.order_by('-published_date');
	context = {
		'User':user,
		'Post':Post,
		'Title': 'Blog Writer',
	}
	return render(request,'Home/home.html',{'User':user,'Post':Post})

# def reg_form(request):
# 	return render(request,'Form/signup.html',{});

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

class CreateNew(View):
	def get(self,request):
		if 'session_id' in request.session:
			user = check_session(request.session);
			return render(request,'Home/create_new.html',{'User':user});
		else:
			HttpResponseRedirect(reverse("Home"));
	def post(self,request):
		if 'session_id' in request.session:
			user = check_session(request.session);
			post = Posts();
			post.author = user;
			post.title = request.POST['title'];
			post.text = request.POST['content'];
			post.published_date = timezone.now();
			post.save();
			return HttpResponseRedirect(reverse('PublicBlog',kwargs={'author_id':user.id}));

		else:
			HttpResponseRedirect(reverse("Home"));


def logout(request):
    try:
        request.session.flush();
    except KeyError:
        return HttpResponse('Error Occur While Logging You Out, Please Try Again')
    return HttpResponseRedirect(reverse('Home'))

def public_blog_view(request,author_id):
	a = Users.objects.get(id=author_id);
	p = Posts.objects.filter(author = a);
	u = check_session(request.session);
	context = {'Author':a,'Post':p,'User':u};
	return render(request,'Home/user_post.html',context);

def single_blog_view(request,author_id,post_id):
	a = Users.objects.get(id=author_id);
	p = Posts.objects.get(id=post_id);
	u = check_session(request.session);
	context = {'Author':a,'Post':p,'User':u};
	return render(request,'Home/single_post.html',context);

#Some General Function	

def check_session(sessions):
	if 'session_id' in sessions:
		return Users.objects.get(id=sessions['session_id']);
	return False;

def is_mail_exist(mail):
	mail_list = Users.objects.values('user_email')
	for item in mail_list:
		if item['user_email'] == mail:
			return True;
	return False;