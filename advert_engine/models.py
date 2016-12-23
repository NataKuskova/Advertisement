import uuid
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Advert(models.Model):
    CREATED = 'created'
    PUBLISHED = 'published'
    DEACTIVATED = 'deactivated'
    STATUS_CHOICES = (
        (CREATED, 'Created'),
        (PUBLISHED, 'Published'),
        (DEACTIVATED, 'Deactivated'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    publish_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=50,
                              choices=STATUS_CHOICES,
                              default=CREATED)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_views = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def first_image(self):
        galleries = self.galleries.order_by('date').all()[:1]
        if galleries.exists():
            return galleries
        return None


class Gallery(models.Model):
    image = models.ImageField(default='None', upload_to='images/')
    name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    advert = models.ForeignKey(Advert, on_delete=models.CASCADE,
                               related_name='galleries')

    def __str__(self):
        return self.name
