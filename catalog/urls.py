from django.urls import path

from catalog.views import (
    BeverageListView,
    BeverageDetailView,
    BeverageCreateView,
    BeverageUpdateView,
    BeverageDeleteView,
    SnackListView,
    SnackDetailView,
    SnackCreateView,
    SnackUpdateView,
    SnackDeleteView,
    FlavorListView,
    FlavorDetailView,
    FlavorCreateView,
    FlavorUpdateView,
    FlavorDeleteView,
    TasterProfileView,
    ToggleFavoriteView,
)

urlpatterns = [
    path("beverages/", BeverageListView.as_view(), name="beverage-list"),
    path(
        "beverages/<int:pk>/",
        BeverageDetailView.as_view(),
        name="beverage-detail",
    ),
    path(
        "beverages/create/",
        BeverageCreateView.as_view(),
        name="beverage-create",
    ),
    path(
        "beverages/<int:pk>/update/",
        BeverageUpdateView.as_view(),
        name="beverage-update",
    ),
    path(
        "beverages/<int:pk>/delete/",
        BeverageDeleteView.as_view(),
        name="beverage-delete",
    ),
    path("snacks/", SnackListView.as_view(), name="snack-list"),
    path("snacks/<int:pk>/", SnackDetailView.as_view(), name="snack-detail"),
    path("snacks/create/", SnackCreateView.as_view(), name="snack-create"),
    path(
        "snacks/<int:pk>/update/",
        SnackUpdateView.as_view(),
        name="snack-update",
    ),
    path(
        "snacks/<int:pk>/delete/",
        SnackDeleteView.as_view(),
        name="snack-delete",
    ),
    path("flavors/", FlavorListView.as_view(), name="flavor-list"),
    path(
        "flavors/<int:pk>/", FlavorDetailView.as_view(), name="flavor-detail"
    ),
    path("flavors/create/", FlavorCreateView.as_view(), name="flavor-create"),
    path(
        "flavors/<int:pk>/update/",
        FlavorUpdateView.as_view(),
        name="flavor-update",
    ),
    path(
        "flavors/<int:pk>/delete/",
        FlavorDeleteView.as_view(),
        name="flavor-delete",
    ),
    path("profile/", TasterProfileView.as_view(), name="profile"),
    path(
        "beverages/<int:pk>/toggle-favorite/",
        ToggleFavoriteView.as_view(),
        name="toggle-favorite",
    ),
]

app_name = "catalog"
