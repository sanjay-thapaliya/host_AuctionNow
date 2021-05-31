from django.core.mail import send_mail
from django.db.models import Max

from loginRegsiter.models import Product, BidDetail


def my_scheduled_job():
    product = Product.objects.filter(publish=False)
    if product:
        for each in product:
            bid_detail = BidDetail.objects.filter(bid_product=each).aggregate(Max('bid_price'))
            winner_price = bid_detail["bid_price__max"]
            winner_user = BidDetail.objects.filter(bid_price=winner_price)
            for n in winner_user:
                send_mail(
                    'Congratulation !!!',
                    'You have own the bet for: ' + n.bid_product.product_name + '\n' + 'Product owner: ' + n.bid_product.product_owner.email + '\n' + 'Please contact soon as possible!!',
                    'AuctionNow Team <info@ggic.com.np>',
                    [n.bid_user.email],
                    fail_silently=False,
                )
                send_mail(
                    'Congratulation you got bid owner for your product!!!',
                    'Your Product: ' + n.bid_product.product_name + '\n' 'Bid Price:' + n.bid_price + '\n' + 'Winner: ' + n.bid_user.email + '\n' + 'Please contact soon as possible!!',
                    'AuctionNow Team <info@ggic.com.np>',
                    [n.bid_product.product_owner.email],
                    fail_silently=False,
                )
                Product.objects.filter(id=n.bid_product.id).delete()
            if not winner_user:
                send_mail(
                    'Sorry (Try again)',
                    'Sorry nobody bid for you product.',
                    'AuctionNow Team <info@ggic.com.np>',
                    [each.product_owner.email],
                    fail_silently=False,
                )
                Product.objects.filter(id=each.id).delete()

                break
