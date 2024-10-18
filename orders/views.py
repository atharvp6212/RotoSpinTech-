from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from .models import Order, OrderedSubPart
from .forms import OrderForm, OrderedSubPartForm
from django.utils import timezone
from django.contrib import messages
from inventory.models import SubPartRawMaterial, RawMaterial, Color, SubPart
from django.http import JsonResponse

@login_required
def select_sub_part(request):
    sub_parts = SubPart.objects.all()  # Get all available sub-parts

    if request.method == 'POST':
        # Get the selected sub-part ID from the form
        selected_sub_part_id = request.POST.get('sub_part')

        if selected_sub_part_id:
            # Redirect to the 'enter_new_order' view with the selected sub-part ID
            return redirect('enter_new_order', sub_part_id=selected_sub_part_id)

    return render(request, 'orders/select_sub_part.html', {
        'sub_parts': sub_parts,
    })


@login_required
def enter_new_order(request, sub_part_id):
    OrderedSubPartFormSet = formset_factory(OrderedSubPartForm, extra=1, can_delete=True)

    # Get the selected sub-part
    selected_sub_part = SubPart.objects.get(id=sub_part_id)

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        quantity = request.POST.get('quantity')  # Get quantity from POST data
        color_id = request.POST.get('color')  # Get selected color

        if order_form.is_valid() and quantity and color_id:
            # Proceed with order creation logic as before
            order = order_form.save()

            OrderedSubPart.objects.create(
                order=order,
                sub_part=selected_sub_part,
                quantity=quantity,
                color_id=color_id  # Assuming color is directly related to OrderedSubPart
            )

            messages.success(request, "Order placed successfully!")
            return redirect('admin_dashboard')

    else:
        order_form = OrderForm()

    return render(request, 'orders/enter_new_order.html', {
        'order_form': order_form,
        'selected_sub_part': selected_sub_part,
    })

def generate_reports(request):
    orders = []
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        if start_date and end_date:
            try:
                # Parse date strings to datetime objects
                start_date = timezone.make_aware(timezone.datetime.strptime(start_date, '%Y-%m-%d'))
                end_date = timezone.make_aware(timezone.datetime.strptime(end_date, '%Y-%m-%d'))

                # Debugging: Print parsed dates
                print(f"Start Date: {start_date}")
                print(f"End Date: {end_date}")

                # Filter orders based on the date range
                orders = Order.objects.filter(order_date__range=[start_date, end_date])

            except ValueError as e:
                # Handle invalid date format
                print(f"Date parsing error: {e}")
                orders = Order.objects.none()
        else:
            print("No date range provided.")
            orders = Order.objects.none()

    return render(request, 'orders/generate_reports.html', {
        'orders': orders
    })