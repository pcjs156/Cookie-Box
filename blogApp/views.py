from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# 카테고리별 크리에이터 목록
def category_view(request, category_id):
    return render(request, 'category.html')


# 해당 카테고리의 공개 웹진 전체 목록
def message_to_creator_view(request, creator_id):
    return render(request, 'message_to_creator.html')


# 웹진수정
@login_required(login_url='/account/logIn/')
def webzine_create_view(request):
    return render(request, 'webzine_create.html')


# 웹진 작성
@login_required(login_url='/account/logIn/')
def webzine_detail_view(request, webzine_id):
    return render(request, 'webzine_detail.html')


# 웹진 디테일 페이지
def webzine_edit_view(request, webzine_id):
    return render(request, 'webzine_edit.html')


# 유저별 작성 웹진 목록
def webzine_list_by_category_view(request, category_id):
    return render(request, 'webzine_list_by_category.html')


# 크리에이터에게 쪽지를 보내는 기능
@login_required(login_url='/account/logIn/')
def webzine_user_list_view(request, creator_id):
    return render(request, 'webzine_user_list.html')