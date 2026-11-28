from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("apps.users.auth.urls")),
    path("api/users/",include("apps.users.urls")),
    path("api/",include("apps.tasks.urls")),
    
    path("", include("apps.dashboard.urls")),
    path("planner/", include("apps.planner.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
