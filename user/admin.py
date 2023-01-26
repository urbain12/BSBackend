from django.contrib import admin
from .models import *
from .form import *
# Register your models here.

from django.contrib import admin
from .models import *
class VaccineCreateAdmin(admin.ModelAdmin):
   list_display = ['id','user','Vaxtype', 'Vaxplace','KG', 'added_at']
   form = VaccineCreateForm
   search_fields = ['Vaxtype','Vaxplace']
# Register your models here.
admin.site.register(User)
admin.site.register(Guide)
admin.site.register(Queries)
admin.site.register(Vaccines,VaccineCreateAdmin)