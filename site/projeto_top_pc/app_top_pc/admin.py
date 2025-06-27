from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Produto)
# Removed registration of undefined models LinkComponente and EstatisticaComponente
