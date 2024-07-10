from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages, auth
from accounts.models import user, userProfile
from vendor.models import vendor
from menuBuilder.models import category, foodItem
from django.contrib.auth.decorators import login_required, user_passes_test
from vendor.forms import registerVendorForm
from accounts.forms import userProfileForm
from accounts.context_processor import getCartItems, getTotal
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import PermissionDenied
from django.db.models import Prefetch
from .models import userCart
from menuBuilder.models import foodItem
from orders.forms import orderForm
# Create your views here.
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


# Restrict the customer from accessing the vendor page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied
    
def marketPlace(request):
    vendors = vendor.objects.filter(is_approved = True, user__is_active = True)
    vendor_count = vendors.count()
    context = {
        "vendors":vendors,
        "vendor_count":vendor_count
    }
    return render(request, "user/marketPlace.html", context)
def restaurant(request, id):
    selectedVendor = vendor.objects.get(id = id)
    categories = category.objects.filter(vendor = selectedVendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset=foodItem.objects.filter(isAvailable=True)
        )
    )

    cart_items = None 

    if request.user.is_authenticated:
        cart_items = userCart.objects.filter(user=request.user)
    context = {
        "categories":categories,
        "vendor":selectedVendor,
        "cart_items":cart_items
    }
    return render(request, "user/restaurantDetails.html", context)



def homePage(request):
    return render(request, "home/homePage.html")

@login_required(login_url='login')
def customerDashboard(request):
    user = request.user
    print(user)
    return redirect("homePage")

@login_required(login_url='login')
def vendorDashboard(request):
    Vendor = vendor.objects.get(user=request.user)
    print(vendor.vendor_name)
    context = {"user":request.user
               }
    return render(request, "vendor/vendorProfile.html", context)

@login_required(login_url='login')
def checkAndRedirect(request):
    if request.user.role == user.Customer:
        return redirect("customerDashboard")
    elif request.user.role == user.Vendor:
        return redirect("vendorDashboard")
    return redirect("homePage")

def loginUser(request):
    if request.user.is_authenticated:
        return checkAndRedirect(request)
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(request, email=email, password = password)

        if user is not None:
            messages.success(request,"login successfull")
            login(request, user)

            return checkAndRedirect(request)
        
        else:
            messages.warning(request,"login failed")
            

    return render(request, "accounts/login.html")

@login_required(login_url='login')
def logoutUser(request):
    if request.user.is_authenticated:
        messages.info(request, "Logged out succesfully !!")
        logout(request)
    return render(request, "accounts/login.html")

@login_required(login_url='login')
def changePassword(request):
    request.session['uid'] = request.user.pk
    return render(request, "accounts/resetPassword.html",{"update":1})

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def restaurantProfile(request):
    Vendor = vendor.objects.get(user=request.user)
    UserProfile = userProfile.objects.get(user=request.user)
    
    if request.method == "POST":
        vendor_form = registerVendorForm(request.POST, request.FILES, instance=Vendor)
        profile_form = userProfileForm(request.POST, request.FILES, instance=UserProfile)

        if vendor_form.is_valid() and profile_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, "Profile Updated!")
            return redirect("restaurantProfile")
        else:
            print(profile_form.errors)
    else:
        vendor_form = registerVendorForm(instance=Vendor)
        profile_form = userProfileForm(instance=UserProfile)

    context = {"vendor_form" : vendor_form,
               "profile_form":profile_form,
               "profile":UserProfile}
    return render(request, "vendor/restaurant-restaurant.html", context)


def addToCart(request, id):
    if request.user.is_authenticated:
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            try:
                
                currentFoodItem = foodItem.objects.get(id=id)
                
                try:
                    chkCart = userCart.objects.get(user=request.user, foodItem=currentFoodItem)
                    chkCart.quantity += 1
                    chkCart.save()
                    
                    return JsonResponse({"status":"success","message":"incremented","cartItem":getCartItems(request),'qty':chkCart.quantity,"totals":getTotal(request)})
                except:
                    
                    chkCart = userCart.objects.create(user=request.user, foodItem=currentFoodItem, quantity=1)
                    print(id)
                    return JsonResponse({"status":"success","message":"newly added","cartItem":getCartItems(request),'qty':chkCart.quantity,"totals":getTotal(request)})

            except:
                return JsonResponse({"status":"failed","message":"id doesnt exist"})
        else:
            return JsonResponse({"status":"failed","message":"Only ajax req"})

    return JsonResponse({"status":"failed","message":"please log in"})
    # return HttpResponse("added to cart" + str(id))


def decreaseCart(request, id):
    if request.user.is_authenticated:
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            try:
                currentFoodItem = foodItem.objects.get(id=id)

                try:
                    chkCart = userCart.objects.get(user=request.user, foodItem=currentFoodItem)
                    chkCart.quantity -= 1
                    chkCart.save()

                    if chkCart.quantity == 0:
                        chkCart.delete()

                    return JsonResponse({"status":"success","message":"decremented","cartItem":getCartItems(request),'qty':chkCart.quantity,"totals":getTotal(request)})
                except:
                    # chkCart = userCart.objects.create(user=request.user, foodItem=currentFoodItem, quantity=1)
                    return JsonResponse({"status":"failed","message":"No food item"})

            except:
                return JsonResponse({"status":"failed","message":"id doesnt exist"})
        else:
            return JsonResponse({"status":"failed","message":"Only ajax req"})

    return JsonResponse({"status":"failed","message":"please log in"})


@login_required(login_url='login')
def viewCart(request):
    cart_items = userCart.objects.filter(user=request.user)
    context = {
        "cart_items":cart_items
    }
    return render(request, "user/cart.html",context)

@login_required(login_url='login')
def deleteCart(request,id):
    try:
        chckCart = userCart.objects.filter(user=request.user, id=id)
        
        chckCart.delete()
        messages.info(request, "item Delete")
        return JsonResponse({"status":"success","message":"item deleted","cartItem":getCartItems(request),"totals":getTotal(request)})

    except:
        return JsonResponse({"status":"failed","message":"No item found"})

@login_required(login_url='login')
def checkout(request):
    cart_items = userCart.objects.filter(user=request.user)
    form = orderForm()

    user_profile = userProfile.objects.get(user=request.user)
    default_values = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'phone': request.user.phone_number,
        'email': request.user.email,
        'address': user_profile.address_line,
        'country': user_profile.country,
        'state': user_profile.state,
        'city': user_profile.city,
        'pin_code': user_profile.pin_code,
    }
    form = orderForm(initial=default_values)
    
    context = {
        "cart_items":cart_items,
        "form":form
    }
    return render(request, "user/checkout.html",context)