import urllib.request
from django.core.files import File
from django.db import models
from django.urls import reverse

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Event.Status.PUBLISHED)


class Tag(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Тег")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Event(models.Model):
    
    title = models.CharField(max_length=255, verbose_name="Название мероприятия")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    description = models.TextField(blank=True, verbose_name="Описание")
    venue = models.CharField(max_length=255, verbose_name="Площадка")
    address = models.CharField(max_length=255, blank=True, verbose_name="Адрес")
    date = models.DateTimeField(verbose_name="Дата и время")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Цена")
    image_url = models.URLField(blank=True, verbose_name="Ссылка на изображение")
    image = models.ImageField(
        upload_to='events/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name="Изображение мероприятия"
    )
    
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время обновления")

    #Связь с категориями "Многие к одному"
    cat = models.ForeignKey(
        'Category',
        on_delete=models.PROTECT,
        related_name = 'events',
        verbose_name="Категория"
    )

    tags = models.ManyToManyField(Tag, blank=True, related_name='events', verbose_name="Теги")
    
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'
    
    is_published = models.BooleanField(
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name="Статус публикации"
    )
    
    objects = models.Manager()
    published = PublishedManager()
    
    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"
        ordering = ['-date']  # Сортировка по дате (новые сверху)
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['slug']),
        ]

    def download_image_from_url(self):
        if self.image_url and not self.image:
            try:
                response = urllib.request.urlopen(self.image_url)
                file_name = f"event_{self.id}.jpg"
                self.image.save(file_name, File(response))
                self.save()
                return True
            except Exception as e:
                print(f"Ошибка: {e}")
                return False
        return False    
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'event_slug': self.slug})
    

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"