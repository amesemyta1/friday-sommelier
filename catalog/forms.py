from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.forms import UserCreationForm

from catalog.models import Beverage, Flavor, Snack, Taster


class BeverageForm(forms.ModelForm):
    class Meta:
        model = Beverage
        fields = [
            "name",
            "description",
            "average_price",
            "alcohol_strength",
            "alcohol_type",
            "flavors",
            "snacks",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g., Whisky Jack Daniels",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Describe the beverage...",
                }
            ),
            "average_price": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "alcohol_strength": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.1"}
            ),
            "alcohol_type": forms.Select(attrs={"class": "form-control"}),
            "flavors": forms.CheckboxSelectMultiple(),
            "snacks": forms.CheckboxSelectMultiple(),
        }


class SnackForm(forms.ModelForm):
    class Meta:
        model = Snack
        fields = ["name", "description", "is_cooking_required"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Provide a brief description of the snack",
                }
            ),
            "is_cooking_required": forms.CheckboxInput(
                attrs={
                    "class": "is_cooking_required",
                }
            ),
        }


class FlavorForm(forms.ModelForm):
    class Meta:
        model = Flavor
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g., Fruity, Bitter, Sweet",
                }
            ),
        }


class TasterCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Taster
        fields = UserCreationForm.Meta.fields + (
            "email",
            "experience_level",
            "preferred_flavors",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "email" in self.fields:
            self.fields["email"].widget.attrs.update({"class": "form-control"})
        self.fields["experience_level"].widget.attrs.update(
            {"class": "form-control"}
        )
        self.fields["preferred_flavors"].widget = (
            forms.CheckboxSelectMultiple()
        )


class TasterSignupForm(SignupForm):
    experience_level = forms.ChoiceField(
        choices=Taster.Experience.choices,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Experience Level",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name in ["username", "email"]:
                field.required = True
                if field.label and " (optional)" in field.label:
                    field.label = field.label.replace(" (optional)", "")
            if field_name not in ["experience_level"]:
                field.widget.attrs.update({"class": "form-control"})

    def save(self, request):
        user = super().save(request)
        user.experience_level = self.cleaned_data["experience_level"]
        user.save()
        return user


class TasterProfileForm(forms.ModelForm):
    class Meta:
        model = Taster
        fields = ["experience_level", "preferred_flavors"]
        widgets = {
            "experience_level": forms.Select(attrs={"class": "form-control"}),
            "preferred_flavors": forms.CheckboxSelectMultiple(),
        }


class BeverageSearchForm(forms.Form):
    search = forms.CharField(
        label="",
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "search-input",
                "placeholder": "Search by beverage name or description...",
            }
        ),
    )


class SnackSearchForm(forms.Form):
    search = forms.CharField(
        label="",
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "search-input",
                "placeholder": "Search by snack name or description...",
            }
        ),
    )


class FlavorSearchForm(forms.Form):
    search = forms.CharField(
        label="",
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "search-input",
                "placeholder": "Search by flavor name (e.g. Sweet, Woody)...",
            }
        ),
    )
