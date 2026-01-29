from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Category, Product


def category_list(request):
    query = request.GET.get('q', '')
    categories = Category.objects.filter(is_active=True)
    if query:
        categories = categories.filter(name__icontains=query)

    return render(request, 'catalog/category_list.html', {
        'categories': categories,
        'query': query
    })


def category_create(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST.get('description', '')
        category = Category.objects.create(
            name=name,
            description=description
        )
        messages.success(request, 'Категория создана успешно!')
        return redirect('category_list')
    return render(request, 'catalog/category_form.html')


def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.name = request.POST['name']
        category.description = request.POST.get('description', '')
        category.save()
        messages.success(request, 'Категория обновлена!')
        return redirect('category_list')
    return render(request, 'catalog/category_form.html', {'category': category})


def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if category.has_products():
        messages.error(request, 'Нельзя удалить категорию с товарами!')
    else:
        category.delete()
        messages.success(request, 'Категория удалена!')
    return redirect('category_list')


def product_list(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category')
    sort = request.GET.get('sort', 'name')

    products = Product.objects.filter(is_active=True)

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    if category_id:
        products = products.filter(category_id=category_id)

    products = products.order_by(sort)

    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    categories = Category.objects.filter(is_active=True)

    return render(request, 'catalog/product_list.html', {
        'products': products,
        'categories': categories,
        'query': query,
        'category_id': category_id,
        'sort': sort
    })


def product_create(request):
    if request.method == 'POST':
        product = Product.objects.create(
            name=request.POST['name'],
            category_id=request.POST['category'],
            description=request.POST.get('description', ''),
            price=request.POST['price'],
            stock=request.POST.get('stock', 0),
            image=request.FILES.get('image')
        )
        messages.success(request, 'Товар создан успешно!')
        return redirect('product_list')
    categories = Category.objects.filter(is_active=True)
    return render(request, 'catalog/product_form.html', {'categories': categories})


def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.name = request.POST['name']
        product.category_id = request.POST['category']
        product.description = request.POST.get('description', '')
        product.price = request.POST['price']
        product.stock = request.POST.get('stock', 0)
        product.is_active = request.POST.get('is_active', True) == 'on'
        if request.FILES.get('image'):
            product.image = request.FILES['image']
        product.save()
        messages.success(request, 'Товар обновлен!')
        return redirect('product_list')
    categories = Category.objects.filter(is_active=True)
    return render(request, 'catalog/product_form.html', {
        'product': product,
        'categories': categories
    })


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, 'Товар удален!')
    return redirect('product_list')
