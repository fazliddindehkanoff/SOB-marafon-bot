from django.contrib import admin
from django.template.response import TemplateResponse
from django import forms

from bot.models import TelegramUser
from bot.constants import REGIONS


class DashboardFilterForm(forms.Form):
    start_date = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date"})
    )
    end_date = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date"})
    )
    region = forms.ChoiceField(choices=REGIONS, required=False)


def custom_admin_index(request):
    form = DashboardFilterForm(request.GET or None)
    users = TelegramUser.objects.all()

    if form.is_valid():
        start_date = form.cleaned_data.get("start_date")
        end_date = form.cleaned_data.get("end_date")
        region = form.cleaned_data.get("region")

        if start_date:
            users = users.filter(registered_at__date__gte=start_date)
        if end_date:
            users = users.filter(registered_at__date__lte=end_date)
        if region:
            users = users.filter(region=region)

    context = dict(
        admin.site.each_context(request),
        title="Dashboard",
        form=form,
        registered_count=users.count(),
        paid_count=users.filter(is_subscribed=True).count(),
        unpaid_count=users.filter(is_subscribed=False).count(),
    )
    return TemplateResponse(request, "admin/custom_index.html", context)
