from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from catalog.models import AlcoholType, Flavor, Snack, Beverage
from catalog.forms import BeverageForm, BeverageSearchForm, SnackForm


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


class CatalogViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testtaster",
            password="Password123",
            email="taster@test.com",
            experience_level=1
        )

        self.alcohol_type = AlcoholType.objects.create(name="Vodka")
        self.flavor = Flavor.objects.create(name="Bitter")

        self.beverage = Beverage.objects.create(
            name="Absolute Vodka",
            description="Premium Swedish vodka",
            average_price=20.00,
            alcohol_strength=40.0,
            alcohol_type=self.alcohol_type
        )
        self.beverage.flavors.add(self.flavor)

    def test_beverage_list_view_status_code(self):
        response = self.client.get(reverse("catalog:beverage-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/beverage_list.html")
        self.assertIn("beverages", response.context)

    def test_beverage_list_search_filtering(self):
        response = self.client.get(reverse("catalog:beverage-list"), {"search": "Absolute"})
        self.assertEqual(len(response.context["beverages"]), 1)

        response = self.client.get(reverse("catalog:beverage-list"), {"search": "NonExistent"})
        self.assertEqual(len(response.context["beverages"]), 0)

    def test_beverage_detail_view_anonymous_redirect(self):
        response = self.client.get(reverse("catalog:beverage-detail", kwargs={"pk": self.beverage.pk}))
        self.assertEqual(response.status_code, 302)

    def test_beverage_detail_view_authenticated(self):
        self.client.login(username="testtaster", password="Password123")
        response = self.client.get(reverse("catalog:beverage-detail", kwargs={"pk": self.beverage.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/beverage_detail.html")
        self.assertFalse(response.context["is_favorite"])

    def test_toggle_favorite_view(self):
        self.client.login(username="testtaster", password="Password123")
        url = reverse("catalog:toggle-favorite", kwargs={"pk": self.beverage.pk})

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Редирект
        self.assertTrue(self.user.favorite_beverages.filter(pk=self.beverage.pk).exists())

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.user.favorite_beverages.filter(pk=self.beverage.pk).exists())

    def test_beverage_create_view_post(self):
        self.client.login(username="testtaster", password="Password123")
        data = {
            "name": "New Gin",
            "description": "Fresh flavor",
            "average_price": 30.00,
            "alcohol_strength": 37.5,
            "alcohol_type": self.alcohol_type.id,
        }
        response = self.client.post(reverse("catalog:beverage-create"), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Beverage.objects.filter(name="New Gin").exists())

    def test_taster_profile_recommendations(self):
        self.client.login(username="testtaster", password="Password123")
        self.user.preferred_flavors.add(self.flavor)

        response = self.client.get(reverse("catalog:profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/taster_profile.html")

        recommended = response.context["recommended_beverages"]
        self.assertIsNotNone(recommended)
        self.assertIn(self.beverage, recommended)