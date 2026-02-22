# Books_web/my_profile/views.py
from django.http import JsonResponse
from users.models import user_info
from .models import BookCollection, SearchHistory
import json
from django.views.decorators.csrf import csrf_exempt

# 1. 功能一：获取个人信息（保持不变）
def get_user_info(request):
    username = request.GET.get('username')
    try:
        user = user_info.objects.get(user_name=username)
        return JsonResponse({
            "status": "success",
            "data": {
                "username": user.user_name,
                "register_time": user.id 
            }
        })
    except user_info.DoesNotExist:
        return JsonResponse({"status": "error", "msg": "用户不存在"}, status=404)

# 2. 功能二：获取浏览历史（保持时间格式化逻辑）
def get_search_history(request):
    username = request.GET.get('username')
    try:
        user = user_info.objects.get(user_name=username)
        history = SearchHistory.objects.filter(user=user).order_by('-id')[:20] 
        # 确保使用你数据库中的时间字段名（search_time）并格式化到秒
        data = [{"upc": h.browse_books, "time": h.search_time.strftime('%Y-%m-%d %H:%M:%S')} for h in history]
        return JsonResponse({"status": "success", "data": data})
    except Exception as e:
        return JsonResponse({"status": "error", "msg": str(e)}, status=500)

# 3. 功能三：获取图书收藏完整信息（用于“我的”页面展示）
def get_my_collections(request):
    username = request.GET.get('username')
    try:
        user = user_info.objects.get(user_name=username)
        collections = BookCollection.objects.filter(user=user)
        data = [{
            "upc": item.book_upc,
            "book_name": item.book_name,
            "time": item.collect_time.strftime('%Y-%m-%d %H:%M:%S') # 精确到秒
        } for item in collections]
        return JsonResponse({"status": "success", "data": data})
    except Exception as e:
        return JsonResponse({"status": "error", "msg": str(e)}, status=500)

# 新增辅助功能：仅获取收藏书籍的 UPC 列表（用于前端 Search/Recommend 页面比对）
def get_collection_upcs(request):
    username = request.GET.get('username')
    try:
        user = user_info.objects.get(user_name=username)
        # 仅提取 book_upc 字段并转为列表
        upcs = list(BookCollection.objects.filter(user=user).values_list('book_upc', flat=True))
        return JsonResponse({"status": "success", "upcs": upcs})
    except Exception:
        return JsonResponse({"status": "success", "upcs": []})

# 4. 核心功能：收藏切换逻辑
@csrf_exempt
def toggle_collection(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            upc = data.get('upc')
            book_name = data.get('book_name')

            # 查找用户
            user = user_info.objects.filter(user_name=username).first()
            if not user:
                return JsonResponse({"msg": "用户未登录"}, status=403)

            # 核心切换逻辑：判断是否存在
            collection_item = BookCollection.objects.filter(user=user, book_upc=upc)

            if collection_item.exists():
                collection_item.delete()
                return JsonResponse({
                    "status": "success", 
                    "is_collected": False, 
                    "msg": f"书名《{book_name}》已取消收藏！" 
                })
            else:
                # 修复占位符，正式写入数据
                BookCollection.objects.create(
                    user=user, 
                    book_upc=upc, 
                    book_name=book_name
                )
                return JsonResponse({
                    "status": "success", 
                    "is_collected": True, 
                    "msg": f"书名《{book_name}》已加入收藏清单！" 
                })

        except Exception as e:
            return JsonResponse({"status": "error", "msg": str(e)}, status=500)