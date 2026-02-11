from django.shortcuts import render

# Create your views here.
import random
from PIL import Image, ImageDraw, ImageFont
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from io import BytesIO
import string
from .models import user_info
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def get_captcha(request):
    try:
        ALL_CHARS = string.digits + string.ascii_letters
        captcha_text = ''.join(random.choices(ALL_CHARS, k = 4))
        request.session['captcha'] = captcha_text.lower()
        
        img = Image.new('RGB', (120, 40), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", 30)
        draw.text((10, 3), captcha_text, fill = (0, 0, 0), font = font)
        
        buf = BytesIO()
        img.save(buf, 'png')
        return HttpResponse(buf.getvalue(), content_type = 'image/png')
    except Exception as e:
        print(f"验证码生成失败: {e}")
        return HttpResponse(status=500)

@csrf_exempt
def register_api(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_captcha = request.POST.get('user_captcha', '').lower()
        print(user_captcha, request.session.get('captcha'))

        if user_info.objects.filter(user_name = username).exists():
            return JsonResponse({"msg": "用户名已存在！"}, status = 400)
        
        if user_captcha != request.session.get('captcha'):
            return JsonResponse({"msg": "验证码错误！"}, status = 400)
        
        hashed_password = make_password(password)

        user_info.objects.create(
            user_name = username,
            password = hashed_password
        )
        return JsonResponse({"msg": "注册成功！"})
    
@csrf_exempt
def login_api(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = user_info.objects.filter(user_name = username).first()

    if user and check_password(password, user.password):
        request.session['user_name'] = username
        return JsonResponse({"msg": "登录成功"})
    else:
        return JsonResponse({"msg": "账号或密码错误"}, status = 401)