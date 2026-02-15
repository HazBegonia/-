from django.apps import AppConfig
import sys

class SearchConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "search"
    trie = None

    def ready(self):
        if 'runserver' in sys.argv:
            from .utils import BookTrie
            from .models import Book
            SearchConfig.trie = BookTrie()
            all_books = Book.objects.values('book_name', 'UPC')
            
            for book in all_books:
                SearchConfig.trie.insert(book['book_name'], book['UPC'])
            print(f"--- Trie 树初始化完成，已载入 {len(all_books)} 本书籍 ---")