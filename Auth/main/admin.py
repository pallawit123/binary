from django.contrib import admin
from .models import *
from .models import Category, Tag, Event, EventGallery

admin.site.register(HeritageSite)
admin.site.register(Contribution)
admin.site.register(TravelExperience)
admin.site.register(Recipe)
admin.site.register(Shop)
admin.site.register(OnlineShop)
admin.site.register(Restaurant)
admin.site.register(Ingredient)
admin.site.register(Food)
admin.site.register(Historical_Significance)
admin.site.register(OnlineBuying)
admin.site.register(Sites)



#Events
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Event)
admin.site.register(EventGallery)

