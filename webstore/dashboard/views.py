from django.views.generic import TemplateView


class DashboardWelcomeView(TemplateView):
    """
    Generic TemplateView,
    **Template:**
    :template:`dasboard/base_dashboard.html`
    """
    template_name = 'dashboard/base_dashboard.html'
