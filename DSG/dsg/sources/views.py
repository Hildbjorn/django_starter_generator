from django.shortcuts import render
from django.views import View


__all__ = (
    'page_not_found_view',
    'HomeView',
    'PageView',
)


def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)


class HomeView(View):
    """ Отображение главной страницы """

    def get(self, request):
        return render(request, "home/home.html")


class PageView(View):
    """ Отображение страницы проекта """

    def get(self, request):
        return render(request, "home/page.html")
