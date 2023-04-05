from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("account/new/", views.register_new_account),
    path("account/<str:user_id>", views.get_account_details),
    path('account/login/', obtain_auth_token),
    # path("account/login/", views.login_account),
    path('account/deposit/<str:user_id>', views.deposit_amount),
    path('account/transfer/<str:from_user_id>', views.transfer_amount),
    path('account/admin/', views.add_or_deduct)
]
