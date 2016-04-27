from django.contrib import admin
from . import models


class CorpusDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'answer', 'owner')
    search_fields = ('question',  'answer', 'owner')
    fields = ('question',  'answer', 'owner')
    list_per_page = 100
    actions_on_top = True
    actions_on_bottom = False
    actions_selection_counter = False
    
admin.site.register(models.CorpusData, CorpusDataAdmin)

# Register your models here.
admin.site.register(models.Robot)
admin.site.register(models.AccountProfile)
