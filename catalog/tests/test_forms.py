from django.test import TestCase
from catalog.models import AlcoholType, Flavor, Snack
from catalog.forms import BeverageForm, BeverageSearchForm


class CatalogFormTests(TestCase):
    def setUp(self):
        self.alcohol_type = AlcoholType.objects.create(name="Wine")
        self.flavor = Flavor.objects.create(name="Fruity")
        self.snack = Snack.objects.create(name="Cheese")

    def test_beverage_form_valid(self):
        form_data = {
            "name": "Merlot",
            "description": "Red wine",
            "average_price": 15.99,
            "alcohol_strength": 13.5,
            "alcohol_type": self.alcohol_type.id,
            "flavors": [self.flavor.id],
            "snacks": [self.snack.id],
        }
        form = BeverageForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_beverage_search_form(self):
        form = BeverageSearchForm(data={"search": "Jack"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["search"], "Jack")
