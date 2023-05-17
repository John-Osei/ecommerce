import datetime
from django.shortcuts import render, redirect
from core.models import CartOrder, Product, Category
from django.db.models import Sum
from userauths.models import User
from useradmin.forms import AddProductForm
from django.contrib.auth.decorators import login_required
from .decorators import user_is_superuser


@login_required
@user_is_superuser
def dashboard(request):
    user = User.objects.all()
    revenue = CartOrder.objects.aggregate(price=Sum("price"))
    total_orders_count = CartOrder.objects.all()
    all_products = Product.objects.all()
    all_categories = Category.objects.all()
    new_customers = User.objects.all().order_by("-id")[:6]
    latest_orders = CartOrder.objects.all().order_by("-id")

    this_month = datetime.datetime.now().month
    monthly_revenue = CartOrder.objects.filter(order_date__month=this_month).aggregate(price=Sum("price"))

    
    context = {
        "monthly_revenue": monthly_revenue,
        "revenue": revenue,
        "user": user,
        "all_products": all_products,
        "all_categories": all_categories,
        "new_customers": new_customers,
        "latest_orders": latest_orders,
        "total_orders_count": total_orders_count,
    }
    return render(request, "useradmin/dashboard.html", context)


@login_required
@user_is_superuser
def dashboard_products(request):
    all_products = Product.objects.all()
    all_categories = Category.objects.all()
    
    context = {
        "all_products": all_products,
        "all_categories": all_categories,
    }
    return render(request, "useradmin/dashboard-products.html", context)


@login_required
@user_is_superuser
def dashboard_orders(request):
    
    latest_orders = CartOrder.objects.all().order_by("-id")

    
    context = {
        "latest_orders": latest_orders,
    }

    return render(request, "useradmin/dashboard-orders.html", context)



@login_required
@user_is_superuser
def dashboard_add_product(request):
    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            form.save_m2m()
            return redirect("useradmin:dashboard-products")
    else:
        form = AddProductForm()
    context = {
        'form':form
    }
    return render(request, "useradmin/dashboard-add-products.html", context)


@login_required
@user_is_superuser
def dashboard_edit_product(request, pid):
    product = Product.objects.get(pid=pid)

    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.save()
            form.save_m2m()
            return redirect("useradmin:dashboard-products")
    else:
        form = AddProductForm(instance=product)
    context = {
        'form':form,
        'product':product,
    }
    return render(request, "useradmin/dashboard-edit-products.html", context)


@login_required
@user_is_superuser
def dashboard_delete_product(request, pid):
    product = Product.objects.get(pid=pid)
    product.delete()
    return redirect("useradmin:dashboard-products")