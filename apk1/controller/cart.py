from django.shortcuts import render, redirect
from django.contrib import messages
from apk1.models import Product, Cart
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

def addtocart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            try:
                product_check = Product.objects.get(id=prod_id)
            except Product.DoesNotExist:
                return JsonResponse({'status': "No such product found"})

            if Cart.objects.filter(user=request.user.id, product_id=prod_id).exists():
                return JsonResponse({'status': "Product Already in Cart"})
            else:
                prod_qty = int(request.POST.get('product_qty'))

                if product_check.quantity >= prod_qty:
                    Cart.objects.create(user=request.user, product_id=prod_id, product_qty=prod_qty)
                    return JsonResponse({'status': "Product added successfully"})
                else:
                    return JsonResponse({'status': f"Only {product_check.quantity} quantity available"})
        else:
            return JsonResponse({'status': "Login to Continue"})
    
    return redirect('main')

@login_required(login_url='loginpage')
def viewcart(request):
    cart =Cart.objects.filter(user=request.user)
    context = {'cart' : cart}
    return render(request, "products/cart.html", context)

@login_required(login_url='loginpage')
def updatecart(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        prod_qty = int(request.POST.get('product_qty'))
        
        if Cart.objects.filter(user=request.user, product_id=prod_id).exists():
            cart_item = Cart.objects.get(user=request.user, product_id=prod_id)
            
            if cart_item.product.quantity >= prod_qty:
                cart_item.product_qty = prod_qty
                cart_item.save()
                return JsonResponse({'status': 'Updated successfully'})
            else:
                return JsonResponse({'status': f'Only {cart_item.product.quantity} quantity available'})
        else:
            return JsonResponse({'status': 'Product not in cart'})
    
    return JsonResponse({'status': 'Invalid request'}, status=400)


@login_required(login_url='loginpage')
def deletecartitem(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if Cart.objects.filter(user=request.user, product_id=prod_id).exists():
            cart_item = Cart.objects.get(user=request.user, product_id=prod_id)
            cart_item.delete()
            return JsonResponse({'status': 'Deleted successfully'})
        else:
            return JsonResponse({'status': 'Product not in cart'})
    return JsonResponse({'status': 'Invalid request'}, status=400)