from django.views import generic

from book.models import Book
from store.forms import BookSearchForm


class Home(generic.ListView):
    model = Book
    template_name = 'store/home.html'
    form_class = BookSearchForm
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(generic.ListView, self).get_context_data(**kwargs)
        context.update(dict(form=self.form_class, query_string=self.request.GET.urlencode()))

        q_title = self.request.GET.get('title')

        context['form'] = BookSearchForm(initial={
            'title': q_title,})

        return context

    def get_queryset(self):
        books = Book.objects.all()
        q_title = self.request.GET.get('title')

        if q_title:
            books = books.filter(title__icontains=q_title)

        return books
