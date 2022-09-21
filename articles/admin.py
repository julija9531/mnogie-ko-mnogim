from django.contrib import admin
from django.forms import BaseInlineFormSet
from django.core.exceptions import ValidationError

from .models import Article, Scope, Tag


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        n_1 = 0
        for form in self.forms:
            if form.cleaned_data.get('is_main', False):
                n_1 +=1

        if n_1 == 0:
            raise ValidationError('Укажите основной раздел')
        elif n_1 != 1:
            raise ValidationError('Основным может быть только один раздел')
        else:
            return super().clean()  # вызываем базовый код переопределяемого метода

class ScopeInLine(admin.TabularInline):
    model = Scope
    extra = 3
    formset = ScopeInlineFormset

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInLine, ]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]

