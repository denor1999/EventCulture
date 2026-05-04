from django import forms
from django.core.validators import MinValueValidator
from .models import Category, Tag
from django.utils import timezone
from django.core.exceptions import ValidationError
import re
from .models import Event

def transliterate_to_latin(text):
                mapping = {
                    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
                    'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
                    'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
                    'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '',
                    'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya', ' ': '-'
                }
    
                result = []
                for char in text.lower():
                    if char in mapping:
                        result.append(mapping[char])
                    elif char.isalnum():
                        result.append(char)
                    else:
                        result.append('-')
    
                slug = re.sub(r'-+', '-', ''.join(result)).strip('-')
                return slug

def validate_russian_title(value):
    # Разрешённые символы: русские буквы, цифры, пробел, дефис
    pattern = r'^[А-Яа-яЁё0-9\s\-]+$'
    
    if not re.match(pattern, value):
        raise ValidationError(
            'Название должно содержать только русские буквы, цифры, пробелы и дефисы. '
            'Латинские буквы и спецсимволы запрещены.'
        )


def validate_future_date(value):    
    if value < timezone.now():
        raise ValidationError('Дата мероприятия не может быть в прошлом. Выберите будущую дату.')
    

class AddEventForm(forms.Form):
    
    title = forms.CharField(
        max_length=255,
        min_length=3,
        label="Название мероприятия",
        validators=[validate_russian_title],
        error_messages={
            'min_length': 'Название должно быть не короче 3 символов',
            'max_length': 'Название не может быть длиннее 255 символов',
            'required': 'Пожалуйста, заполните название мероприятия',
        }
    )
    
    slug = forms.SlugField(
        max_length=255,
        label="URL (slug)",
        error_messages={
        'min_length': 'Название должно быть не короче 3 символов',
        'max_length': 'Название не может быть длиннее 255 символов',
        'required': 'Пожалуйста, заполните название мероприятия',
        }
    )
    
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}),
        required=False,
        label="Описание"
    )
    
    venue = forms.CharField(
        max_length=255,
        label="Площадка",
        error_messages={'required': 'Укажите площадку проведения'}
    )
    
    address = forms.CharField(
        max_length=255,
        required=False,
        label="Адрес"
    )
    
    date = forms.DateTimeField(
    widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
    label="Дата и время",
    validators=[validate_future_date],
    error_messages={'required': 'Выберите дату и время мероприятия'}
    )
    
    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        initial=0,
        label="Цена",
        validators=[
            MinValueValidator(0, message='Цена не может быть отрицательной')
        ]
    )
    
    is_published = forms.BooleanField(
        required=False,
        initial=True,
        label="Опубликовать"
    )
    
    cat = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Выберите категорию",
        label="Категория",
        error_messages={'required': 'Выберите категорию мероприятия'}
    )
    
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'size': 5}),
        label="Теги"
    )

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        slug = cleaned_data.get('slug')
        
        if title and slug:
            
            expected_slug = title.lower().replace(' ', '-')
            expected_slug = transliterate_to_latin(title)
            
            if expected_slug != slug:
                self.add_error('slug', f'Рекомендуемый slug: "{expected_slug}"')
        
        return cleaned_data



class EventModelForm(forms.ModelForm):
    
    class Meta:
        model = Event
        fields = ['title', 'slug', 'description', 'venue', 'address', 
                  'date', 'price', 'is_published', 'cat', 'tags', 'image']
        
        labels = {
            'title': 'Название мероприятия',
            'slug': 'URL (slug)',
            'description': 'Описание',
            'venue': 'Площадка',
            'address': 'Адрес',
            'date': 'Дата и время',
            'price': 'Цена',
            'is_published': 'Опубликовать',
            'cat': 'Категория',
            'tags': 'Теги',
        }
        
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'cols': 50}),
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'tags': forms.SelectMultiple(attrs={'size': 5}),
        }
        
        error_messages = {
            'title': {
                'required': 'Пожалуйста, заполните название мероприятия',
            },
            'slug': {
                'required': 'URL обязателен',
                'invalid': 'Slug может содержать только латинские буквы, цифры, дефис и подчёркивание',
            },
            'venue': {
                'required': 'Укажите площадку проведения',
            },
            'date': {
                'required': 'Выберите дату и время мероприятия',
            },
            'cat': {
                'required': 'Выберите категорию мероприятия',
            },
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        
        # Особые настройки для поля slug
        self.fields['slug'].widget.attrs.update({'class': 'form-control slug-field'})
        
        # Для тегов — особый виджет
        self.fields['tags'].help_text = 'Удерживайте Ctrl для выбора нескольких тегов'
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 3:
            raise ValidationError('Название должно быть не короче 3 символов')
        return title
    
    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date and date < timezone.now():
            raise ValidationError('Дата мероприятия не может быть в прошлом')
        return date
    
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        slug = cleaned_data.get('slug')
        
        if title and slug:
            expected_slug = transliterate_to_latin(title)
            if expected_slug != slug:
                self.add_error('slug', f'Рекомендуемый slug: "{expected_slug}"')
        
        return cleaned_data