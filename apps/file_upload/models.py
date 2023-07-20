from django.db import models
from .utils import get_filtered_image
from PIL import Image
import numpy as np
from io import BytesIO
from django.core.files.base import ContentFile

ACTION_CHOISES = (
    ("NO_FILTER", "no filter"),
    ("COLORIZED", "colorized"),
    ("BLURRED", " blurred"),
    ("GRAYSCALE", "grayscale"),
    ("INVERT", "invert"),
    ("BINARY", "binary"),
)


# Create your models here.
class Upload(models.Model):
    image = models.ImageField(upload_to="images")
    action = models.CharField(max_length=50, choices=ACTION_CHOISES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.image)

    def save(self, *args, **kwargs):
        # open image
        pil_img = Image.open(self.image)

        # convert image to array and do some processing
        cv_img = np.array(pil_img)
        img = get_filtered_image(cv_img, self.action)

        # convert back to pil image
        im_pil = Image.fromarray(img)

        # save
        buffer = BytesIO()
        im_pil.save(buffer, format="png")
        image_png = buffer.getvalue()

        self.image.save(str(self.image), ContentFile(image_png), save=False)

        super().save(*args, **kwargs)
