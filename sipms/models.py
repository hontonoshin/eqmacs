from django.db import models


###### admin: ginnoji
###### password: ForeverYorozuya



class TimeStamped(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SiPM(TimeStamped):
    layer = models.CharField(max_length=64,blank=True)
    daq_id = models.CharField(max_length=64,blank=True)
    asic = models.CharField(max_length=64,blank=True)
    channel = models.CharField(max_length=128, unique=True)

    class Meta:
        ordering = ["layer", "daq_id", "asic", "channel"]

    def __str__(self):
        return f"{self.channel} (L{self.layer}, DAQ {self.daq_id}, ASIC {self.asic})"


class SiPMGainMeasurement(TimeStamped):

    sipm = models.ForeignKey(
        SiPM,
        on_delete=models.CASCADE,
        related_name="gain_measurements",
    )


    order = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )
    voltage = models.FloatField()
    mean_peak_distance = models.FloatField()
    sigma = models.FloatField(
        null=True, blank=True,
    )

    txt_file = models.FileField(
        upload_to="sipm_gain/txt/",
        null=True, blank=True,
    )
    plot_image = models.ImageField(
        upload_to="sipm_gain/plots/",
        null=True, blank=True,
    )

    class Meta:
        ordering = ["sipm", "voltage"]
        unique_together = ("sipm", "voltage")   

    def __str__(self):
        return f"{self.sipm} @ {self.voltage} V"

    def parse_txt_into_fields(self):
        if not self.txt_file:
            return

        self.txt_file.seek(0)
        data = self.txt_file.read()

        if isinstance(data, bytes):
            data = data.decode("utf-8", errors="ignore")

        content = data.strip()
        if not content:
            return

        parts = content.split()
        if len(parts) < 4:
            return

        try:
            idx = int(parts[0])
            voltage = float(parts[1])
            mean = float(parts[2])
            sigma = float(parts[3])
        except ValueError:
            return

        self.voltage = voltage
        self.mean_peak_distance = mean
        self.sigma = sigma

        self.txt_file.seek(0)

    def save(self, *args, **kwargs):
        if self.txt_file and (self.mean_peak_distance is None or self.voltage is None):
            self.parse_txt_into_fields()
        super().save(*args, **kwargs)
