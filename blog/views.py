from django.shortcuts import render, get_object_or_404
from .models import BlogModel
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404

def paginate_queryset(request, queryset, count):
    paginator = Paginator(queryset, count)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj

def index(request):
    post_list = BlogModel.objects.order_by('-post_datetime')
    page_obj = paginate_queryset(request, post_list, 10)
    # page_obj = paginate_queryset(request, post_list, 1)
    context = {
        'post_list': post_list,
        'page_obj': page_obj,
    }
    
    return render(request, 'blog/index.html', context)

def detail(request, pk):
    content = get_object_or_404(BlogModel, pk=pk)
    # # 少し長い表現
    # try:
    #     content = BlogModel.objects.get(pk=pk)
    # except BlogModel.DoesNotExist:
    #     raise Http404('記事が見つかりません。')
        
    return render(request, 'blog/detail.html', {'content': content})