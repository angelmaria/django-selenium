from django.urls import path
from . import views

urlpatterns = [
    path('', views.quote_list, name='quote_list'),
    path('author/<int:author_id>/', views.author_detail, name='author_detail'),
    path('tag/<int:tag_id>/', views.tag_detail, name='tag_detail'),
    path('generate-tag-distribution-chart/', views.generate_tag_distribution_chart, name='generate_tag_distribution_chart'),
    path('generate-author-distribution-chart/', views.generate_author_distribution_chart, name='generate_author_distribution_chart'),
    path('generate-author-decade-distribution-chart/', views.generate_author_decade_distribution_chart, name='generate_author_decade_distribution_chart'),
    path('about/', views.about, name='about'),
]
