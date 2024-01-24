from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:pk>/',views.details_vehicle),
    path('vehicles',views.vehicles),
    path('driver_register/',views.driver_registration, name='driver_registration'),
    path('login',views.login,name='login'),
    path('view_license/<int:id>/', views.view_license, name='view_license'),
    path('services',views.services),
    path('user_home',views.user_home),
    path('logout/', views.logout_view, name='logout'),
    path('driver_home',views.driver_home),
    path('add_vehicle',views.add_vehicle),
    path('delete_vehicle/<int:id>/',views.delete_vehicle),
    path('filter/<int:fid>/',views.filter),
    path('drivers',views.view_drivers),
    path('search_vehicles',views.search_vehicles,name='search_vehicles'),
    path('book_vehicle/<int:vehicle_id>/',views.book_vehicle),
    path('viewbookings',views.view_booking),
    path('mybookings',views.my_booking),
    path('stats',views.view_stats),
    path('make_payment/<int:booking_id>/', views.make_payment, name='make_payment'),
    path('edit-user',views.edituser),
    path('changep-user',views.changepassword_user),
    path('edit-driver',views.editdriver),
    path('changep-driver',views.changepassword_driver),
    path('uview_drivervehicle/<int:did>/',views.view_driver_vehicles)
]
    

