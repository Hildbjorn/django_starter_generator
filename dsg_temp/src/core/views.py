from django.views.generic import TemplateView


# СДЕЛАТЬ: Удалить форму - это только тест
from django import forms


class MyForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()


class DefaultPageView(TemplateView):
    template_name = 'layout/default.html'


class IndexPageView(TemplateView):
    template_name = 'home/index.html'

    # СДЕЛАТЬ: Удалить форму - это только тест
    def get_context_data(self, **kwargs):
        # Получаем контекст из родительского класса
        context = super().get_context_data(**kwargs)
        # Создаем экземпляр формы и добавляем его в контекст
        context['form'] = MyForm()
        return context
