import os, glob
import shutil
from django.core.management.base import BaseCommand



class Command(BaseCommand):
    def handle(self, *args, **options):
        if not os.path.exists(f'media/movies'):
            os.makedirs(f'media/movies')
        film_files = glob.glob(os.path.join("images 2/", "*.jpg"))
        for n, image in enumerate(film_files):
            print(f'{n+1}|{len(film_files)}')
            film_name = image.split('/')[-1].split('$')[0]
            shutil.copy(image, f'media/movies/{film_name}_{n}.jpg')

