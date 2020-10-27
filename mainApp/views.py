from django.shortcuts import render

# 아래 test/EXAMPLE_view는 개발용 코드입니다. ==================


# url은 'http://localhost:8000/test' 입니다.
def test_view(request):
    return render(request, 'test.html')


# url은 'http://localholst:8000/ex' 입니다.
def EXAMPLE_view(request):
    return render(request, 'EXAMPLE.html')


# 해당 라인 아래부터 구현을 시작해주세요! =======================


# 메인 페이지
def main_view(request):
    return render(request, 'main.html')


# 인트로페이지
def intro_view(request):
    return render(request, 'intro.html')