from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)
    about = models.TextField(null=True, blank=True)
    born = models.DateField(null=True, blank=True)
    birth_place = models.CharField(max_length=100, null=True, blank=True)
    about_page_url = models.URLField(max_length=200, null=True, blank=True)  # Campo para almacenar la URL de la página "about"

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'authors'

class Quote(models.Model):
    text = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='quotes')

    def __str__(self):
        return f"{self.text[:50]}... - {self.author.name}"

    class Meta:
        db_table = 'quotes'

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tags'

class QuoteTag(models.Model):
    id = models.AutoField(primary_key=True)  # Agregar un campo de ID como clave primaria
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='quote_tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='quote_tags')

    class Meta:
        db_table = 'quote_tags'
        unique_together = ('quote', 'tag')  # Asegura que la combinación de quote y tag sea única
