import views
from django.contrib import admin
from django.urls import path
from views import home, login_page, signup, history, about, result, logout_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('login/', login_page),
    path('signup/', signup),
    path('logout/', logout_view),
    path('history/', history),
    path('about/', about),
    path('result/', result),
    path('scan/<int:id>/', views.scan_detail),
    path('export/', views.export_results),
    path('forgot-password/', views.forgot_password),
    path('delete-all/', views.delete_all_results),
    path('delete/<int:id>/', views.delete_result),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)