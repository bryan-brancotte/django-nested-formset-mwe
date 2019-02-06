from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, ListView, UpdateView, CreateView

from myapp import models, forms

class PromotionUpdateView(UpdateView):
    model = models.Promotion
    fields = '__all__'

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
            context = self.get_context_data()
            formset = context['formset']

            if formset.is_valid():
                formset.instance = self.object
                formset.save()
        return super().form_valid(form)


class PromotionDetailView(DetailView):
    model = models.Promotion


class PromotionListView(ListView):
    model = models.Promotion


class PromotionCreateView(CreateView):
    model = models.Promotion
    fields = '__all__'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = forms.StudentInlineFormset(self.request.POST)
        else:
            data['formset'] = forms.StudentInlineFormset()
        return data

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save()
            context = self.get_context_data()
            formset = context['formset']

            if formset.is_valid():
                formset.instance = self.object
                formset.save()
        return super().form_valid(form)
