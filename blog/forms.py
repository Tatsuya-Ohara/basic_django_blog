from django import forms
from .models import Tag, Category, Comment


class PostSearchForm(forms.Form):
    '''記事検索フォーム'''
    # キーワード入力用フォーム
    keyword = forms.CharField(
        label='検索キーワード',
        required=False,  # 空欄OK, Trueで空欄許さない
        )

    # タグ絞り込み用フォーム
    # tags = forms.ModelChoiceField(
    tags = forms.ModelMultipleChoiceField(
        label='タグでの絞り込み',
        required=False,  # 空欄でもOK
        queryset=Tag.objects.order_by('name'),
        )

    # カテゴリー絞り込み用フォーム / ForeignKeyの場合に"ModelChoiceField"を使うことが多い
    category = forms.ModelChoiceField(
        label='カテゴリで絞り込み',
        required=False,
        queryset=Category.objects.order_by('name'),
        )

    category = forms.CharField(
        label='カテゴリーでの絞り込み',
        required=False,  # 空欄でもOK
        )


class CommentCreateForm(forms.ModelForm):
    """コメント投稿フォーム"""
    class Meta:
        model = Comment
        exclude = ('target', 'created_at')
