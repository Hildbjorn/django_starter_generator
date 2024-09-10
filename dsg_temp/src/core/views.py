from pathlib import Path
from django.views.generic import TemplateView


class IndexPageView(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        # Получаем полный путь к директории проекта
        project_path = Path(__file__).resolve().parent
        # Извлекаем только название директории
        project_name = str(project_path.name)

        print('Проект: ', project_name)

        context = super().get_context_data(**kwargs)
        context['project_name'] = project_name
        return context
