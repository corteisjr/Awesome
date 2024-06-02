from django.shortcuts import render, redirect
from .models import *
from .forms import *
from bs4 import BeautifulSoup
from django.contrib import messages
import requests

def home_view(request):
    posts = Post.objects.all()
    
    return render(request, 'a_posts/home.html', {'posts': posts})

def post_create_view(request):
    form = PostCreateForm()
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            website = requests.get(form.data['url'])
            source_code = BeautifulSoup(website.text, 'html.parser')
            
            find_image =source_code.select('meta[content^="https://live.staticflickr.com/"]')
            image = find_image[0]['content']
            post.image = image
            
            find_title = source_code.select('h1.photo-title')
            title  = find_title[0].text.strip()
            post.title = title
            
            find_artist = source_code.select('a.owner-name')
            artist = find_artist[0].text.strip()
            post.artist = artist

            post.save()
            return redirect('home')
    return render(request, 'a_posts/post_create.html', {'form': form})

def post_delete_view(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        post.delete()
        messages.warning(request, 'Post deleted')
        return redirect('home')
    return render(request, 'a_posts/post_delete.html', {'post':post})


def post_edit_view(request, pk):
    post = Post.objects.get(id=pk)
    form = PostEditForm(instance=post)
    
    if request.method == 'POST':
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated')
            return redirect('home')
    context = {
        'post': post,
        'form': form,
    }
    
    return render(request, 'a_posts/post_edit.html', context=context)