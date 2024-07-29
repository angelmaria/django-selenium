from django.contrib import admin
from .models import Author, Quote, Tag, QuoteTag

admin.site.register(Author)
admin.site.register(Quote)
admin.site.register(Tag)
admin.site.register(QuoteTag)
