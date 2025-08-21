from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Pizza Ordering API",
      default_version='v1',
      description="API for creating, updating, deleting pizza orders and viewing the menu",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   url=None,  # 👈 Important: let drf-yasg detect request host (works in Codespaces)
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('orders/', include('orders.urls')),  # orders app contains /orders and /menu

    # API docs
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-ui'),
]
