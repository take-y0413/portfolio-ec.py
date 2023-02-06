from django import forms
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.cache import never_cache
from account.models import Purchase

from account.helper import GetOnlyYouMixin, PostOnlyYouMixin


@method_decorator(never_cache, name='dispatch')
class PurchasePreview(GetOnlyYouMixin, generic.TemplateView):
    template_name = 'store/purchase/preview.html'

    def get_context_data(self, **kwargs):
        cart = self.request.user.cart
        ctx = super().get_context_data(**kwargs)
        ctx['total_price'] = cart.total_price
        return ctx


@method_decorator(never_cache, name='dispatch')
class PurchaseProcess(PostOnlyYouMixin, generic.FormView):
    """
    TemplateView ではpostは未実装。
    djangoのformは使わない
    """
    form_class = forms.Form
    success_url = reverse_lazy('store:purchase_done')

    def form_valid(self, form):
        user = self.request.user

        for unit in user.cart.units.all():
            Purchase.objects.create(fk_user=user, fk_book=unit.book, purchase_num=unit.quantity)
        user.cart.units.clear()
        return super().form_valid(form)

class PurchaseDone(generic.TemplateView):
    template_name = 'store/purchase/done.html'
