from django.urls import path
from main.views import show_main, create_menu_item, show_xml, show_json, show_xml_by_id, show_json_by_id, register, login_user, logout_user

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-menu-item', create_menu_item, name='create_menu_item'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]