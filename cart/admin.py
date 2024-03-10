from django.contrib import admin
from . import models as m_
# Register your models here.
admin.site.register(m_.Cart)
admin.site.register(m_.CartItem)