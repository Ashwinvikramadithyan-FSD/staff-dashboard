from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .forms import AssetForm, AssetRequestForm
from .models import Asset, AssetRequest
from Profile.models import Profile, BorrowRequest
from django.core.paginator import Paginator


def hr_dashboard(request):
    employees = Profile.objects.all()
    search_query = request.GET.get("search", "").strip()
    asset_list = Asset.objects.all().order_by("-id")

    if search_query:
        asset_list = asset_list.filter(name__icontains=search_query)

    paginator = Paginator(asset_list, 4)
    page_number = request.GET.get("page")
    assets = paginator.get_page(page_number)

    requests = BorrowRequest.objects.select_related(
        "product", "requested_by"
    ).all().order_by("-submitted_at")

    total_employees = employees.count()
    total_assets = Asset.objects.count()
    available_assets = Asset.objects.filter(is_in_stock=True).count()
    pending_requests = BorrowRequest.objects.filter(status="pending").count()

    return render(
        request,
        "hr/dashboard.html",
        {
            "employees": employees,
            "assets": assets,
            "requests": requests,
            "search_query": search_query,
            "total_employees": total_employees,
            "total_assets": total_assets,
            "available_assets": available_assets,
            "pending_requests": pending_requests,
        }
    )


def submit_asset_request(request):
    success = False

    if request.method == "POST":
        form = AssetRequestForm(request.POST)
        if form.is_valid():
            form.save()
            form = AssetRequestForm()
            success = True
    else:
        form = AssetRequestForm()

    return render(
        request,
        "asset/request_form.html",
        {"form": form, "success": success}
    )


def asset_request_history(request):
    asset_requests = AssetRequest.objects.select_related(
        "product"
    ).all().order_by("-submitted_at")

    return render(
        request,
        "hr/asset_request_history.html",
        {"asset_requests": asset_requests}
    )


def approve_asset_request(request, id):
    req = get_object_or_404(AssetRequest, id=id)
    req.status = "APPROVED"
    req.save()
    return redirect("asset_request_history")


def reject_asset_request(request, id):
    req = get_object_or_404(AssetRequest, id=id)

    if request.method == "POST":
        req.status = "REJECTED"
        req.rejection_reason = request.POST.get("rejection_reason")
        req.save()
        return redirect("asset_request_history")

    return render(request, "hr/reject_asset_request.html", {"req": req})


def delete_asset_request(request, id):
    req = get_object_or_404(AssetRequest, id=id)
    if request.method == "POST":
        req.delete()
    return redirect("asset_request_history")


def delete_borrow_request(request, id):
    req = get_object_or_404(BorrowRequest, id=id)
    if request.method == "POST":
        req.delete()
    return redirect(f"{reverse('hr_dashboard')}?tab=requests")


def approve_request(request, id):
    req = get_object_or_404(BorrowRequest, id=id)
    req.status = "approved"
    req.save()
    return redirect(f"{reverse('hr_dashboard')}?tab=requests")


def reject_request(request, id):
    req = get_object_or_404(BorrowRequest, id=id)

    if request.method == "POST":
        req.status = "rejected"
        req.rejection_reason = request.POST.get("rejection_reason")
        req.save()
        asset = req.product
        asset.is_in_stock = True
        asset.save()
        return redirect(f"{reverse('hr_dashboard')}?tab=requests")

    return render(request, "hr/reject_request.html", {"req": req})


def update_employee(request, id):
    employee = get_object_or_404(Profile, id=id)

    if request.method == "POST":
        employee.first_name = request.POST.get("first_name")
        employee.last_name = request.POST.get("last_name")
        employee.email = request.POST.get("email")
        employee.phone_number = request.POST.get("phone_number")
        employee.branch = request.POST.get("branch")
        employee.role = request.POST.get("role")
        employee.save()
        return redirect("hr_dashboard")

    return render(request, "hr/update_employee.html", {"employee": employee})


def delete_employee(request, id):
    employee = get_object_or_404(Profile, id=id)
    employee.delete()
    return redirect("hr_dashboard")


def add_asset(request):
    if request.method == "POST":
        form = AssetForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(f"{reverse('hr_dashboard')}?tab=assets")
    else:
        form = AssetForm()

    return render(request, "hr/add_asset.html", {"form": form})


def asset_detail(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    return render(request, "hr/asset_detail.html", {"asset": asset})


def toggle_stock(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    asset.is_in_stock = not asset.is_in_stock
    asset.save()
    return redirect("asset_detail", asset_id=asset.id)


def asset_edit(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)

    if request.method == "POST":
        asset.name = request.POST.get("name")
        asset.description = request.POST.get("description")
        if request.FILES.get("image"):
            asset.image = request.FILES["image"]
        asset.save()
        return redirect("asset_detail", asset_id=asset.id)

    return render(request, "asset/edit.html", {"asset": asset})


def asset_delete(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    if request.method == "POST":
        asset.delete()
        return redirect(f"{reverse('hr_dashboard')}?tab=assets")
    return redirect("asset_detail", asset_id=asset.id)

def logout(request):
    request.session.flush()
    return redirect('login')