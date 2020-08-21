from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView

from .models import Item, Comment


class ItemList(ListView):
    queryset = Item.objects.order_by('-posted')
    context_object_name = 'item_list'
    template_name = 'index.html'


class ItemDetail(DetailView):
    model = Item
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(item_id=self.kwargs.get('pk')).order_by('-posted')

        return context


class ItemCreate(CreateView):
    model = Item
    fields = '__all__'


class ItemDelete(DeleteView):
    model = Item
    success_url = reverse_lazy('item-list')


class CommentCreate(CreateView):
    model = Comment
    fields = '__all__'
