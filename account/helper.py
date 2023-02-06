from django.contrib.auth.mixins import UserPassesTestMixin


class OnlyYouMixin(UserPassesTestMixin):
    login_url = 'account:login'

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk']


class GetOnlyYouMixin(UserPassesTestMixin):
    '''
    urlにpkが入らない場合はこちらをつかう
    '''
    login_url = 'account:login'

    def test_func(self):
        request_user = self.request.user
        cart_user = self.request.GET.get('uname', False)
        return request_user.username == cart_user


class PostOnlyYouMixin(UserPassesTestMixin):
    login_url = 'account:login'

    def test_func(self):
        request_user = self.request.user
        cart_user = self.request.POST.get('uname', False)
        return request_user.username == cart_user
