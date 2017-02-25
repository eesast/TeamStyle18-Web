# -*-  coding:utf-8 -*-
from django.shortcuts import render, render_to_response,HttpResponseRedirect
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login
from .models import Post, PostFile, Comment
from .forms import PostForm,CommentForm

Category_List=(
		('1','赛事公告'),
		('2','技术讨论'),
		('3','bug汇报'),
		)

def forum_content(request,id):
	try:
		post = Post.objects.get(id=int(id))
	except:
		HttpResponseRedirect('/forum_index')
	delete_id = request.POST.get('delete_id','')
	try:
		delcomment = Comment.objects.get(id=int(delete_id))
		delcomment.post.save()
		delcomment.delete()
	except Exception:
		pass
	if 	request.user.is_authenticated() :
		if request.method=='POST':
			form = CommentForm(request.POST)
			if form.is_valid():
				cd = form.cleaned_data
				comment = Comment(content=cd['comment'],post = Post.objects.get(id=int(id)),replier=request.user)
				comment.save()
				comment.post.save()
			else:
				form = CommentForm()
		commentlist = post.p_comment.all()
		print(1)
		return render(request,'forum_content.html',{'post':post,'commentlist':commentlist})
	else:
		commentlist = post.p_comment.all()
		return render(request,'forum_content.html',{'post':post,'commentlist':commentlist})



def forum_create(request):
	if not request.user.is_authenticated():
		forum_index(request)
	if request.method == 'POST':
		form = PostForm(request.POST)
		print(form.errors)
		if form.is_valid():
			cd = form.cleaned_data
			post = Post(title=cd['title'],content=cd['body'],sender=request.user,category=cd['category'])
			post.save()
			return HttpResponseRedirect('/forum_index')
	else:
		form = PostForm()
	return render(request,'forum_create.html', {'form': form})





def forum_index(request,page=1):
	post_list = Post.objects.order_by('priority','-timestamp')
	paginator = Paginator(post_list,5)
	delete_id = None
	delete_id = request.POST.get('delete_id','')
	if request.user.is_authenticated():
		print(1)
	try:
		post = Post.objects.get(id=int(delete_id))
		post.delete()
	except Exception:
		pass
	try:
		page = int (request.GET.get('page','1'))
	except ValueError:
		page = 1
	try:
		posts = paginator.page(page)
	except (EmptyPage,InvalidPage):
		posts = paginator.page(paginator.num_pages)
	for i in range(page,page+3):
		if i > paginator.num_pages:
			break
		maxpage = i
	for i in range(page,page-3,-1):
		if i < 1:
			break
		minpage = i
	pagerange=range(minpage,maxpage+1)
	if request.user.is_authenticated():
		return render(request,'forum_index.html',{"posts":posts,"pagerange":pagerange,})
	else:
		return render(request,'forum_index.html',{"posts":posts,"pagerange":pagerange,})

def forum_index_tongzhi(request,page=1):
	post_list = Post.objects.filter(category='1')
	paginator = Paginator(post_list,5)
	delete_id = None
	delete_id = request.POST.get('delete_id','')
	try:
		post = Post.objects.get(id=int(delete_id))
		post.delete()
	except Exception:
		pass
	try:
		page = int (request.GET.get('page','1'))
	except ValueError:
		page = 1
	try:
		posts = paginator.page(page)
	except (EmptyPage,InvalidPage):
		posts = paginator.page(paginator.num_pages)
	for i in range(page,page+3):
		if i > paginator.num_pages:
			break
		maxpage = i
	for i in range(page,page-3,-1):
		if i < 1:
			break
		minpage = i
	pagerange=range(minpage,maxpage+1)
	if request.user.is_authenticated():
		return render(request,'forum_index.html',{"posts":posts,"pagerange":pagerange,})
	else:
		return render(request,'forum_index.html',{"posts":posts,"pagerange":pagerange,})

def forum_index_jishu(request,page=1):
	post_list = Post.objects.filter(category='2')
	paginator = Paginator(post_list,5)
	delete_id = None
	delete_id = request.POST.get('delete_id','')
	try:
		post = Post.objects.get(id=int(delete_id))
		post.delete()
	except Exception:
		pass
	try:
		page = int (request.GET.get('page','1'))
	except ValueError:
		page = 1
	try:
		posts = paginator.page(page)
	except (EmptyPage,InvalidPage):
		posts = paginator.page(paginator.num_pages)
	for i in range(page,page+3):
		if i > paginator.num_pages:
			break
		maxpage = i
	for i in range(page,page-3,-1):
		if i < 1:
			break
		minpage = i
	pagerange=range(minpage,maxpage+1)
	if request.user.is_authenticated():
		return render(request,'forum_index.html',{"posts":posts,"pagerange":pagerange,})
	else:
		return render(request,'forum_index.html',{"posts":posts,"pagerange":pagerange,})

def forum_index_bug(request,page=1):
	post_list = Post.objects.filter(category='3')
	paginator = Paginator(post_list,5)
	delete_id = request.POST.get('delete_id','')
	try:
		post = Post.objects.get(id=int(delete_id))
		post.delete()
	except Exception:
		pass
	try:
		page = int (request.GET.get('page','1'))
	except ValueError:
		page = 1
	try:
		posts = paginator.page(page)
	except (EmptyPage,InvalidPage):
		posts = paginator.page(paginator.num_pages)
	for i in range(page,page+3):
		if i > paginator.num_pages:
			break
		maxpage = i
	for i in range(page,page-3,-1):
		if i < 1:
			break
		minpage = i
	pagerange=range(minpage,maxpage+1)
	if request.user.is_authenticated():
		return render(request,'forum_index.html',{"posts":posts,"pagerange":pagerange,})
	else:
		return render(request,'forum_index.html',{"posts":posts,"pagerange":pagerange,})

def forum_index_mypost(request,page=1):
	if request.user.is_authenticated:
		post_list = Post.objects.filter(sender=request.user)
		paginator = Paginator(post_list,5)
		delete_id = None
		delete_id = request.POST.get('delete_id','')
		try:
			post = Post.objects.get(id=int(delete_id))
			post.delete()
		except Exception:
			pass
		try:
			page = int (request.GET.get('page','1'))
		except ValueError:
			page = 1
		try:
			posts = paginator.page(page)
		except (EmptyPage,InvalidPage):
			posts = paginator.page(paginator.num_pages)
		for i in range(page,page+3):
			if i > paginator.num_pages:
				break
			maxpage = i
		for i in range(page,page-3,-1):
			if i < 1:
				break
			minpage = i
		pagerange=range(minpage,maxpage+1)
		return render(request,'forum_index.html',{"posts":posts,"pagerange":pagerange,})
	else:
		pagerange=range(1,2)
		return render(request,'forum_index.html',{"pagerange":pagerange,})




# Create your views here.
# Create your views here.
