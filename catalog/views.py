from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Category, Product
from .forms import CategoryForm, ProductForm


def category_list(request):
    search = request.GET.get("search", "")
    qs = Category.objects.all()
    if search:
        qs = qs.filter(name__icontains=search)
    return render(
        request,
        "catalog/category_list.html",
        {"categories": qs, "search": search},
    )


def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Категория создана.")
            return redirect("catalog:category_list")
    else:
        form = CategoryForm()
    return render(
        request,
        "catalog/category_form.html",
        {"form": form, "title": "Создать категорию"},
    )


def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Категория обновлена.")
            return redirect("catalog:category_list")
    else:
        form = CategoryForm(instance=category)
    return render(
        request,
        "catalog/category_form.html",
        {"form": form, "title": "Редактировать категорию"},
    )


def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        if category.product_set.exists():
            messages.error(request, "Нельзя удалить категорию с товарами.")
        else:
            category.delete()
            messages.success(request, "Категория удалена.")
        return redirect("catalog:category_list")
    return render(
        request,
        "catalog/category_confirm_delete.html",
        {"category": category},
    )


def product_list(request):
    category_id = request.GET.get("category")
    search = request.GET.get("search", "")
    sort = request.GET.get("sort", "name")
    order = request.GET.get("order", "asc")

    qs = Product.objects.filter(is_active=True)

    if category_id:
        qs = qs.filter(category_id=category_id)

    if search:
        qs = qs.filter(
            Q(name__icontains=search) | Q(description__icontains=search)
        )

    if sort == "price":
        qs = qs.order_by(f"price" if order == "asc" else "-price")
    elif sort == "created_at":
        qs = qs.order_by(f"-created_at" if order == "asc" else "created_at")
    else:
        qs = qs.order_by(f"name" if order == "asc" else "-name")

    categories = Category.objects.filter(is_active=True)
    return render(
        request,
        "catalog/product_list.html",
        {
            "products": qs,
            "categories": categories,
            "category_id": category_id,
            "search": search,
            "sort": sort,
            "order": order,
        },
    )


def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Товар создан.")
            return redirect("catalog:product_list")
    else:
        form = ProductForm()
    return render(
        request,
        "catalog/product_form.html",
        {"form": form, "title": "Создать товар"},
    )


def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Товар обновлён.")
            return redirect("catalog:product_list")
    else:
        form = ProductForm(instance=product)
    return render(
        request,
        "catalog/product_form.html",
        {"form": form, "title": "Редактировать товар"},
    )


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Товар удалён.")
        return redirect("catalog:product_list")
    return render(
        request,
        "catalog/product_confirm_delete.html",
        {"product": product},
    )
