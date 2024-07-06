from django.shortcuts import render, redirect,HttpResponse
from .forms import *
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from client.models import *
from.models import *
from django.shortcuts import get_object_or_404
from django.contrib import messages

def freelancer_home(request):
    return render(request,"freelancer_home.html")
def register_freelancer(request):
    if request.method == 'POST':
        form = FreelancerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            experience = form.cleaned_data.get('experience')
            skills = form.cleaned_data.get('skills')
            # Create and save the Freelancer profile
            Freelancer.objects.create(user=user, experience=experience, skills=skills)
            return redirect('login_freelancer')
    else:
        form = FreelancerRegistrationForm()
    return render(request, 'register_freelancer.html', {'form': form})


def login_freelancer(request):
    if request.method == 'POST':
        form = FreelancerLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('freelancer_dashboard')  # Redirect to freelancer dashboard after login
    else:
        form = FreelancerLoginForm()
    return render(request, 'freelancer_login.html', {'form': form})



@login_required
def freelancer_dashboard(request):
    freelancer = get_object_or_404(Freelancer, user=request.user)
    projects_done = Project.objects.filter(freelancer=freelancer,status = 'Accepted')
    project_count = freelancer.get_project_count()
    print(freelancer)
    return render(request, 'freelancer_dashboard.html', {'freelancer': freelancer,'projects_done': projects_done,'project_count': project_count})

@login_required
def all_clients(request):
    clients = Client.objects.all()
    return render(request,'all_clients.html',{'clients':clients})

@login_required
def all_projects(request):
    projects = Project.objects.all()
    return render(request,'all_projects.html',{'projects':projects})


def update_project_status(request):
    if request.method == 'POST':
        project_id = request.POST.get('project_id')
        action = request.POST.get('status')
        
        try:
            project = Project.objects.get(id=project_id)
            if action == 'accept':
                project.status = 'accepted'
                messages.success(request, 'Project accepted successfully.')
            elif action == 'reject':
                project.status = 'rejected'
                messages.success(request, 'Project rejected successfully.')
            project.save()
        except Project.DoesNotExist:
            messages.error(request, 'Project does not exist.')
    
    return redirect('all_projects')



