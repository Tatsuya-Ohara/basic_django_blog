from django import forms
from .models import Tag, Category


class PostSearchForm(forms.Form):
    '''記事検索フォーム'''
    # キーワード入力用フォーム
    keyword = forms.CharField(
		label='検索キーワード',
		# 空欄でも問題ないようにする: Trueにすると空欄を許さない
  		required=False,
	)
    
    # タグ絞り込み用フォーム
    tags = forms.ModelMultipleChoiceField(
    # tags = forms.ModelChoiceField(
		label='タグでの絞り込み',
		# 空欄でも問題ないようにする
		required=False,
		queryset=Tag.objects.order_by('name'),
	)
    
    # カテゴリー絞り込み用フォーム / ForeignKeyの場合に"ModelChoiceField"を使うことが多い
    category = forms.ModelChoiceField(
        label='カテゴリで絞り込み',
        required=False,
        queryset=Category.objects.order_by('name'),
	)
    # category = forms.CharField(
	# 	label='カテゴリーでの絞り込み',
	# 	# 空欄でも問題ないようにする
	# 	required=False,
	# )