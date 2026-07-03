from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, BorrowRequest
from .forms import ProductForm, BorrowForm
from Profile.models import Profile


def _current_hr_profile(request):
    profile_id = request.session.get('profile_id')
    if not profile_id:
        return None
    return Profile.objects.filter(id=profile_id, role='hr').first()


def hr_dashboard(request):
    if not _current_hr_profile(request):
        return redirect('login')

    product_form = ProductForm()
    borrow_form = BorrowForm()
    active_tab = 'products'

    if request.method == 'POST' and 'add_product' in request.POST:
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return redirect('hr_dashboard')
        active_tab = 'forms'

    if request.method == "POST" and "borrow_product" in request.POST:
        borrow_form = BorrowForm(request.POST)
        if borrow_form.is_valid():
            borrow = borrow_form.save(commit=False)
            borrow.product = Product.objects.get(id=request.POST["product_id"])
            borrow.save()
            return redirect("hr_dashboard")

    products = Product.objects.all().order_by('-id')
    borrow_requests = BorrowRequest.objects.select_related('product').order_by('-submitted_at')

    return render(request, 'hr.html', {
        'product_form': product_form,
        'borrow_form': borrow_form,
        'products': products,
        'active_tab': active_tab,
        'borrow_requests': borrow_requests,
    })


def update_status(request, id):
    """HR clicks Approve or Reject on a borrow request"""
    req = get_object_or_404(BorrowRequest, id=id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action in ['approved', 'rejected']:
            req.status = action
            req.save()
    return redirect('/hr/?tab=details')


def hr_status(request):
    """Status page — shows only approved and rejected"""
    if not _current_hr_profile(request):
        return redirect('login')

    borrow_requests = BorrowRequest.objects.select_related('product').exclude(status='pending').order_by('-submitted_at')
    return render(request, 'hr.html', {
        'active_tab': 'status',
        'borrow_requests': borrow_requests,
        'products': Product.objects.all().order_by('-id'),
        'product_form': ProductForm(),
        'borrow_form': BorrowForm(),
    })


def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == "POST":
        product.delete()
        return redirect('hr_dashboard')
    return render(request, 'hr.html', {
        'product': product,
        'active_tab': 'products',
        'products': Product.objects.all().order_by('-id'),
        'product_form': ProductForm(),
        'borrow_form': BorrowForm(),
        'borrow_requests': BorrowRequest.objects.select_related('product').order_by('-submitted_at'),
    })


def delete_borrow_request(request, id):
    """Delete a single borrow request row from the Details or Status tab."""
    borrow_request = get_object_or_404(BorrowRequest, id=id)
    came_from = request.POST.get('tab', 'details') if request.method == "POST" else 'details'
    if request.method == "POST":
        borrow_request.delete()
        if came_from == 'status':
            return redirect('hr_status')
    return redirect('/hr/?tab=details')