from django.shortcuts import render
from allauth.account.views import ConfirmEmailView
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from banks.models import EconomicIndicator
from django.views.decorators.cache import cache_page


class CustomConfirmEmailView(ConfirmEmailView):
    def get(self, *args, **kwargs):
        super().get(*args, **kwargs)
        return HttpResponseRedirect('/email-confirmed/')


@cache_page(60 * 15)  # Cache homepage for 15 minutes
def home(request):
    country = request.GET.get('country', '').strip()
    selected_indicator = request.GET.get('indicator', '').strip()
    year_from = request.GET.get('year_from')
    year_to = request.GET.get('year_to')

    data = EconomicIndicator.objects.all()

    if country:
        data = data.filter(country__icontains=country)

    if selected_indicator:
        data = data.filter(indicator_code=selected_indicator)

    if year_from and year_from.isdigit():
        data = data.filter(year__gte=int(year_from))

    if year_to and year_to.isdigit():
        data = data.filter(year__lte=int(year_to))

    paginator = Paginator(data, 20)  # 20 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # For the dropdown filter: distinct indicator codes and names
    indicators = EconomicIndicator.objects.values('indicator_code', 'indicator_name').distinct()

    context = {
        'page_obj': page_obj,
        'indicators': indicators,
        'selected_indicator': selected_indicator,
        'country': country,
        'year_from': year_from or '',
        'year_to': year_to or '',
    }
    return render(request, 'frontend/home.html', context)


def login_view(request):
    return render(request, 'frontend/login.html')


def register_view(request):
    return render(request, 'frontend/register.html')


def email_confirmed(request):
    return render(request, 'email_confirmed.html')


def email_confirmation_sent(request):
    return render(request, 'frontend/email_confirmation_sent.html')