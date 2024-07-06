from django.shortcuts import render, redirect,HttpResponse,get_object_or_404
from .forms import *
import stripe  # Import the stripe library

from django.conf import settings
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from freelancer.models import *
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


def client_home(request):
    return render(request,'client_home.html')
def register_client(request):
    if request.method == 'POST':
        form = ClientRegistrationForm(data = request.POST)
        if form.is_valid():
            user = form.save()
            company_name = form.cleaned_data.get('company_name')
            # Create and save the Client profile
            Client.objects.create(user=user, company_name=company_name)
            return redirect('login_client')  # Redirect to the login page after successful registration
    else:
        form = ClientRegistrationForm()
    return render(request, 'register_client.html', {'form': form})

def login_client(request):
    if request.method == 'POST':
        form = ClientLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('client_dashboard')  
    else:
        form = ClientLoginForm()
    return render(request, 'client_login.html', {'form': form})



@login_required
def client_dashboard(request):
    client = Client.objects.get(user=request.user)

    my_projects = Project.objects.filter(client_id =request.user.id)
    return render(request, 'client_dashboard.html', {'client': client,'my_projects':my_projects})    


@login_required
def all_freelancers(request):
    freelancers = Freelancer.objects.all()
    return render(request,"all_freelancers.html",{'freelancers':freelancers})    


@login_required
def add_project(request):
    if request.method == "POST":
        form = AddProjectForm(data = request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.client = request.user
            project.save()
            return redirect('client_home')  # Redirect to client's dashboard or any other page after successful addition
    else:
        form = AddProjectForm()
    return render(request, 'add_project.html', {'form': form})

def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        project.delete()
        return redirect('client_dashboard')

    # Redirect to dashboard if the method is not POST (optional)
    return redirect('client_dashboard')



stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def process_payment(request, project_id):
    project = Project.objects.get(id=project_id)
    amount = int(project.budget * 100)  # Stripe expects the amount in cents

    intent = stripe.PaymentIntent.create(
        amount=amount,
        currency='usd',
        metadata={'project_id': project.id}
    )

    return render(request, 'process_payment.html', {
        'project': project,
        'client_secret': intent.client_secret,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY
    })

@csrf_exempt
def payment_confirmation(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        project_id = payment_intent['metadata']['project_id']
        project = Project.objects.get(id=project_id)
        Payment.objects.create(
            project=project,
            stripe_charge_id=payment_intent['id'],
            amount=project.budget
        )
        project.status = 'completed'
        project.save()

    return HttpResponse(status=200)
