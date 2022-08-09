from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os

def rename_profile_pic(instance, filename):
    file_base, file_extension = os.path.splitext(filename)
    return f'profile_pics/{instance.user.username + file_extension}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    image = models.ImageField(default='default.jpg', upload_to=rename_profile_pic)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
    
    def set_default_image(self):
        self.user.profile.image.delete(save=False)
        self.user.profile.image = 'default.jpg'
        self.user.profile.save()
