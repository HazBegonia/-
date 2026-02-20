from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from .apps import SearchConfig
from .models import Book    
from my_profile.models import SearchHistory
from users.models import user_info

def suggest_api(request):
    q = request.GET.get('q', '').strip()
    if not q:
        return JsonResponse({'data': []})

    user_id = request.session.get('user_id')
    user_name_from_session = request.session.get('user_name')
    print(f"当前搜索词: {q}, 长度: {len(q)}")
    print(f"Session中的用户ID: {user_id}")
    
    if user_id:
        try:
            current_user = user_info.objects.get(id=user_id)
            SearchHistory.objects.create(
                user_id=user_id,
                user=current_user, 
                username=user_name_from_session,
                browse_books=q
            )
            print("Successfully saved to database!")
        except Exception as e:
            print(f"保存失败，错误原因: {e}")

    matched_upcs = SearchConfig.trie.query(q)
    books_info = Book.objects.filter(UPC__in = matched_upcs).values(
        'book_name', 'subject', 'price', 'image', 'description', 'rating', 'stock', 'UPC'
    )
    return JsonResponse({"data": list(books_info)})