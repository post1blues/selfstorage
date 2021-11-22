from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout

from tempfile import TemporaryFile
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils.encoding import force_text
import qrcode

from selfstorage.models import StorageOrder, SeasonOrder, Payment
from users.forms import CustomUserCreationForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('index')
    template_name = 'users/signup.html'

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            is_ordered = False

            if request.session.get('current_order_id') and request.session.get('order_type') == 'box-rent':
                order = StorageOrder.objects.get(id=request.session.get('current_order_id'))
                order.customer = user
                order.save()
                is_ordered = True
            elif request.session.get('current_order_id') and request.session.get('order_type') == 'season-rent':
                order = SeasonOrder.objects.get(id=request.session.get('current_order_id'))
                order.customer = user
                order.save()
                is_ordered = True

            new_user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],
                )
            login(request, new_user)

            if is_ordered:
                return redirect('payment')

            return redirect('index')
        else:
            return render(request, self.template_name, {'form': form})


class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('profile')
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        user = authenticate(
            email=request.POST['username'],
            password=request.POST['password']
        )

        if user:
            login(request, user)

            if request.session.get('current_order_id') and request.session.get('order_type') == 'box-rent':
                order = StorageOrder.objects.get(id=request.session.get('current_order_id'))
                order.customer = user
                order.save()
                return redirect('payment')
            elif request.session.get('current_order_id') and request.session.get('order_type') == 'season-rent':
                order = SeasonOrder.objects.get(id=request.session.get('current_order_id'))
                order.customer = user
                order.save()
                return redirect('payment')
            return redirect('profile')

        return redirect('login')


@login_required(login_url='/login/')
def profile(request):
    current_user = request.user
    storage_orders = StorageOrder.objects.filter(customer=current_user)
    season_orders = SeasonOrder.objects.filter(customer=current_user)
    return render(request, 'users/profile.html', {'current_user': current_user, 'storage_orders': storage_orders, 'season_orders': season_orders})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required(login_url='/login/')
def payment(request):
    is_ordered = False
    if request.session.get('current_order_id') and request.session.get('order_type') == 'box-rent':
        order = StorageOrder.objects.get(id=request.session.get('current_order_id'))
        is_ordered = True
    elif request.session.get('current_order_id') and request.session.get('order_type') == 'season-rent':
        order = SeasonOrder.objects.get(id=request.session.get('current_order_id'))
        is_ordered = True

    if not is_ordered:
        return redirect('index')

    if request.POST:
        card_number = request.POST.get('card_number')
        payment = Payment(
            card_number=card_number,
            price=order.price,
            is_success=True
        )
        payment.save()
        order.payment = payment
        order.save()
        return redirect('payment_done')

    context = {'order': order}

    return render(request, 'users/payment.html', context)


@login_required(login_url='/login/')
def payment_done(request):
    request.session.pop('order_type', None)
    request.session.pop('current_order_id', None)
    return render(request, 'users/payment_done.html')
