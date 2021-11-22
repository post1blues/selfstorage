from django.urls import path, include

from users.views import SignUpView, CustomLoginView, profile, payment, payment_done

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', profile, name='profile'),
    path('payment/', payment, name='payment'),
    path('payment_done/', payment_done, name='payment_done'),
    path('', include('django.contrib.auth.urls')),
]