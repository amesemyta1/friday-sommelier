from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic, View

from catalog.forms import (
    BeverageForm,
    SnackForm,
    FlavorForm,
    TasterProfileForm,
    BeverageSearchForm,
    SnackSearchForm,
    FlavorSearchForm,
)
from catalog.models import Beverage, Snack, Flavor, Taster, AlcoholType


class BeverageListView(generic.ListView):
    model = Beverage
    template_name = "catalog/beverage_list.html"
    context_object_name = "beverages"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get("search", "")
        context["search_form"] = BeverageSearchForm(
            initial={"search": search_query}
        )
        return context

    def get_queryset(self):
        queryset = Beverage.objects.select_related(
            "alcohol_type"
        ).prefetch_related("flavors")
        form = BeverageSearchForm(self.request.GET)
        if form.is_valid() and form.cleaned_data["search"]:
            query = form.cleaned_data["search"]
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
        return queryset


class BeverageDetailView(LoginRequiredMixin, generic.DetailView):
    model = Beverage
    template_name = "catalog/beverage_detail.html"
    context_object_name = "beverage"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["is_favorite"] = (
                self.request.user.favorite_beverages.filter(
                    pk=self.object.pk
                ).exists()
            )
        return context


class BeverageCreateView(LoginRequiredMixin, generic.CreateView):
    model = Beverage
    form_class = BeverageForm
    template_name = "catalog/beverage_form.html"
    success_url = reverse_lazy("catalog:beverage-list")


class BeverageUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Beverage
    form_class = BeverageForm
    template_name = "catalog/beverage_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "catalog:beverage-detail", kwargs={"pk": self.object.pk}
        )


class BeverageDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Beverage
    template_name = "catalog/beverage_confirm_delete.html"
    success_url = reverse_lazy("catalog:beverage-list")


class SnackListView(generic.ListView):
    model = Snack
    template_name = "catalog/snack_list.html"
    context_object_name = "snacks"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get("search", "")
        context["search_form"] = SnackSearchForm(
            initial={"search": search_query}
        )
        return context

    def get_queryset(self):
        queryset = Snack.objects.all()
        form = SnackSearchForm(self.request.GET)
        if form.is_valid() and form.cleaned_data["search"]:
            query = form.cleaned_data["search"]
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
        return queryset


class SnackDetailView(LoginRequiredMixin, generic.DetailView):
    model = Snack
    template_name = "catalog/snack_detail.html"
    context_object_name = "snack"


class SnackCreateView(LoginRequiredMixin, generic.CreateView):
    model = Snack
    form_class = SnackForm
    template_name = "catalog/snack_form.html"
    success_url = reverse_lazy("catalog:snack-list")


class SnackUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Snack
    form_class = SnackForm
    template_name = "catalog/snack_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "catalog:snack-detail", kwargs={"pk": self.object.pk}
        )


class SnackDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Snack
    template_name = "catalog/snack_confirm_delete.html"
    success_url = reverse_lazy("catalog:snack-list")


class FlavorListView(generic.ListView):
    model = Flavor
    template_name = "catalog/flavor_list.html"
    context_object_name = "flavors"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get("search", "")
        context["search_form"] = FlavorSearchForm(
            initial={"search": search_query}
        )
        return context

    def get_queryset(self):
        queryset = Flavor.objects.all()
        form = FlavorSearchForm(self.request.GET)
        if form.is_valid() and form.cleaned_data["search"]:
            query = form.cleaned_data["search"]
            queryset = queryset.filter(name__icontains=query)
        return queryset


class FlavorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Flavor
    template_name = "catalog/flavor_detail.html"
    context_object_name = "flavor"


class FlavorCreateView(LoginRequiredMixin, generic.CreateView):
    model = Flavor
    form_class = FlavorForm
    template_name = "catalog/flavor_form.html"
    success_url = reverse_lazy("catalog:flavor-list")


class FlavorUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Flavor
    form_class = FlavorForm
    template_name = "catalog/flavor_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "catalog:flavor-detail", kwargs={"pk": self.object.pk}
        )


class FlavorDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Flavor
    template_name = "catalog/flavor_confirm_delete.html"
    success_url = reverse_lazy("catalog:flavor-list")


class TasterProfileView(LoginRequiredMixin, generic.UpdateView):
    model = Taster
    form_class = TasterProfileForm
    template_name = "catalog/taster_profile.html"
    success_url = reverse_lazy("catalog:profile")

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        preferred_flavors = user.preferred_flavors.all()

        if preferred_flavors.exists():
            context["recommended_beverages"] = (
                Beverage.objects.filter(flavors__in=preferred_flavors)
                .select_related("alcohol_type")
                .prefetch_related("flavors")
                .distinct()[:5]
            )
        else:
            context["recommended_beverages"] = None
        return context


class ToggleFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        beverage = get_object_or_404(Beverage, pk=pk)
        user = request.user
        if user.favorite_beverages.filter(pk=beverage.pk).exists():
            user.favorite_beverages.remove(beverage)
        else:
            user.favorite_beverages.add(beverage)
        referer = request.META.get("HTTP_REFERER")
        if referer:
            return redirect(referer)
        return redirect("catalog:beverage-detail", pk=pk)


class AlcoholTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = AlcoholType
    fields = ["name"]
    template_name = "catalog/alcohol_type_form.html"
    success_url = reverse_lazy("catalog:beverage-create")
