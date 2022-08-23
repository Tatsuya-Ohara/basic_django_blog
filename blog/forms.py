from django import forms
from .models import Tag


class PostSearchForm(forms.Form):
    '''記事検索フォーム'''
    # キーワード入力用フォーム
    keyword = forms.CharField(
		label='検索キーワード',
		# 空欄でも問題ないようにする
  		required=False,
	)
    
    # タグ絞り込み用フォーム
    tags = forms.ModelMultipleChoiceField(
		label='タグでの絞り込み',
		# 空欄でも問題ないようにする
		required=False,
		queryset=Tag.objects.order_by('name'),
	)