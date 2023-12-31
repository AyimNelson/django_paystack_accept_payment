from django.shortcuts import get_object_or_404, render, redirect
from .models import Product, Payment
from django.views.generic import ListView, DetailView, TemplateView
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
from authentication.models import User
from django.contrib import messages

# Create your views here.
class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = "products"
    
    
"""
Data about the product object is collected and assigned to paystact...

This View handles only a single product, since we're focused on how to accept payment

If you are making the integration into an e-commerse application where the user has a lot of items in their cart,
then do the implementation on the CartDetails...

All you need is to collect all the neccessary parameters to make the payment

Such as, the user_id, email, total_amount, currency ect


"""
# It is neccessary to check if the user is authenticated before processing payment 
# "Preform the check in the template to restrict anonymose users from clicking the pay button"

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        user = self.request.user
        
        amount = product.price * 100 #convert to persewas...
        user_mail = self.request.user.email
        paystack_public_key = settings.PAYSTACK_PUBLIC_KEY

        context['amount'] = amount
        context['user_mail'] = user_mail
        context['paystack_public_key'] = paystack_public_key

        context['product'] = product
        
        return context
    


"""
Lets handle the Success of a payment
In this view, We are using the GET method to pick the reference id that was generated by paystack
For security reasons we should not create our own reference...

"""
# It is neccessary to check if the user is authenticated before processing payment
class SuccessPageView(LoginRequiredMixin, TemplateView):
    template_name = 'success_page.html'  # Replace with your success page template

    def get(self, request, *args, **kwargs):
        # Retrieve the payment reference from the query parameters
        reference = request.GET.get('reference')
        
        """
        Check if reference already exist in the database, since paystacks reference id is unique
        If the reference id from paystack already exist for a Payment object, it means the user is perhaps trying to refresh the successpage
        or they want to compromise the systems security...()
        This will create a new Payment object, which means the user will make a new purchase fro every refresh they make...
        
        """
        if Payment.objects.filter(reference=reference).exists():
            messages.warning(request, 'Purchase already exist for this Product.')
            return redirect('products')
        
        """
        Make a request to the Paystack API to verify the transaction
        Base on the reference from paystack, let us use that same reference to verify if the data is accurate
        
        The reference will be used to collect all the neccesary to help us create a Purchase object in our database to keep tract on sold items
        
        
        """
        paystack_secret_key = settings.PAYSTACK_SECRET_KEY
        url = f'https://api.paystack.co/transaction/verify/{reference}'
        headers = {
            'Authorization': f'Bearer {paystack_secret_key}',
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers)
        data = response.json()

        # Check if the transaction was successful
        if data['status'] and reference:
            # Retrieve the necessary data from the Paystack response
            amount = data['data']['amount']/100
            email = data['data']['customer']['email']
            product_id = data['data']['metadata']['product_id']
            user_id = data['data']['metadata']['user_id']          
            
            # Retrieve the corresponding user object
            user = get_object_or_404(User, pk=user_id)
            # Retrieve the corresponding product object
            product = get_object_or_404(Product, pk=product_id)
            
            # Create a new purchase object in the database
            payment = Payment.objects.create(
                user=user,
                product=product,
                reference=reference,
                amount=amount,
            )
            
            # Render the success page template with the necessary context
            context = {
                'user':user,
                'product': product,
                'amount': amount,
                'user_email': email,
                'payment': payment,
            }
            return render(request, 'success_page.html', context)
        # If the transaction was not successful, handle the failure case
        else:
            # pass
            return render(request, 'error_page.html')
        
        
