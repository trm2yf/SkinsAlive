from django.contrib import admin

# Register your models here.
from sprint1.models import Document, Bulletin, Folder

admin.site.register(Document)
admin.site.register(Bulletin)
admin.site.register(Folder)
