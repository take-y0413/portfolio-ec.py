from django.views import generic
from django.views.generic.edit import ModelFormMixin

from book.models import Book
from store.forms import CartUnitForm


class BookDetail(ModelFormMixin, generic.DetailView):
    model = Book
    template_name = 'book/detail.html'
    context_object_name = 'book'
    form_class = CartUnitForm

    def form_valid(self, form):
        return render(self.request, 'book/detail.html', {'form': form})
