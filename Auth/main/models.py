from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone

# Create your models here.

class TravelExperience(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    visit_date = models.DateField()
    location = models.CharField(max_length=255)  # To be enhanced with map-based input (Leaflet.js)
    images = models.ImageField(upload_to='experience_images/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiences')
    source = models.URLField(blank=True, null=True)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
 

    
class HeritageSite(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Contribution(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    associated_site = models.ForeignKey(HeritageSite, on_delete=models.SET_NULL, null=True)
    media = models.FileField(upload_to='contribution_media/', blank=True, null=True)
    source = models.URLField(blank=True, null=True)
    contributor = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    verified = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.title
    
class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Food(models.Model):
    name = models.CharField(max_length=100)
    short_description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='food_images/', blank=True, null=True)
    tutorial_video_url = models.URLField(blank=True, null=True)  # YouTube or external video URL

    def __str__(self):
        return self.name

class Historical_Significance(models.Model):
    name=models.OneToOneField(Food, on_delete=models.CASCADE, primary_key=True)
    history=models.TextField(blank=True, null=True)
    cultural_significance=models.TextField(blank=True, null=True)

class OnlineBuying(models.Model):
    name = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='buying_links')
    product_url = models.URLField(blank=True, null=True)


    
class Recipe(models.Model):
    name = models.OneToOneField(Food, on_delete=models.CASCADE, primary_key=True)
    description = models.TextField(blank=True, null=True)
    prep_time = models.IntegerField(blank=True, null=True)
    servings = models.IntegerField(blank=True, null=True)
    ingredient_list = models.ManyToManyField(Ingredient, related_name="recipes") 
    instructions = models.TextField(blank=True, null=True)
    carbohydrate = models.TextField(blank=True, null=True)  
    protein = models.TextField(blank=True, null=True)  
    fat = models.TextField(blank=True, null=True)  
    calories = models.TextField(blank=True, null=True)  
    image=models.ImageField(upload_to='img', blank=True, null=True)
   


class Shop(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True, null=True)  
    maps_link = models.URLField(blank=True, null=True)  
    contact = models.CharField(max_length=20, blank=True, null=True)
    ingredients = models.ManyToManyField(Ingredient, related_name="shops")
    promocode=models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        
        return self.name
class OnlineShop(models.Model):
    name = models.CharField(max_length=100)  
    product_url = models.URLField(blank=True, null=True)  
    ingredient = models.ForeignKey(Ingredient, related_name="online_shops", on_delete=models.CASCADE)  

    def __str__(self):
        return f"{self.name} - {self.ingredient.name}"



class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True, null=True)  
    maps_link = models.URLField(blank=True, null=True)  
    contact = models.CharField(max_length=20, blank=True, null=True)
    food=models.ManyToManyField(Food, related_name="restaurants")

    def __str__(self):
        return self.name

class Sites(models.Model):
    name = models.CharField(max_length=100)
    photo1=models.ImageField(upload_to='img', blank=True, null=True)
    photo2=models.ImageField(upload_to='img', blank=True, null=True)
    photo3=models.ImageField(upload_to='img', blank=True, null=True)
    shortdescription=models.TextField(blank=True, null=True)
    description=models.TextField(blank=True, null=True)
    history=models.TextField(blank=True, null=True)
    cultural_significance=models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    