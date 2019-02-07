"""
iPPI-DB django forms
"""
import itertools
from collections import OrderedDict

from django import forms
from django.forms import ModelForm, inlineformset_factory
from django.utils.translation import ugettext_lazy as _, ugettext

from myapp import models


class BaseInlineNestedFormSet(forms.BaseInlineFormSet):
    def add_fields(self, form, index):
        super().add_fields(form, index)
        delete_field = form.fields.pop('DELETE')
        delete_field.widget.attrs["onclick"] = "delete_button_clicked(this)"
        delete_field.widget.attrs["class"] = delete_field.widget.attrs.get("class", "") + " formset-item-delete"
        delete_field.label = _("DELETE_label")
        delete_help_text = ugettext("DELETE_help_text")
        if delete_help_text != "DELETE_help_text":
            delete_field.help_text = delete_help_text
        form.fields = OrderedDict(
            itertools.chain([('DELETE', delete_field)], form.fields.items())
        )

    def is_valid(self):
        result = super().is_valid()

        if self.is_bound:
            for form in self.forms:
                result = result and form.is_valid()
                if hasattr(form, 'nested'):
                    result = result and form.nested.is_valid()

        return result

    def save(self, commit=True):
        result = super().save(commit=commit)

        for form in self.forms:
            if hasattr(form, 'nested'):
                if not self._should_delete_form(form):
                    form.nested.save(commit=commit)
        return result


class AddressForm(ModelForm):
    class Meta:
        model = models.Address
        fields = '__all__'

    # Even if we set the field to required in the model they are not in the html form. Its an intended feature of the
    # formset which allow you to add new formset item but not use it, and also use the DELETE checkbox
    # without having the browser indicating the user that the field must be field.
    # uncomment hereafter and you will see
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields["full_address"].widget.attrs["required"] = True


class PromotionForm(ModelForm):
    class Meta:
        model = models.Promotion
        fields = '__all__'


AddressInlineFormset = inlineformset_factory(
    parent_model=models.Student,
    model=models.Address,
    form=AddressForm,
    formset=BaseInlineNestedFormSet,
    # fields='__all__',
    extra=1,
    # min_num=1,# using the min_num is tempting, but with an nested inlined formset it does not work:
    # # it wants to have at least on address which is obsiouly empty when we check the DELETE of its empty student
    # # it make the formset being invalid. Prefer an extra=1, an in case of server side validation.
    # validate_min=True,
    can_delete=True,
)


class BaseStudentFormset(BaseInlineNestedFormSet):
    def add_fields(self, form, index):
        super().add_fields(form, index)
        form.nested = AddressInlineFormset(
            instance=form.instance,
            data=form.data if form.is_bound else None,
            files=form.files if form.is_bound else None,
            prefix='addresses-%s-%s' % (
                form.prefix,
                AddressInlineFormset.get_default_prefix()
            ),
            # queryset=models.Address.objects.filter(student=form.instance)
        )

    def clean(self):
        """Checks that no two articles have the same title."""
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return
        names = set()
        for form in self.forms:
            if form.cleaned_data.get("DELETE", False):
                continue

            # if the form is empty
            if not (form.has_changed() or 'first_name' in form.cleaned_data or 'last_name' in form.cleaned_data):
                continue

            name = form.cleaned_data['first_name'] + "__" + form.cleaned_data['last_name']
            if name in names:
                raise forms.ValidationError(
                    _("Student must be distinct. Incriminated entry:'%(last_name)s %(first_name)s'") %
                    dict(
                        first_name=form.cleaned_data['first_name'],
                        last_name=form.cleaned_data['last_name']
                    )
                )
            names.add(name)


StudentInlineFormset = inlineformset_factory(
    parent_model=models.Promotion,
    model=models.Student,
    formset=BaseStudentFormset,
    fields='__all__',
    extra=0,
    min_num=1,  # here you can use it
    validate_min=True,
    can_delete=True,
)
