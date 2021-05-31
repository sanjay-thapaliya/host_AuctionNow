from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.shortcuts import render
from loginRegsiter.models import Product, BidDetail
from django.core.mail import send_mail

@login_required(login_url='loginpage')
def dashboard_home(request):
    posted_products = Product.objects.filter(product_owner=request.user)
    if request.method == "POST":
        product_name = request.POST.get("product_name")
        product_price = request.POST.get("product_price")
        product_detail = request.POST.get("product_detail")
        product_image = request.FILES.get("product_image")
        date = request.POST.get("date")
        error_message = None
        if not product_name:
            error_message = 'Must contain Product name'
        elif not product_price:
            error_message = 'Must contain Product price'
        elif not product_detail:
            error_message = 'Must contain Product detail information'
        elif not product_image:
            error_message = 'Must contain Image'
        elif not date:
            error_message = 'Must contain date'
        if error_message:
            return render(request, 'user_dashboard/dashboard.html', {'error_message': error_message, 'posted_products': posted_products})
        Product.objects.create(product_owner=request.user, product_name=product_name, product_detail=product_detail,
                               product_price=product_price, product_image=product_image, date=date)
        pass
    # posted_products = Product.objects.filter(product_owner=request.user)
    print(request.user.id)
    return render(request, 'user_dashboard/dashboard.html', {'posted_products': posted_products})


# product = Product.objects.filter(publish=False)
# print(product)
# if product:
#     for each in product:
#         bid_detail = BidDetail.objects.filter(bid_product=each).aggregate(Max('bid_price'))
#         print(bid_detail)
#         winner_price = bid_detail["bid_price__max"]
#         winner_user = BidDetail.objects.filter(bid_price=winner_price)
#         for n in winner_user:
#             print('winner:' + n.bid_user.email)
#             print('Winner bid price::' + n.bid_price)
#             print('product owner:' + n.bid_product.product_owner.email)
#             print('Ask price:' + n.bid_product.product_price)
#
#             send_mail(
#                 'Congratulation !!!',
#                 'You have own the bet for: ' + n.bid_product.product_name + '\n' + 'Product owner: ' + n.bid_product.product_owner.email + '\n' + 'Please contact soon as possible!!',
#                 'sanjay@gmail.com',
#                 [n.bid_user.email],
#                 fail_silently=False,
#             )
#             send_mail(
#                 'Congratulation you got bid owner for your product!!!',
#                 'Your Product: ' + n.bid_product.product_name + '\n' 'Bid Price:' + n.bid_price + '\n' + 'Winner: ' + n.bid_user.email + '\n' + 'Please contact soon as possible!!',
#                 'sanjay@gmail.com',
#                 [n.bid_product.product_owner.email],
#                 fail_silently=False,
#             )
#             break
#

