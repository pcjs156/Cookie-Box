from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import mainApp.urls
import accountApp.urls
import blogApp.urls
import mailingApp.urls

from mainApp.views import main_view

include_url_patterns = [
    path('', include(mainApp.urls)),
    path('account/', include(accountApp.urls)),
    path('blog/', include(blogApp.urls)),
    path('mailing/', include(mailingApp.urls)),
    path('ckeditor/', include('ckeditor_uploader.urls')),  # CKEditor 기본 url
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_view, name="main"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += include_url_patterns