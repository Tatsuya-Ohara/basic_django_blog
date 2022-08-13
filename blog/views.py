from django.shortcuts import render
from .models import BlogModel
def index(request):
    posts = BlogModel.objects.order_by('-post_datetime')
    
    return render(request, 'blog/index.html', {'posts': posts})

def detail(request, pk):
    contents = BlogModel.objects.filter(pk=pk)
    return render(request, 'blog/detail.html', {'contents': contents})