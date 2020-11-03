from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import mainApp.urls
import accountApp.urls
import blogApp.urls
import mailingApp.urls

from mainApp.views import intro_view

from mailingApp.scheduler import EmailScheduler

include_url_patterns = [
    path('', include(mainApp.urls)),
    path('account/', include(accountApp.urls)),
    path('blog/', include(blogApp.urls)),
    path('mailing/', include(mailingApp.urls)),
    path('ckeditor/', include('ckeditor_uploader.urls')),  # CKEditor 기본 url
]

urlpatterns = [
    path('', intro_view, name="intro"),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += include_url_patterns

scheduler = EmailScheduler()
scheduler.run(19, 32)