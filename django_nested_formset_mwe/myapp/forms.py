"""
iPPI-DB django forms
"""

from django import forms
from django.forms import ModelForm, inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from myapp import models


class BaseInlineNestedFormSet(forms.BaseInlineFormSet):

    def is_valid(self):
        result = super().is_valid()

        if self.is_bound:
            for form in self.forms:
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["full_address"].widget.attrs["required"] = True


class StudentForm(ModelForm):
    class Meta:
        model = models.Student
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs["required"] = True
        self.fields["last_name"].widget.attrs["required"] = True


class PromotionForm(ModelForm):
    class Meta:
        model = models.Promotion
        fields = '__all__'


AddressInlineFormset = inlineformset_factory(
    parent_model=models.Student,
    model=models.Address,
    form=AddressForm,
    extra=0,
    min_num=1,
    validate_min=True,
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
    form=StudentForm,
    extra=0,
    min_num=1,
    validate_min=True,
    can_delete=True,
)
