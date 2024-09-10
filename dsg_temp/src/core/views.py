from django.views.generic import TemplateView


class IndexPageView(TemplateView):
    template_name = 'home/index.html'
