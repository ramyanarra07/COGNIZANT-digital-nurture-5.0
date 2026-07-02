from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),  # Make sure this line exists and isn't commented out
    # ... your other app routes ...
]