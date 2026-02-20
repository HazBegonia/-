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
import json
from django.views.decorators.cache import never_cache

@csrf_exempt
@never_cache
def get_captcha(request):
    try:
        ALL_CHARS = string.digits + string.ascii_letters
        captcha_text = ''.join(random.choices(ALL_CHARS, k = 4))
        request.session['captcha'] = captcha_text.lower()
        
        if not request.session.session_key:
            request.session.create()
        request.session.save()

        img = Image.new('RGB', (120, 40), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 30)
            draw.text((10, 3), captcha_text, fill=(0, 0, 0), font=font)
        except:
            draw.text((10, 10), captcha_text, fill=(0, 0, 0))
        
        buf = BytesIO()
        img.save(buf, 'png')
        return HttpResponse(buf.getvalue(), content_type='image/png')
    except Exception as e:
        return HttpResponse(status=500)

@csrf_exempt
def register_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            user_captcha = data.get('user_captcha', '').lower()
        except:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_captcha = request.POST.get('user_captcha', '').lower()

        print(f"用户输入: {user_captcha}, Session存的: {request.session.get('captcha')}")

        if user_captcha != request.session.get('captcha'):
            return JsonResponse({"msg": "验证码错误！"}, status = 400)
        
        if user_info.objects.filter(user_name = username).exists():
            return JsonResponse({"msg": "用户名已存在！"}, status = 400)
        
        user_info.objects.create(user_name=username, password=make_password(password))
        return JsonResponse({"msg": "注册成功！"})
    
@csrf_exempt
def login_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            user_captcha = data.get('user_captcha', '').lower()
        except Exception:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_captcha = request.POST.get('user_captcha', '').lower()

        session_captcha = request.session.get('captcha')
        print(f"比对详情 -> 用户输入: [{user_captcha}], Session存储: [{session_captcha}]")

        if not user_captcha or user_captcha != session_captcha:
            return JsonResponse({"msg": "验证码错误！"}, status=400)

        user = user_info.objects.filter(user_name=username).first()
        if user and check_password(password, user.password):
            request.session['user_id'] = user.id 
            request.session['user_name'] = username
            request.session['is_login'] = True
            request.session.modified = True
            request.session.save() 
            return JsonResponse({
                "msg": "登录成功", 
                "username": username,
                "user_id": user.id
            }, status=200)