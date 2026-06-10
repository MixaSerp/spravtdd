# app/views.py
from django.views.generic import ListView
from django.db.models import Q  
from .models import Term

class TermListView(ListView):
    model = Term
    template_name = 'app/term_list.html'
    context_object_name = 'terms'
    ordering = ['name']
    paginate_by = 50
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(definition__icontains=query)
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context
