from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.views import View
from django.urls import reverse
from .models import Users, Posts, Votes
from django.utils import timezone;


# index function to load default home page
def index(request):
	user = check_session(request.session);
	Post = Posts.objects.order_by('-published_date');
	context = {
		'User':user,
		'Post':Post,
		'Title': 'Blog Writer',
		'List':get_liked_post(user),
	}
	print(context['List'])
	return render(request,'Home/home.html',context)

# SignUp get method loades the default signup page
# SignUp post method save the data coming from signup post request 
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
			if u.check_validation():
				u.save();
				request.session['session_id'] = u.id;
				return HttpResponseRedirect(reverse('Home'));
			return HttpResponse('<h2>Please Fill Form Correctly</h2>');
		else:
			return HttpResponse('Enter Other Email :/')
		return HttpResponse('Something Wrong is Happen :(');

# LogIn post method save the data coming from login post request
class LogIn(View):
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
		user = check_session(request.session);
		if user == False:
			return HttpResponseRedirect(reverse("Home"));
		else:
			return render(request,'Home/create_new.html',{'User':user});
	def post(self,request):
		if 'session_id' in request.session:
			user = check_session(request.session);
			post = Posts();
			post.title = request.POST['title'];
			post.text = request.POST['content'];
			if post.check_validation():
				post.author = user;
				post.published_date = timezone.now();
				post.save();
				return HttpResponseRedirect(reverse('PublicBlog',kwargs={'author_id':user.id}));
			else:
				return HttpResponseRedirect(reverse('CreateNew'));
		else:
			HttpResponseRedirect(reverse("Home"));

class UpdateBlog(View):
	def get(self,request,author_id,post_id):
		u = check_session(request.session);
		if u and u.id == author_id:
			p = Posts.objects.get(id=post_id);
			context = {'Author':u,'Post':p,'User':u};
			return render(request,'Home/manage2.html',context);
		else:
			return HttpResponse('Why are you here? :/ ');

	def post(self,request,author_id,post_id):
		u = check_session(request.session);
		if u and u.id == author_id:
			p = Posts.objects.get(id=post_id);
			p.title = request.POST['title'];
			p.text = request.POST['content'];
			p.save();
			context = {'Author':u,'Post':p,'User':u};
			return HttpResponseRedirect(reverse('PublicBlog',kwargs={'author_id':u.id}));
		else:
			return HttpResponse('Hmm... Seriously Something is Wrong !');
			


def manage(request):
	u = check_session(request.session);
	if u:
		p = Posts.objects.filter(author = u);
		context = {'Author':u,'Post':p,'User':u,'Title':p};
		return render(request,'Home/manage1.html',context);
	else:
		return HttpResponseRedirect(reverse('Home'))

def delete_blog(request,author_id,post_id):
	if request.method == 'GET':
		u = check_session(request.session);
		confirm = True;
		if u and u.id == author_id and confirm:
			Posts.objects.get(id=post_id).delete();
	return HttpResponseRedirect(reverse('Manage'));

def like(request):
	u = check_session(request.session);
	if u:
		post_id = request.POST['post_id'];
		post = Posts.objects.get(id = post_id)
		get_vote = Votes.objects.get_or_create(post_id=post,user_id=u)
		get_vote[0].toggle_vote();
		get_vote[0].save();
		return JsonResponse({'count_like':post.count_like()})
	else:
		return JsonResponse({'var':1})


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
	context = {'Author':a,'Post':p,'User':u,'Title':p,'List':get_liked_post(u),};
	return render(request,'Home/user_post.html',context);

def single_blog_view(request,author_id,post_id):
	a = Users.objects.get(id=author_id);
	p = Posts.objects.get(id=post_id);
	u = check_session(request.session);
	context = {'Author':a,'Post':p,'User':u,};
	return render(request,'Home/single_post.html',context);

def public_liked_view(request,author_id):
	a = Users.objects.get(id=author_id);
	p = Posts.objects.filter(votes__in=Votes.objects.filter(user_id=a,vote=True));
	u = check_session(request.session);
	context = {'Author':a,'Post':p,'User':u,'Title':p,'List':get_liked_post(u),};
	return render(request,'Home/liked_post.html',context);


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

def get_liked_post(user_id):
	if user_id:
		votes = Votes.objects.filter(user_id=user_id.id,vote=True);
		liked_list = []
		for v in votes:
			liked_list.append(v.post_id.id);
		return liked_list;