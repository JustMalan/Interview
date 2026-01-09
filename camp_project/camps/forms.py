from django import forms
from .models import Camp, ParentRegistration, Student, CampRegistration


class CampForm(forms.ModelForm):
    class Meta:
        model = Camp
        fields = ["name", "start_date", "end_date"]


class ParentRegistrationForm(forms.ModelForm):
    class Meta:
        model = ParentRegistration
        fields = ["parent_name", "email"]


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["first_name", "last_name", "age"]


class CampRegistrationForm(forms.ModelForm):
    class Meta:
        model = CampRegistration
        fields = ["camp", "duration_weeks"]

    def __init__(self, *args, **kwargs):
        # allow passing parent_registration in at runtime
        self.parent_registration = kwargs.pop("parent_registration", None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        obj = super().save(commit=False)
        if self.parent_registration:
            obj.parent_registration = self.parent_registration
        if commit:
            obj.save()
        return obj
