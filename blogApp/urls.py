from django.urls import path

from . import views

urlpatterns = [
    path('category/<int:category_id>', views.category_view, name="category"),
    path('message_to_creator/<int:creator_id>',
         views.message_to_creator_view,
         name="message_to_creator"),
    path('webzine_create/', views.webzine_create_view, name="webzine_create"),
    path('webzine_detail/<int:webzine_id>',
         views.webzine_detail_view,
         name="webzine_detail"),
    path('webzine_edit/<int:webzine_id>',
         views.webzine_edit_view,
         name="webzine_edit"),
    path('webzine_list_by_category/<int:category_id>',
         views.webzine_list_by_category_view,
         name="webzine_list_by_category"),
    path('webzine_user_list/<int:creator_id>',
         views.webzine_user_list_view,
         name="webzine_user_list"),
]
