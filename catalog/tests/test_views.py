from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from catalog.models import AlcoholType, Flavor, Beverage


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
