from django.db import transaction
from django.views.generic import DetailView, ListView, UpdateView, CreateView
from django.views.generic.edit import FormMixin

from myapp import models, forms


class EmbededFormsetMixin(FormMixin):
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = forms.StudentInlineFormset(self.request.POST, instance=self.object)
        else:
            data['formset'] = forms.StudentInlineFormset(instance=self.object)
        return data

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save()
            # form.instance = self.object
            context = self.get_context_data()
            formset = context['formset']

            if formset.is_valid():
                formset.instance = self.object
                formset.save()
            else:
                return super().form_invalid(form)
        return super().form_valid(form)


class PromotionUpdateView(EmbededFormsetMixin, UpdateView):
    model = models.Promotion
    fields = '__all__'


class PromotionDetailView(DetailView):
    model = models.Promotion


class PromotionListView(ListView):
    model = models.Promotion


class PromotionCreateView(EmbededFormsetMixin, CreateView):
    model = models.Promotion
    fields = '__all__'
