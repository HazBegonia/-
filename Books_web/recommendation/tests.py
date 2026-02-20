from django.http import JsonResponse
from .recommender import BookRecommender
from users.models import user_info
from django.views.decorators.http import require_GET

@require_GET
def get_recommendations(request):
    username = request.GET.get('username')
    try:
        user = user_info.objects.get(username=username)
    except user_info.DoesNotExist:
        return JsonResponse({'error': 'User not found', 'data': []}, status=404)

    recommender = BookRecommender(user)
    recommended_books = recommender.train_and_predict()

    book_list = []
    for book in recommended_books:
        book_list.append({
            'id': book.id,
            'book_name': book.book_name,
            'price': float(book.price),
            'subject': book.subject,
            'rating': book.rating,
            'image': book.image,
            'upc': book.UPC
        })

    return JsonResponse({
        'status': 'success',
        'count': len(book_list),
        'data': book_list
    })