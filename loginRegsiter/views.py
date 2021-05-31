from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from loginRegsiter.forms import CreateUserForm
from loginRegsiter.models import Product, BidDetail
from django.core.paginator import Paginator
from background_task import background
from datetime import datetime


@background(schedule=2)
def demo():
    product = Product.objects.filter(date__lt=datetime.now())
    for each in product:
        Product.objects.filter(id=each.id).update(publish=False)


demo()


def home(request):
    if request.method == "POST":
        search_text = request.POST.get("search_text")
        product_li = Product.objects.filter(product_name__istartswith=search_text)
        paginator = Paginator(product_li, 6)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        if page_obj.has_next():
            next_url = f'?page={page_obj.next_page_number()}'
        else:
            next_url = ''
        if page_obj.has_previous():
            prev_url = f'?page={page_obj.previous_page_number()}'
        else:
            prev_url = ''
        return render(request, 'home.html', {'page_obj': page_obj, 'next_url': next_url, 'prev_url': prev_url})

    product_li = Product.objects.all()
    paginator = Paginator(product_li, 6)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    if page_obj.has_next():
        next_url = f'?page={page_obj.next_page_number()}'
    else:
        next_url = ''
    if page_obj.has_previous():
        prev_url = f'?page={page_obj.previous_page_number()}'
    else:
        prev_url = ''

    return render(request, 'home.html', {'page_obj': page_obj, 'next_url': next_url, 'prev_url': prev_url})


def product_dis(request, id):
    particular_product = Product.objects.filter(id=id)[0]
    if request.user.id:
        check_post_product_user = Product.objects.filter(product_owner=request.user)
        error_bid_price = None
        if request.method == "POST":
            bid_product = particular_product
            bid_price = request.POST.get('bid_price')
            bid_user = request.user
            print(bid_price)
            print(particular_product.product_price)
            if bid_price < particular_product.product_price:
                error_bid_price = 'Bid amount should be greater than Minimum Price!!'
                return render(request, 'Product Detail/Product_dis.html', {'particular_product': particular_product,
                                                                           'error_bid_price': error_bid_price})
            BidDetail(bid_product=bid_product, bid_price=bid_price, bid_user=bid_user).save()
            pass
        error = None
        if check_post_product_user:
            for each in check_post_product_user:
                if each.id == id:
                    error = 'You post this product!!'
                    return render(request, 'Product Detail/Product_dis.html',
                                  {'particular_product': particular_product, 'error': error})
        check_bid = BidDetail.objects.filter(bid_user=request.user, bid_product=particular_product)
        return render(request, 'Product Detail/Product_dis.html',
                      {'particular_product': particular_product, 'check_bid': check_bid})
    else:
        return render(request, 'Product Detail/Product_dis.html', {'particular_product': particular_product})


def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        get_email = request.POST.get('email')
        check_email = User.objects.filter(email=get_email)
        error_message = None
        if check_email:
            error_message = "Email is already exist!!"
            return render(request, 'login_register/register.html', {'form': form, 'error_message': error_message})

        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            return redirect('loginpage')
    return render(request, 'login_register/register.html', {'form': form})


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            user = request.user
            return redirect(home)
        else:
            error_message = "Username of password not match!!"
            return render(request, 'login_register/login.html', {'error_message': error_message})

    return render(request, 'login_register/login.html')


def logout_page(request):
    logout(request)
    return redirect(home)



