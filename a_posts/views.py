from django.shortcuts import render, redirect
from .models import *
from .forms import *
from bs4 import BeautifulSoup
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
        return redirect('home')
    return render(request, 'a_posts/post_delete.html', {'post':post})