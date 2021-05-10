from my_receipts.apps.shops.models import Shop

from .models import Receipt


def add_receipt_by_id(user, parser_class, parser_kwargs=None):
    if parser_kwargs is None:
        parser_kwargs = {}
    parser = parser_class(**parser_kwargs)

    receipt = Receipt.objects.filter(vendor=parser.vendor, remote_id=parser.id).first()
    if receipt:
        return receipt

    shop, _ = Shop.all_objects.get_or_create(
        name=parser.shop_name,
        address=parser.shop_address,
        defaults={"itn": parser.shop_itn},
    )
    receipt = Receipt.objects.create(
        vendor=parser.vendor,
        remote_id=parser.id,
        user=user,
        shop=shop,
        number=parser.receipt_number,
        shift=parser.shift,
        cashier=parser.cashier,
        created_in_receipt=parser.receipt_created_dt,
        sum=parser.receipt_sum,
    )
    for order, item in enumerate(parser.items):
        receipt.add_item(
            item_name=item.name,
            price=item.price,
            amount=item.amount,
            sum=item.sum,
            order=order,
        )

    return receipt
