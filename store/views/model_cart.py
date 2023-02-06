from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.cache import never_cache
from django.views.generic.edit import ModelFormMixin

from account.helper import OnlyYouMixin, PostOnlyYouMixin
from account.models import User
from book.models import Book
from store.models import CartUnit
from store.forms import CartUnitForm


@method_decorator(never_cache, name='dispatch')
class ModelCartContent(OnlyYouMixin, generic.DetailView):
    model = User
    context_object_name = 'cart'
    template_name = 'store/cart/contents.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        return obj.cart


class ModelAddToCart(LoginRequiredMixin, generic.RedirectView):
    """CartUnitをカートに追加する。
    どのユーザのカートの追加するかは、サーバ側で決定しているので、OnlyYouMixinはいらない
    """

    def get_redirect_url(self):
        user_pk = self.request.user.pk
        return reverse_lazy('store:modelcart_content', args=(user_pk,))

    def post(self, request, *args, **kwargs):
        user = request.user
        book_pk = request.POST['book_pk']
        quantity = request.POST['quantity']
        user.cart.add_unit(CartUnit(book=Book.objects.get(pk=book_pk), quantity=int(quantity)))
        return super().post(request, *args, **kwargs)


class ModelCartDelete(PostOnlyYouMixin, generic.DeleteView):
    """
    CartUnitをカートに追加する。
    """
    model = CartUnit

    def get_object(self, queryset=None):
        unit_pk = self.request.POST['unit_pk']
        return CartUnit.objects.get(id=unit_pk)

    def get_success_url(self):
        user_pk = self.request.user.pk
        return reverse_lazy('store:modelcart_content', args=(user_pk,))
