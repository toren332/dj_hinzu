from django.db import models
from django.contrib.postgres.fields import ArrayField
from PIL import Image as PILImage
from torchvision import transforms
from torchvision import models as torch_models
import torch.nn as nn
import numpy as np
from scipy import spatial

class Embed(models.Model):
    image = models.ImageField(upload_to="movies/")
    film_name = models.CharField(max_length=256)
    vector = ArrayField(models.FloatField())


class Image(models.Model):
    image = models.ImageField(upload_to="images/")
    embed = models.ForeignKey(Embed, on_delete=models.CASCADE, blank=True, null=True, related_name='image_embed')

    def save(self, *args, **kwargs):
        network = torch_models.densenet121(pretrained=True)
        model = nn.Sequential(network.features, nn.AvgPool2d(7, stride=1))
        model.train(False)
        preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        try:
            input_image = PILImage.open(f'media{self.image}').convert('RGB')
        except:
            super().save(*args, **kwargs)
            input_image = PILImage.open(f'media/{self.image}').convert('RGB')

        vector1 = np.array(model(preprocess(input_image).unsqueeze(0)).squeeze(-1).squeeze(-1).tolist()[0])
        l = []
        len_ = len(Embed.objects.all())
        for n, embed in enumerate(Embed.objects.all()):
            # print(n, len_)
            vector2 = np.array(embed.vector)
            result = 1 - spatial.distance.cosine(vector1, vector2)
            l.append({
                'id': embed.id,
                'similarity': result,
            })
        l = sorted(l, key=lambda i: i['similarity'],reverse=True)
        embed = Embed.objects.get(pk=l[0]['id'])
        self.embed = embed
        super().save(*args, **kwargs)  # Call the "real" save() method.