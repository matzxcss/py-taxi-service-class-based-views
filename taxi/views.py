from django.shortcuts import render
from django.views import generic

from taxi.models import Car, Driver, Manufacturer


def index(request):

    context = {
        "num_drivers": Driver.objects.count(),
        "num_cars": Car.objects.count(),
        "num_manufacturers": Manufacturer.objects.count(),
    }

    return render(request, "taxi/index.html", context=context)


class ManufacturerListView(generic.ListView):
    model = Manufacturer
    queryset = Manufacturer.objects.all().order_by("name")
    paginate_by = 5


class CarListView(generic.ListView):
    queryset = (
        Car.objects.select_related("manufacturer").all().order_by("model")
    )
    paginate_by = 5


class CarDetailView(generic.DetailView):
    model = Car
    template_name = "taxi/car_detail.html"
    queryset = (
        Car.objects.prefetch_related("drivers")
        .select_related("manufacturer")
        .all()
    )


class DriverListView(generic.ListView):
    model = Driver
    queryset = Driver.objects.all().order_by("username")
    paginate_by = 5


class DriverDetailView(generic.DetailView):
    model = Driver
    template_name = "taxi/driver_detail.html"
    queryset = Driver.objects.prefetch_related("cars").all()
