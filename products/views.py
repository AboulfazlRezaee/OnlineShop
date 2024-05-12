from django.views import generic
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.utils.translation import gettext as _

from .models import Product, Comment, Category
from .forms import CommentForm

# Create your views here.

def category(request, slug):
    slug = slug.replace('-', ' ')

    try:
        category = Category.objects.get(name=slug)
        products = Product.objects.filter(category=category, active=True).order_by('-datetime_modified')
        context = {
            'products': products,
            'category': category,
            }
        return render(request, 'products/category_list.html', context)
    except:
        messages.error(request, _("That Category doesn't exist!"))
        return redirect('product_list')


class ProductListView(generic.ListView):
    # model = Product
    queryset = Product.objects.filter(active=True)
    template_name = 'products/product_list.html'
    context_object_name = 'products'

    #sort by datetime_update
    ordering = ['-datetime_modified']
    paginate_by = 12

    

class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context
    

class CommentCreateView(generic.CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user

        product_id = int(self.kwargs['product_id'])
        product = get_object_or_404(Product, id=product_id)
        obj.product = product

        if form.is_valid():
            messages.success(self.request, _('Your Comment added Successfully.'))
        else:
            messages.error(self.request, _('Form is not valid. Please check your input.'))


        return super().form_valid(form)