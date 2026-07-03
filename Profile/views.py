from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password
from .models import Profile
from .forms import RegisterForm
from hr.models import Product, BorrowRequest as HRBorrowRequest


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login(request):
    error = None
    submitted_username = ''
    if request.method == "POST":
        submitted_username = request.POST.get('username', '').strip()
        submitted_password = request.POST.get('password', '')
        profile = Profile.objects.filter(username=submitted_username).first()

        if profile is None or not check_password(submitted_password, profile.password):
            error = 'Invalid username or password.'
        else:
            request.session.flush()
            request.session['profile_id'] = profile.id
            if profile.role == 'hr':
                return redirect('hr_dashboard')
            return redirect('staff')

    return render(request, 'login.html', {'error': error, 'username': submitted_username})


def logout(request):
    request.session.flush()
    return redirect('login')


def staff(request):
    profile_id = request.session.get('profile_id')
    current_profile = Profile.objects.filter(id=profile_id).first() if profile_id else None

    if request.method == 'POST' and 'borrow_product' in request.POST:
        if not current_profile:
            return redirect('login')
        product_id = request.POST.get('product_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        take_time = request.POST.get('take_time')
        bring_time = request.POST.get('bring_time')
        if product_id and first_name and take_time and bring_time:
            HRBorrowRequest.objects.create(
                product_id=product_id,
                requested_by=current_profile,
                first_name=first_name,
                last_name=last_name,
                take_time=take_time,
                bring_time=bring_time,
            )
        return redirect('staff')

    if current_profile:
        profiles = Profile.objects.filter(id=current_profile.id)
        borrow_requests = HRBorrowRequest.objects.filter(
            requested_by=current_profile
        ).select_related('product').order_by('-submitted_at')
    else:
        profiles = Profile.objects.none()
        borrow_requests = HRBorrowRequest.objects.none()

    products = Product.objects.all()
    return render(request, 'staff.html', {
        'profiles': profiles, 'products': products, 'borrow_requests': borrow_requests,
    })


def delete_history_request(request, id):
    profile_id = request.session.get('profile_id')
    req = get_object_or_404(HRBorrowRequest, id=id, requested_by_id=profile_id)
    if request.method == "POST":
        req.delete()
    return redirect('staff')


def delete_request_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == "POST":
        product.delete()
    return redirect('staff')