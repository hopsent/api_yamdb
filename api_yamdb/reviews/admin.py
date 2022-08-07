from django.contrib import admin

from .models import User, Review, Comments, Title, Category, Genre


class ReviewAdmin(admin.ModelAdmin):
    """Администрирование отзывов."""
    list_display = (
        'pk', 'text', 'author', 'score', 'pub_date'
    )
    search_fields = ('author',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    """Администрирование комментариев."""
    list_display = (
        'pk', 'text', 'author', 'pub_date'
    )
    search_fields = ('author',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


admin.site.register(User)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comments, CommentAdmin)
admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(Category)
