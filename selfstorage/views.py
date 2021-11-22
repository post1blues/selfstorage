from django.shortcuts import render, redirect
from django.utils import timezone

from selfstorage.models import Storage, Box, Payment, StorageOrder, SeasonOrder, SeasonService
from users.forms import CustomUserCreationForm


def index(request):
    storages = Storage.objects.all()
    boxes = Box.objects.all().order_by('size')

    context = {'storages': storages, 'boxes': boxes,}
    return render(request, 'selfstorage/index.html', context)


def season_storage(request):
    storages = Storage.objects.all()
    services = SeasonService.objects.all()

    context = {'storages': storages, 'services': services, }
    return render(request, 'selfstorage/season_storage.html', context)


def order(request):
    if request.POST:
        if request.POST.get('rent-type') == 'box-rent':
            months = request.POST['rent_time']
            days = int(months) * 30
            end_date = timezone.now() + timezone.timedelta(days=days)
            storage = Storage.objects.get(id=int(request.POST.get('storage')))
            box = Box.objects.get(id=int(request.POST.get('box')))
            price = (storage.price + box.price) * int(months)
            new_order = StorageOrder(
                storage=storage,
                box=box,
                end_of_storage=end_date,
                price=price
            )

            try:
                new_order.save()
            except:
                return redirect('index')

            current_order_id = new_order.id
            request.session['current_order_id'] = current_order_id
            request.session['order_type'] = 'box-rent'

        if request.POST.get('rent-type') == 'season-rent':
            months = request.POST['rent_time']
            days = int(months) * 30
            end_date = timezone.now() + timezone.timedelta(days=days)
            storage = Storage.objects.get(id=int(request.POST.get('storage')))
            season_product = SeasonService.objects.get(id=int(request.POST.get('service')))
            price = (season_product.price_per_month + storage.price) * int(months)
            new_order = SeasonOrder(
                season_product=season_product,
                storage=storage,
                end_of_storage=end_date,
                price=price
            )

            try:
                new_order.save()
            except:
                return redirect('index')

            current_order_id = new_order.id
            request.session['current_order_id'] = current_order_id
            request.session['order_type'] = 'season-rent'

        if not request.user.is_authenticated:
            return redirect('signup')
        new_order.customer = request.user
        new_order.save()
        return redirect('payment')
    return redirect('index')


def about(request):
    return render(request, 'selfstorage/aboutus.html')


def contact(request):
    return render(request, 'selfstorage/contactus.html')

