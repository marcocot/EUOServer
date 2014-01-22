from django.http import HttpResponse
from django.utils.text import slugify
from django.views.generic import DetailView
from .models import Script


class ScriptDetailView(DetailView):
    model = Script
    # http_method_names = ['post', ]
    slug_field = 'hash'

    def get_context_data(self, **kwargs):
        kwargs['title'] = self.object.title
        return kwargs

    def render_to_response(self, context, **response_kwargs):
        response = HttpResponse(content_type='text/x-euo')
        response['Content-Disposition'] = 'attachment; filename="%s.euo"' % slugify(context['title'])

        import pdb;

        pdb.set_trace()

        response.write(self.object.script.read())

        return response