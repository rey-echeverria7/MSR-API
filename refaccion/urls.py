from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from refaccion import views

#api versioning
router = routers.DefaultRouter()
router.register(r'refacciones',views.RefaccionViewSet, basename='refacciones')


#Defining URLs automatically 
urlpatterns = [
    path("api/v1/", include(router.urls) ), #GENERATES GET, POST, PUT , DELETE
    path("docs/", include_docs_urls(title="MSR-API"))
]
