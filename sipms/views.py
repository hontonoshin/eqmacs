from django.shortcuts import render, get_object_or_404
from .models import SiPM


def home(request):
    ctx = {
        "sipm_count": SiPM.objects.count(),
    }
    return render(request, "sipms/home.html", ctx)


def sipm_list(request):
    qs = SiPM.objects.all()

    layer = (request.GET.get("layer") or "").strip()
    daq_id = (request.GET.get("daq_id") or "").strip()
    asic = (request.GET.get("asic") or "").strip()
    channel = (request.GET.get("channel") or "").strip()

    if layer:
        qs = qs.filter(layer__iexact=layer)

    if daq_id:
        qs = qs.filter(daq_id__iexact=daq_id)

    if asic:
        qs = qs.filter(asic__iexact=asic)

    ctx = {
        "sipms": qs,
        "filter_layer": layer,
        "filter_daq_id": daq_id,
        "filter_asic": asic,
    }
    return render(request, "sipms/sipm_list.html", ctx)


def sipm_detail(request, pk):
    sipm = get_object_or_404(SiPM, pk=pk)
    return render(request, "sipms/sipm_detail.html", {"sipm": sipm})


def quick_search(request):
    q = (request.GET.get("q") or "").strip()

    sipms = SiPM.objects.all()
    if q:
        sipms = sipms.filter(channel__icontains=q)

    ctx = {
        "q": q,
        "results": sipms,
    }
    return render(request, "sipms/search_results.html", ctx)
