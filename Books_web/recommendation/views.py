# recommendation/views.py
from django.http import JsonResponse
from .recommender import BookRecommender
from users.models import user_info
from search.models import Book  # 必须导入 Book 模型
from django.views.decorators.http import require_GET

@require_GET
def get_recommendations(request):
    username = request.GET.get('username')
    if not username:
        return JsonResponse({'error': 'Username required', 'data': []}, status=400)

    try:
        user = user_info.objects.get(user_name=username)
    except user_info.DoesNotExist:
        return JsonResponse({'error': 'User not found', 'data': []}, status=404)

    # 1. 获取算法推荐的前 10 本书
    recommender = BookRecommender(user)
    recommended_books = list(recommender.train_and_predict()) 
    
    # 2. 提取这 10 本书的 ID，用于后续排除
    recommended_ids = [book.id for book in recommended_books]

    # 3. 随机获取另外 10 本书，必须排除掉已推荐的 ID 保证不重复
    # order_by('?') 是 Django 实现数据库随机排序的简便方法
    random_books = Book.objects.exclude(id__in=recommended_ids).order_by('?')[:10]

    # 4. 将两部分书籍合并，组成 20 本
    all_books = recommended_books + list(random_books)

    # 5. 统一封装成前端需要的 JSON 格式
    book_list = []
    for book in all_books:
        book_list.append({
            'id': book.id,
            'book_name': book.book_name,
            'price': float(book.price),
            'subject': book.subject,
            'rating': book.rating,
            'image': book.image,
            'upc': book.UPC,
            'stock': book.stock
        })

    return JsonResponse({
        'status': 'success', 
        'count': len(book_list), 
        'data': book_list
    })