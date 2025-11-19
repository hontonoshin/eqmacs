from django.contrib import admin
from .models import SiPM
from . import models as m
from django import forms
from django.contrib import messages





class SiPMGainMeasurementInline(admin.TabularInline):
    model = m.SiPMGainMeasurement
    extra = 0           
    fields = ("order", "voltage", "mean_peak_distance", "sigma", "txt_file", "plot_image")
    readonly_fields = ("order", "voltage", "mean_peak_distance", "sigma")


@admin.register(SiPM)
class SiPMAdmin(admin.ModelAdmin):
    list_display = ("channel", "layer", "daq_id", "asic")
    list_filter = ("layer", "daq_id", "asic")
    search_fields = ("channel",)
    fields = (
        "layer", "daq_id", "asic", "channel",
    )
    
    inlines = [SiPMGainMeasurementInline]


