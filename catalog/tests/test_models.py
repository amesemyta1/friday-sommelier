from django.test import TestCase
from catalog.models import AlcoholType, Flavor, Snack, Beverage


class CatalogModelTests(TestCase):
    def test_alcohol_type_str(self):
        alcohol_type = AlcoholType.objects.create(name="Whisky")
        self.assertEqual(str(alcohol_type), "Whisky")

    def test_flavor_str(self):
        flavor = Flavor.objects.create(name="Sweet")
        self.assertEqual(str(flavor), "Sweet")

    def test_snack_str(self):
        snack = Snack.objects.create(name="Chips", description="Salted chips")
        self.assertEqual(str(snack), "Chips")

    def test_beverage_str(self):
        alcohol_type = AlcoholType.objects.create(name="Beer")
        beverage = Beverage.objects.create(
            name="Guinness",
            average_price=4.50,
            alcohol_strength=4.2,
            alcohol_type=alcohol_type
        )
        self.assertEqual(str(beverage), "Guinness (4.2%)")