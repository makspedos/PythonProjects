from .models import Basket

def getting_basket_info(request):
    session_key = request.session.session_key
    if not session_key:
        request.session["session_key"]=123
        request.session.cycle_key()

    products_in_basket = Basket.objects.filter(session_key=session_key, is_active=True)
    product_total_count = products_in_basket.count()

    return locals()