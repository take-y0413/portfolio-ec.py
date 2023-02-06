from book.models import Book


class SessionCartManager:
    """
    Session Cartの構造: [{'book_pk':foo, 'quantity': bar }, {}, ・・・]
    """
    kname = 'cart'  # key name

    @staticmethod
    def _make_unit(book_pk, quantity=1):
        return {'book_pk': int(book_pk), 'quantity': int(quantity)}

    @staticmethod
    def add_unit(lis_cart, book_pk, quantity=1):
        book_pk = int(book_pk)
        quantity = int(quantity)
        for cart_unit in lis_cart:
            if cart_unit['book_pk'] == int(book_pk):
                cart_unit['quantity'] += quantity
                return lis_cart
        lis_cart.append(SessionCartManager._make_unit(book_pk, quantity))
        return lis_cart

    @staticmethod
    def delete_unit(lis_cart, book_pk):
        book_pk = int(book_pk)
        for cart_unit in lis_cart:
            if cart_unit['book_pk'] == book_pk:
                lis_cart.remove(cart_unit)
        return lis_cart

    @staticmethod
    def to_rendered(lis_cart):
        """
        templateが必要とする情報にフォーマットする。（このメソッドが返すものをコンテキストに追加すればよい）
        """
        return [{'book': Book.objects.get(pk=cart_unit['book_pk']).title,
                 'quantity': cart_unit['quantity'],
                 'book_pk': cart_unit['book_pk']}
                for cart_unit in lis_cart]
