from django.contrib import admin
from django.contrib import messages
from .models import Event, Category, Tag

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'cat', 'date', 'price', 'is_published')
    list_display_links = ('id', 'title')
    list_editable = ('is_published',)
    ordering = ('-date', 'title')
    list_per_page = 10
    actions = ['make_published', 'make_draft']
    search_fields = ['title', 'cat__name', 'venue']
    list_filter = ['is_published', 'cat', 'date']

    fields = ['title', 'slug', 'cat', 'tags', 'venue', 'address', 'date', 'price', 'description', 'image_url', 'is_published']
        
    prepopulated_fields = {'slug': ('title',)}
    
    filter_horizontal = ['tags']

    @admin.display(description="Длина описания")
    def short_description(self, obj):
        if obj.description:
            return f"{len(obj.description)} симв."
        return "Нет описания"
    
    @admin.action(description="Опубликовать выбранные мероприятия")
    def make_published(self, request, queryset):
        count = queryset.update(is_published=Event.Status.PUBLISHED)
        self.message_user(request, f"Опубликовано {count} мероприятие(й).", messages.SUCCESS)

    @admin.action(description="Снять с публикации выбранные мероприятия")
    def make_draft(self, request, queryset):
        count = queryset.update(is_published=Event.Status.DRAFT)
        self.message_user(request, f"{count} мероприятие(й) снято с публикации.", messages.WARNING)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    ordering = ('name',)
    search_fields = ['name']

    prepopulated_fields = {'slug': ('name',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    ordering = ('name',)
    search_fields = ['name']

    prepopulated_fields = {'slug': ('name',)}

# Register your models here.
