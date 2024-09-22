from django.urls import path
from craftapp import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm, MyPasswordResetForm , MyPasswordChangeForm, MySetPasswordForm

urlpatterns = [
    path("", views.home),
    path("about", views.about),
    path("contact", views.contact),
    # path("category/<slug:val>", views.CategoryView.as_view(),name="category"),
    path("category<slug:val>", views.category, name="category"),
    path("pd<int:pk>", views.proddetails.as_view(),name="pd"),
    path("category-title<val>", views.categorytitle),
    path("profile", views.ProfileView.as_view()),
    path("address", views.address),
    path("Updateaddress<int:pk>", views.updateAddress.as_view()),
    path('logout', views.user_logout),
    path("add-to-cart", views.add_to_cart),
    path("cart", views.show_cart,name='cart'),
    path("checkout", views.checkout.as_view()),
    path("paymentdone", views.payment_done),
    path("orders", views.orders),
    path("search", views.search),
    # path("removecart", views.remove_cart),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    


    #login authentication
    path("registration", views.CustomerRegistration.as_view()),
    path("login", auth_view.LoginView.as_view(template_name='app/login.html',
    authentication_form=LoginForm)),
    path("passwordchange", auth_view.PasswordChangeView.as_view(template_name='app/changepassword.html',
    form_class=MyPasswordChangeForm, success_url='/passwordchangedone'), name='passwordchange'),
    path('passwordchangedone', auth_view.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),
    

    path('password_reset', auth_view.PasswordResetView.as_view(template_name='app/password_reset.html', 
    form_class=MyPasswordResetForm) , name='password_reset'),

    path('password-reset/done', auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>', auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=MySetPasswordForm ) , name='password_reset_confirm'),

    path('password-reset-complete',auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'),name='password_reset_complete'),




]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)