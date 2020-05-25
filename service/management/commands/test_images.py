import glob
import os
from django.core.management.base import BaseCommand
from PIL import Image
from torchvision import transforms
from torchvision import models as torch_models
import torch.nn as nn

from service import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        models.Image.objects.all().delete()
        photo_files = glob.glob(os.path.join('media/images', "*.JPG"))
        print(photo_files)
        for n, image in enumerate(photo_files):
            print(f'{n}|{len(photo_files)}')
            models.Image.objects.create(**{
                'image': image[5:],
            })
            # print(film_name,)