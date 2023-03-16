from .models import Comment


def common(request):
    context = {
        'comment_list': Comment.objects.order_by("-created_at")[:5]
    }
    return context
