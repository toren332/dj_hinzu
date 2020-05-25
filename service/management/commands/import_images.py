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

        models.Embed.objects.all().delete()
        film_files = glob.glob(os.path.join('media/movies', "*.jpg"))
        for n, image in enumerate(film_files):
            network = torch_models.densenet121(pretrained=True)
            model = nn.Sequential(network.features, nn.AvgPool2d(7, stride=1))
            model.train(False)
            preprocess = transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ])
            print(f'{n}|{len(film_files)}')
            input_image = Image.open(image).convert('RGB')

            embed = model(preprocess(input_image).unsqueeze(0)).squeeze(-1).squeeze(-1)
            film_name = image.split('/')[-1].split('_')[0]
            models.Embed.objects.create(**{
                'film_name': film_name,
                'vector': embed.tolist()[0],
                'image': image[5:],
            })