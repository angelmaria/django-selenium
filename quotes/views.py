# quotes/views.py
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Quote, Author, Tag, QuoteTag
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
from django.http import HttpResponse
from django.db.models import Count

# Configurar Matplotlib para usar el backend 'Agg'
matplotlib.use('Agg')

def quote_list(request):
    author_id = request.GET.get('author')
    tag_id = request.GET.get('tag')
    quotes = Quote.objects.all()

    # Filtrar por autor si se ha seleccionado uno
    if author_id:
        quotes = quotes.filter(author_id=author_id)
    
    # Filtrar por etiqueta si se ha seleccionado una
    if tag_id:
        quotes = quotes.filter(quote_tags__tag_id=tag_id)

    # Paginación
    paginator = Paginator(quotes, 10)  # Muestra 10 citas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Obtener la lista de autores y etiquetas para los formularios
    authors = Author.objects.all()
    tags = Tag.objects.all()  # Obtén todas las etiquetas

    return render(request, 'quotes/quote_list.html', {
        'page_obj': page_obj,
        'authors': authors,
        'tags': tags,  # Añade las etiquetas al contexto
        'selected_author': author_id,
        'selected_tag': tag_id,  # Añade la etiqueta seleccionada al contexto
    })

def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'quotes/author_detail.html', {'author': author})

def tag_detail(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    quotes = QuoteTag.objects.filter(tag=tag)
    return render(request, 'quotes/tag_detail.html', {'tag': tag, 'quotes': quotes})

def generate_tag_distribution_chart(request):
    tags = Tag.objects.all()
    tag_counts = QuoteTag.objects.values('tag_id').annotate(count=Count('quote_id'))

    tag_counts_df = pd.DataFrame(list(tag_counts))
    tags_df = pd.DataFrame(list(tags.values('id', 'name')))

    tag_distribution = tags_df.merge(tag_counts_df, left_on='id', right_on='tag_id')

    # Ordenar por cantidad y seleccionar las 10 etiquetas más repetidas
    top_tags = tag_distribution.sort_values('count', ascending=False).head(10)

    plt.figure(figsize=(12, 8))
    sns.barplot(x='count', y='name', data=top_tags, palette='viridis')
    plt.title('Top 10 Tags by Number of Quotes')
    plt.xlabel('Number of Quotes')
    plt.ylabel('Tag')
    plt.tight_layout()

    response = HttpResponse(content_type='image/png')
    plt.savefig(response, format='png')
    plt.close()
    return response

def generate_author_distribution_chart(request):
    authors = Author.objects.all()
    author_counts = Quote.objects.values('author_id').annotate(count=Count('id'))

    author_counts_df = pd.DataFrame(list(author_counts))
    authors_df = pd.DataFrame(list(authors.values('id', 'name')))

    author_distribution = authors_df.merge(author_counts_df, left_on='id', right_on='author_id')

    # Ordenar por cantidad y seleccionar las 10 autoras más repetidas
    top_authors = author_distribution.sort_values('count', ascending=False).head(10)

    plt.figure(figsize=(12, 8))
    sns.barplot(x='count', y='name', data=top_authors, palette='viridis')
    plt.title('Top 10 Authors by Number of Quotes')
    plt.xlabel('Number of Quotes')
    plt.ylabel('Author')
    plt.tight_layout()

    response = HttpResponse(content_type='image/png')
    plt.savefig(response, format='png')
    plt.close()
    return response

def generate_author_decade_distribution_chart(request):
    # Obtener las fechas de nacimiento de los autores
    authors = Author.objects.all().values('born')
    
    # Convertir las fechas de nacimiento a décadas
    authors_df = pd.DataFrame(list(authors))
    authors_df['born'] = pd.to_datetime(authors_df['born'])
    authors_df['decade'] = (authors_df['born'].dt.year // 10 * 10).astype(int)
    
    # Contar el número de autores por década
    decade_counts = authors_df['decade'].value_counts().reset_index()
    decade_counts.columns = ['decade', 'count']
    decade_counts = decade_counts.sort_values('decade')

    # Generar la gráfica
    plt.figure(figsize=(12, 8))
    sns.barplot(x='decade', y='count', data=decade_counts, palette='coolwarm')
    plt.title('Number of Authors by Decade')
    plt.xlabel('Decade')
    plt.ylabel('Number of Authors')
    plt.tight_layout()

    # Enviar la imagen como respuesta HTTP
    response = HttpResponse(content_type='image/png')
    plt.savefig(response, format='png')
    plt.close()
    return response

def about(request):
    # Obtener todos los autores y sus URLs
    authors = Author.objects.all()
    return render(request, 'quotes/about.html', {'authors': authors})