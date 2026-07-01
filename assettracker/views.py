from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, AssetForm
from .models import User, Asset
from .models import Employee, Asset, AssetRequest
from .forms import AssetRequestForm
from django.contrib import messages
from django.core.paginator import Paginator

def register_view(request):

 if request.method == 'POST':

    form = RegisterForm(request.POST)

    if form.is_valid():

        form.save()

        return redirect('login')

 else:

    form = RegisterForm()

 return render(request, 'assettracker/register.html',  {'form': form})


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            if user.role == "HR":
                return redirect("hr_dashboard")

            else:
                return redirect("staff_dashboard")

        else:

            messages.error(
                request,
                "Invalid Username or Password"
            )

    return render(
        request,
        "assettracker/login.html"
    )
def logout_view(request):
 logout(request)

 return redirect('login')

from django.core.paginator import Paginator

@login_required
def hr_dashboard(request):

    employees = User.objects.all()

    search_query = request.GET.get("search", "").strip()

    asset_list = Asset.objects.all().order_by("-id")

    if search_query:
        asset_list = asset_list.filter(name__icontains=search_query)

    paginator = Paginator(asset_list, 4)   # 4 assets per page

    page_number = request.GET.get("page")

    assets = paginator.get_page(page_number)

    requests = AssetRequest.objects.all()

    # Dashboard Counts
    total_employees = employees.count()
    total_assets = Asset.objects.count()
    available_assets = Asset.objects.filter(is_in_stock=True).count()
    pending_requests = AssetRequest.objects.filter(status="PENDING").count()

    return render(
        request,
        "hr/dashboard.html",
        {
            "employees": employees,
            "assets": assets,
            "requests": requests,
            "search_query": search_query,

            # Dashboard counts
            "total_employees": total_employees,
            "total_assets": total_assets,
            "available_assets": available_assets,
            "pending_requests": pending_requests,
        }
    )
@login_required
def staff_dashboard(request):


 return render(
    request,
    'staff/dashboard.html'
)

def approve_request(request, id):
    req = get_object_or_404(AssetRequest, id=id)
    req.status = "APPROVED"
    req.save()

    asset = req.asset
    asset.is_in_stock = False
    asset.save()

    return redirect("/hr-dashboard/?tab=requests")


@login_required
def reject_request(request, id):

    req = get_object_or_404(
        AssetRequest,
        id=id
    )

    if request.method == "POST":

        req.status = "REJECTED"

        req.rejection_reason = request.POST.get(
            "rejection_reason"
        )

        req.save()

        return redirect("/hr-dashboard/?tab=requests")

    return render(
        request,
        "hr/reject_request.html",
        {
            "req": req
        }
    )
@login_required
def request_asset(request):

    if request.method == "POST":

        form = AssetRequestForm(request.POST)

        if form.is_valid():

            asset_request = form.save(commit=False)

            # Logged-in staff user
            asset_request.employee = request.user

            asset_request.save()

            return redirect("staff_dashboard")

    else:

        form = AssetRequestForm()

    return render(
        request,
        "staff/request_asset.html",
        {
            "form": form
        }
    )
@login_required
def asset_list(request):

    assets = Asset.objects.all()

    return render(
        request,
        'hr/asset_list.html',
        {'assets': assets}
    )
@login_required
def employee_profile(request):

    employees = User.objects.all()

    return render(
        request,
        'hr/employee_profile.html',
        {
            'employees': employees
        }
    )

@login_required
def submitted_requests(request):

    requests = AssetRequest.objects.select_related(
        "employee",
        "asset"
    ).all().order_by("-requested_at")

    return render(
        request,
        "hr/submitted_requests.html",
        {
            "requests": requests
        }
    )

@login_required
def history_page(request):

    return render(
        request,
        'hr/history.html'
    )


@login_required
def inventory_page(request):

    return render(
        request,
        'hr/inventory.html'
    )
@login_required
def update_employee(request, id):

    employee = User.objects.get(id=id)

    if request.method == "POST":

        employee.first_name = request.POST.get(
            "first_name"
        )

        employee.last_name = request.POST.get(
            "last_name"
        )

        employee.email = request.POST.get(
            "email"
        )

        employee.phone_number = request.POST.get(
            "phone_number"
        )

        employee.branch = request.POST.get(
            "branch"
        )

        employee.role = request.POST.get(
            "role"
        )

        employee.save()

        return redirect(
            'hr_dashboard'
        )

    return render(
        request,
        'hr/update_employee.html',
        {'employee': employee}
    )


@login_required
def delete_employee(request, id):

    employee = User.objects.get(id=id)

    employee.delete()

    return redirect(
        'hr_dashboard'
    )
from django.core.paginator import Paginator


@login_required
def assets_page(request):

    assets_list = Asset.objects.all().order_by("id")

    paginator = Paginator(assets_list, 4)

    page_number = request.GET.get("page")

    assets = paginator.get_page(page_number)

    return render(
        request,
        "hr/assets.html",
        {
            "assets": assets
        },
    )
@login_required
def add_asset(request):

    if request.method == 'POST':

        form = AssetForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            return redirect('/hr-dashboard/?tab=assets')

    else:

        form = AssetForm()

    return render(
        request,
        'hr/add_asset.html',
        {'form': form}
    )


@login_required
def update_asset(request, id):

    asset = Asset.objects.get(id=id)

    if request.method == 'POST':

        form = AssetForm(
            request.POST,
            request.FILES,
            instance=asset
        )

        if form.is_valid():

            form.save()

            return redirect('hr_dashboard')

    else:

        form = AssetForm(
            instance=asset
        )

    return render(
        request,
        'hr/update_asset.html',
        {
            'form': form,
            'asset': asset
        }
    )


@login_required
def delete_asset(request, id):

    asset = Asset.objects.get(id=id)

    asset.delete()

    return redirect('assets_page')

@login_required
def asset_detail(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)

    return render(
        request,
        "hr/asset_detail.html",
        {
            "asset": asset
        }
    )

@login_required
def toggle_stock(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)

    asset.is_in_stock = not asset.is_in_stock
    asset.save()

    return redirect("asset_detail", asset_id=asset.id)


@login_required
def asset_edit(request, asset_id):

    asset = get_object_or_404(
        Asset,
        id=asset_id
    )

    if request.method == "POST":

        asset.name = request.POST.get("name")
        asset.description = request.POST.get("description")

        if request.FILES.get("image"):
            asset.image = request.FILES["image"]

        asset.save()

        return redirect(
            "asset_detail",
            asset_id=asset.id
        )

    return render(
        request,
        "asset/edit.html",
        {
            "asset": asset
        }
    )


@login_required
def asset_delete(request, asset_id):

    asset = get_object_or_404(
        Asset,
        id=asset_id
    )

    if request.method == "POST":
        asset.delete()
        return redirect("/hr-dashboard/?tab=assets")

    return redirect("asset_detail", asset_id=asset.id)