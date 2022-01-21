from django.views import generic
from django.core.paginator import Paginator
from product.models import Variant,ProductVariantPrice,Product,ProductVariant

class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context


#List = ProductVariantPrice.objects.all() 
#p = Paginator(List, 2)
#Page = p.page(1)
#paginator = Paginator(List, 2)

class ViewProductList(generic.TemplateView):
    template_name = 'products/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        List = ProductVariantPrice.objects.all() 
        variant = Variant.objects.all()
        
        paginator = Paginator(List, 2)
        page_number = self.request.GET.get('page',1)
        page_obj = paginator.get_page(page_number)
        total_product = paginator.count
        start_index = page_obj.start_index()
        end_index = page_obj.end_index()


        product_name = self.request.GET.get('title')
        price_from = self.request.GET.get('price_from')
        price_to = self.request.GET.get('price_to')
        product_variant = self.request.GET.get('variant')
        product_Date = self.request.GET.get('date')

        
        if product_name !='' and product_name is not None:
            context['product'] = ProductVariantPrice.objects.filter(product__title=product_name)
        elif price_from !='' and price_from is not None:
            context['product'] = ProductVariantPrice.objects.filter(price=price_from)
        elif product_variant !='' and product_variant is not None:
            context['product'] = ProductVariantPrice.objects.filter(product_variant_one__variant__title=product_variant,product_variant_two__variant__title=product_variant,product_variant_three__variant__title=product_variant)
        elif price_to !='' and price_to is not None:
            context['product'] = ProductVariantPrice.objects.filter(price=price_to)
        elif product_Date !='' and product_Date is not None:
            context['product'] = ProductVariantPrice.objects.filter(product__sku=product_Date)
        elif product_name !='' and product_name is not None and price_from !='' and price_from is not None:
            context['product'] = ProductVariantPrice.objects.filter(product__title=product_name,price=price_from)
        else:
            context['product'] = page_obj.object_list
        
        
        
        context['paginator'] = paginator
        context['total'] = total_product
        context['start'] = start_index
        context['end'] = end_index
        context['variant'] = variant
        return context