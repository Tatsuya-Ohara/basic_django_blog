from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogModel, Comment
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.db.models import Q

from .forms import PostSearchForm, CommentCreateForm


def paginate_queryset(request, queryset, count):
    """ページネーション"""
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
    """index.htmlのデータ用"""
    post_list = BlogModel.objects.order_by('-post_datetime')

    # ユーザーが送信したGETパラメーターを取得、フォームクラスに渡してインスタンス化
    form = PostSearchForm(request.GET)
    # 入力内容のチェック処理: ちゃんと入力があったか？確認
    if form.is_valid():
        # 入力されたキーワードの取得: cleaned_dataはform.is_validが必要。
        # formを扱う際には必ずform.is_validを呼ぶ。
        keyword = form.cleaned_data['keyword']
        # ModelChoiceFieldを使うとリストではなくstrで返ってくる。→[tags]のように角かっこが必要
        # ModelMultipleChoiceFieldだとリスト形式で返ってくる。
        tags = form.cleaned_data['tags']
        category = form.cleaned_data['category']

        if keyword:
            # テキスト用のQオブジェクトを追加
            post_list = post_list.filter(
                Q(title__icontains=keyword) | Q(body__icontains=keyword)
            )
        if category:
            post_list = post_list.filter(Q(category__name__icontains=category))
            # ModelChoiceFieldに変更したことにより、Qを外す。
            post_list = post_list.filter(category=category)

        if tags:
            # ModelMultipleChoiceFieldの場合は[]は不要。→Webページから送信されたidのリストをもとに、モデルのインスタンスリストを生成してくれているため。
            # ModelChoiceFieldの場合はリスト化はしてくれない？ため、[tags]のようにする。
            post_list = post_list.filter(tag__in=tags)
            # for tag in tags:
            #     # 全てを含む
            #     post_list = post_list.filter(tag=tag)

        messages.success(request, '「{}」の検索結果'.format(keyword))

        page_obj = paginate_queryset(request, post_list, 10)
        context = {
            'post_list': post_list,
            'page_obj': page_obj,
            'form': form,
            'keyword': keyword,
            'tags': tags,
            'category': category,
            'messages': messages,
            }
        return render(request, 'blog/index.html', context)

    page_obj = paginate_queryset(request, post_list, 10)
    context = {
        'post_list': post_list,
        'page_obj': page_obj,
        'form': form,
        'keyword': "",
        'tags': "",
        'category': "",
        'messages': messages,
    }

    # # 検索機能の処理
    # keyword = request.GET.get('keyword')
    # if keyword:
    #     # テキスト用のQオブジェクトを追加
    #     post_list = post_list.filter(
    #         (Q(title__icontains=keyword) | Q(body__icontains=keyword))
    #     )
    #     messages.success(request, '「{}」の検索結果'.format(keyword))

    # page_obj = paginate_queryset(request, post_list, 10)
    # # page_obj = paginate_queryset(request, post_list, 1)
    # context = {
    #     'post_list': post_list,
    #     'page_obj': page_obj,
    # }

    return render(request, 'blog/index.html', context)


def detail(request, pk):
    content = get_object_or_404(BlogModel, pk=pk)
    # comments = Comment.objects.get(pk=pk)
    comments = Comment.objects.filter(target=pk)
    # print(comments)
    # print('コメントの件数', comments)
    relation_post = BlogModel.objects.filter(relation_posts=pk)

    # 送信データがあればフォームに紐付けられる / なければからのフォームになる
    form = CommentCreateForm(request.POST or None)
    # 送信データがあれば入力チェックを行う / なければからのフォームを表示する
    if form.is_valid():
        # 記事とコメントを紐づける前の処理(saveメソッドを呼び出す) → 公式で推奨された方法。
        # form.instance.target = ...ともできるが、公式のやり方ではない。
        comment = form.save(commit=False)
        # 記事と紐付けをする
        comment.target = content
        # フォームの内容をもとにコメントを作成
        comment.save()
        # 保存/更新/削除後はリダイレクトが必要
        return redirect('index')

    context = {
        'contents': content,
        'form': form,
        'comments': comments,
        'relation_post': relation_post,
    }
    # # 少し長い表現
    # try:
    #     content = BlogModel.objects.get(pk=pk)
    # except BlogModel.DoesNotExist:
    #     raise Http404('記事が見つかりません。')
    return render(request, 'blog/detail.html', context)
    # return render(request, 'blog/detail.html', {'context': context})
    # see: https://zerofromlight.com/blogs/detail/59/
