# from django.contrib.auth.views import LoginView, LogoutView
import urllib.parse

from django.contrib.auth import login, views as auth_v
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic

from account.forms import SignupForm
from account.models import Cart, User
from store.helper import SessionCartManager


class Login(auth_v.LoginView):
    template_name = 'account/login.html'

    def get_success_url(self):
        """
        まずsessionカートの内容をモデルに移す
        このメソッドはログインが成功したときしか呼ばれない
        success_url: home or purchase -> store:home or store:purchase_preveiw
        """
        try:
            session_cart = self.request.session[SessionCartManager.kname]
            self.request.user.cart.import_session(session_cart)
            del self.request.session[SessionCartManager.kname]
        except KeyError:
            return reverse_lazy('store:home')

        next_page = self.request.GET.get('next_page', 'home')
        print(next_page)
        if next_page == 'purchase':
            next_url = reverse_lazy('store:purchase_preview') + '?' + urllib.parse.urlencode(
                {'uname': self.request.user.username})
            return next_url
        else:
            return reverse_lazy('store:home')


class Logout(auth_v.LogoutView):
    next_page = reverse_lazy('store:home')


class SignUp(generic.CreateView):
    template_name = 'account/signup.html'
    model = User
    form_class = SignupForm
    success_url = reverse_lazy('account:signupdone')

    def form_valid(self, form):
        # ユーザ・カート作成
        new_user = form.save(commit=False)
        new_user.cart = Cart.objects.create()
        new_user.save()

        next_page = self.request.GET.get('next_page', 'home')
        if next_page == 'purchase':
            session_cart = self.request.session[SessionCartManager.kname]

            login(self.request, new_user)

            new_user.cart.import_session(session_cart)
            del self.request.session[SessionCartManager.kname]

            next_url = reverse_lazy('store:purchase_preview') + '?' + urllib.parse.urlencode(
                {'uname': new_user.username})
            return HttpResponseRedirect(next_url)
        else:
            return HttpResponseRedirect(self.success_url)


class SignUpDone(generic.TemplateView):
    template_name = 'account/signupdone.html'
