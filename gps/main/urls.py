from django.urls import path
from .views import (
    SignUpView, LoginView, User_SignUpView, User_LoginView, LogoutView, DashboardView, User_DashboardView,
    Register_LaptopView, Register_VehicleView, SetItemPinView, ModifyPinView, ValidateItemEntryView, 
    AuthenticateItemExitView, ItemReportView, LogSearchView, ResetPasswordView, ResetPasswordConfirmView
)
                   

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    
    path('user/signup/', User_SignUpView.as_view(), name='user-signup'),
    path('user/login/', User_LoginView.as_view(), name='user-login'),
    
    path('logout/', LogoutView.as_view(), name='logout'),
    
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('user/dashboard', User_DashboardView.as_view(), name='user-dashboard'),
    
    path('register/laptop/', Register_LaptopView.as_view(), name='register-laptop'),
    path('register/vehicle/', Register_VehicleView.as_view(), name='register-vehicle'),
    
    path('set/pin/', SetItemPinView.as_view(), name='set-item-pin'),
    path('modify/pin/', ModifyPinView.as_view(), name='modify-pin'),
    
    path('validate/item/entry/', ValidateItemEntryView.as_view(), name='validate-item-entry'),
    path('authenticate/item/exit/', AuthenticateItemExitView.as_view(), name='authenticate-item-exit'),
    
    path("item/report/", ItemReportView.as_view(), name="item-report"),
    
    path('log/', LogSearchView.as_view(), name='log-search'),
    
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('reset-password/<str:token>/', ResetPasswordConfirmView.as_view(), name='reset-password-confirm'),
    
]
