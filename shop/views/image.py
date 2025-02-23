from django.http import HttpResponse
from ..models import Image


def images(_, image_id):
    image = Image.objects.get(id=image_id)
    response = HttpResponse(image.data, content_type=image.mimetype)
    response["Cache-Control"] = "max-age=3600, public"
    return response