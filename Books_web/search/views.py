from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from .apps import SearchConfig
from .models import Book

def suggest_api(request):
    q = request.GET.get('q', '')
    if not q:
        return JsonResponse({'data': []})
    matched_upcs = SearchConfig.trie.query(q)
    books_info = Book.objects.filter(UPC__in = matched_upcs).values('book_name', 'subject', 'price', 'image', 'description', 'rating', 'stock')
    return JsonResponse({"data": list(books_info)})