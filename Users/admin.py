from django.contrib import admin

from Users.models import Block, userRegisteredTable

# Register your models here.
admin.site.register(userRegisteredTable)
admin.site.register(Block)