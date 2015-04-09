from django.contrib import admin

# Register your models here.
from sprint1.models import Document, Skin, Folder, Author

admin.site.register(Document)
admin.site.register(Skin)
admin.site.register(Folder)
admin.site.register(Author)
