from django.urls import path
from . import views


urlpatterns = [
    path('', views.upload_file, name='upload_file'),
    path('calc/csv/<str:name_file>', views.calc, name='calc'),
    path('download_csv/', views.download_csv, name='download_csv'),
    path('<str:status_file>', views.upload_file, name='file_false'),
    # path('select_columns/csv/<str:name_file>', views.select_columns, name='select_columns'),
]
