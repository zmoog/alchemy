from django.views.generic.base import TemplateView

class SpaView(TemplateView):

	template_name = "spa/home.html"