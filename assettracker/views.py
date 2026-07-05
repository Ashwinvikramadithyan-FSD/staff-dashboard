from django.shortcuts import render, get_object_or_404, redirect
from .forms import AssetForm
from .models import User, Asset, AssetRequest
from django.core.paginator import Paginator


def hr_dashboard(request):
    employees = User.objects.all()
    search_query = request.GET.get("search", "").strip()
    asset_list = Asset.objects.all().order_by("-id")

    if search_query:
        asset_list = asset_list.filter(name__icontains=search_query)

    paginator = Paginator(asset_list, 4)
    page_number = request.GET.get("page")
    assets = paginator.get_page(page_number)

    requests = AssetRequest.objects.select_related(
        "employee", "asset"
    ).all().order_by("-requested_at")

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
            "total_employees": total_employees,
            "total_assets": total_assets,
            "available_assets": available_assets,
            "pending_requests": pending_requests,
        }
    )


def approve_request(request, id):
    req = get_object_or_404(AssetRequest, id=id)
    req.status = "APPROVED"
    req.save()
    asset = req.asset
    asset.is_in_stock = False
    asset.save()
    return redirect("/?tab=requests")


def reject_request(request, id):
    req = get_object_or_404(AssetRequest, id=id)

    if request.method == "POST":
        req.status = "REJECTED"
        req.rejection_reason = request.POST.get("rejection_reason")
        req.save()
        return redirect("/?tab=requests")

    return render(request, "hr/reject_request.html", {"req": req})


def update_employee(request, id):
    employee = get_object_or_404(User, id=id)

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
    employee = get_object_or_404(User, id=id)
    employee.delete()
    return redirect("hr_dashboard")


def add_asset(request):
    if request.method == "POST":
        form = AssetForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/?tab=assets")
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
        return redirect("/?tab=assets")
    return redirect("asset_detail", asset_id=asset.id)