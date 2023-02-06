from django import forms
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.cache import never_cache

from store.helper import SessionCartManager


@method_decorator(never_cache, name='dispatch')
class SessionCartContent(generic.TemplateView):
    template_name = 'store/cart/contents.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        cart = self.request.session.get(SessionCartManager.kname, [])
        ctx['lis_cart'] = SessionCartManager.to_rendered(cart)
        return ctx


class SessionAddToCart(generic.RedirectView):
    url = reverse_lazy('store:sessioncart_content')

    def post(self, request, *args, **kwargs):
        book_pk = request.POST['book_pk']
        quantity = request.POST['quantity']
        cart = request.session.get(SessionCartManager.kname, [])
        cart = SessionCartManager.add_unit(cart, book_pk, quantity)
        request.session[SessionCartManager.kname] = cart
        return super().post(request, *args, **kwargs)


class SessionCartDelete(generic.FormView):
    form_class = forms.Form
    success_url = reverse_lazy('store:sessioncart_content')

    def form_valid(self, form):
        cart = self.request.session[SessionCartManager.kname]
        deleting_book_pk = int(self.request.POST['book_pk'])
        cart = SessionCartManager.delete_unit(cart, deleting_book_pk)
        self.request.session[SessionCartManager.kname] = cart
        return super().form_valid(form)
