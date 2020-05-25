from django.contrib import admin
from service import models
from django.utils.html import format_html


@admin.register(models.Embed)
class EmbedAdmin(admin.ModelAdmin):
    list_display = ['id', 'film_name', 'image_tag']

    def image_tag(self, obj):
        return format_html('<img height="100" src="{}" />'.format(obj.image.url))


@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.Image._meta.get_fields()]
    list_display.pop(list_display.index('embed'))

    list_display.append('image_tag')
    list_display.append('embed_img')

    def image_tag(self, obj):
        return format_html('<img height="100" src="{}" />'.format(obj.image.url))

    def embed_img(self, obj):
        return format_html('<img height="100" src="{}" />'.format(obj.embed.image.url))