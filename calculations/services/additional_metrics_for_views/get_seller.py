from users.models import Shop, Seller

def get_seller_and_current_shop(username) -> tuple:
    user_id = username.id
    try:
        shop_0 = Shop.objects.get(client_id=0)
    except:
        shop_0 = Shop.objects.create(client_id=0, api_key='null', user_id=None)
    try:
        seller = Seller.objects.get(user_id=user_id)
    except:
        seller = Seller.objects.create(user_id=user_id, current_shop=0)
    try:
        print(f'current_shop: {seller.current_shop}')
        shop = Shop.objects.get(client_id=seller.current_shop)
    except:
        shop = shop_0

    return seller, shop