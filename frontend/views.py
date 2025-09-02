from django.contrib import messages
from django.forms import ValidationError
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.core.paginator import Paginator
from frontend import helper
# user app imports
from users.models import users as User
from users.forms import ProfileUpdateForm, SignUpForm, LoginForm

# core app imports
from core.models import Location,complaints_handler

# complaints app imports
from complaints.forms import ComplaintForm
from complaints.models import Complaint,ComplaintVote, TakenComplaint


# Main view for the index page.
class Index(View):
    def get(self, request):
        first_day, last_day = helper.get_month_range()
        complaints_qs = Complaint.objects.filter(
            created_at__date__range=(first_day, last_day)
        ).annotate(
            vote_count=Count('votes')
        ).order_by('-vote_count')

        location_filter = request.GET.get('location_filter', None)
        
        if not request.user.is_authenticated:
            complaints_qs = complaints_qs[:2]
        elif location_filter:
            complaints_qs = complaints_qs.filter(location=location_filter)

        paginator = Paginator(complaints_qs, 10)
        page_number = request.GET.get('page', 1)
        try:
            complaints_page = paginator.get_page(page_number)
        except:
            complaints_page = paginator.get_page(1)

        if not request.user.is_authenticated:
            context = {'complaints': complaints_page, 'has_vote': False, 'locations': Location.objects.all()}
            return render(request, 'frontend/index.html', context)

        assigned_location = complaints_handler.objects.filter(admin=request.user).first()
        
        context = {
            'complaints': complaints_page,
            'has_vote': helper.has_vote(request.user),
            'locations': Location.objects.all(),
            'user_location': assigned_location.location if assigned_location else None
        }

        # Handle AJAX request for pagination separately
        if request.GET.get('is_ajax'):
            # Render only the complaints list partial as HTML snippet
            html = render(request, 'frontend/includes/complaints_list_partial.html', context).content.decode('utf-8')
            return JsonResponse({'html': html})

        # Normal page load rendering full template
        
        return render(request, 'frontend/index.html', context)

# Sign up view
class signup(View):
    def get(self, request):
        return render(request, "frontend/signup.html")

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"]
            )
            return JsonResponse({"status": "success"})
        return JsonResponse({"status": "error", "message": form.errors})

# Login view
class login(View):
    def get(self, request):
        return render(request, "frontend/login.html")

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            auth_login(request, form.cleaned_data["user"])
            profile_verified = helper.is_profile_verified(request.user)
            return JsonResponse({"status": "success", "profile_verified": profile_verified})
        return JsonResponse({"status": "error", "message": form.errors})

# Logout view
class logout(View):
    def get(self, request):
        auth_logout(request)
        return redirect('frontend:index')

# Profile view
class profile(LoginRequiredMixin,View):
    login_url = 'frontend:login'

    def get(self, request):
        user = User.objects.filter(id=request.user.id).first()
        profile_picture_text = ''.join([i[0] for i in user.fullname.split(" ")])

        vote_count, complaint_count, taken_ratio = helper.get_user_statistics(user)
        context = {
            'user': user,
            'profile_picture_text': profile_picture_text,
            'total_vote_count': vote_count,
            'total_complaint_count': complaint_count,
            'taken_ratio': taken_ratio
        }

        return render(request, 'frontend/profile.html', context)

# Profile update view
class profile_update(LoginRequiredMixin,View):
    login_url = 'frontend:login'

    def get(self, request):
        user = User.objects.filter(id=request.user.id).first()
        location = Location.objects.all()
        return render(request, 'frontend/profile_update.html', {'user': user, 'location': location})

    def post(self, request):
        user = User.objects.filter(id=request.user.id).first()
        form = ProfileUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return JsonResponse({"status": "success"})
        return JsonResponse({"status": "error", "message": form.errors})    

# Add complaint view
class add_complaint(LoginRequiredMixin,View):
    login_url = 'frontend:login'
    
    def get(self, request):
        profile_verified = helper.is_profile_verified(request.user)
        if not profile_verified:
            messages.warning(request, "Please update your profile first.")
            return redirect('frontend:profile_update')

        has_vote = helper.has_vote(request.user)
        location = Location.objects.all()
        if not has_vote:
            return redirect('frontend:index')
        
        return render(request, 'frontend/add_complaint.html', {'location': location})

    def post(self, request):
        has_vote = helper.has_vote(request.user)
        if not has_vote:
            return JsonResponse({"status": "error", "message": "You have no points left."})

        user = User.objects.filter(id=request.user.id).first()
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(user=user)
            return JsonResponse({"status": "success"})
        return JsonResponse({"status": "error", "message": form.errors})

# Vote complaint view
class vote_complaint(View):

    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({"status": "error", "message": "User not authenticated."})
        
        profile_verified = helper.is_profile_verified(request.user)
        if not profile_verified:
            return JsonResponse({"status": "error", "message": "Profile not verified. Please update your profile."})

        can_take_complaint = helper.can_take_complaint(request.user)
        if not can_take_complaint:
            return JsonResponse({"status": "error", "message": "You have already taken 2 complaints."})

        user = request.user
        complaint_id = request.POST.get("complaint_id")
        complaint = Complaint.objects.filter(id=complaint_id).first()
        if not complaint:
            return JsonResponse({"status": "error", "message": "Complaint not found."})

        # Logic to handle voting
        if TakenComplaint.objects.filter(complaint=complaint).exists():
            return JsonResponse({"status": "error", "message": "This complaint has already been taken."})

        vote = ComplaintVote.objects.create(user=user, complaint=complaint)

        return JsonResponse({"status": "success"})

# Display complaint details
class complaint(LoginRequiredMixin,View):
    login_url = 'frontend:login'

    def get(self, request, slug):
        complaint = Complaint.objects.filter(slug=slug).first()
        if not complaint:
            return render(request, 'frontend/404.html')

        return render(request, 'frontend/complaint.html', {'complaint': complaint})

# Take complaint into action view
class take_complaint(View):
    def post(self, request):

        # 1. login check
        if not request.user.is_authenticated:
            return JsonResponse({"status": "error", "message": "User not authenticated."})

        # 2. complaint handler permission check
        if not request.user.has_perm('core.admin_perm'):
            return JsonResponse({"status": "error", "message": "You do not have permission to take this complaint."})

        # 3. profile verification check
        profile_verified = helper.is_profile_verified(request.user)
        if not profile_verified:
            return JsonResponse({"status": "error", "message": "Profile not verified. Please update your profile."})

        # 4. complaint taking limit check
        can_take_complaint = helper.can_take_complaint(request.user)
        if not can_take_complaint:
            return JsonResponse({"status": "error", "message": "You have no points left."})

        user = request.user
        complaint_id = request.POST.get("complaint_id")
        complaint = Complaint.objects.filter(id=complaint_id).first()

        # 5. Complaint existence check
        if not complaint:
            return JsonResponse({"status": "error", "message": "Complaint not found."})

        # 6. Complaint taking status check
        if TakenComplaint.objects.filter(complaint=complaint).exists():
            return JsonResponse({"status": "error", "message": "You have already taken this complaint."})

        # insert complaint taking record and update status
        TakenComplaint.objects.create(assigned_to=user, complaint=complaint)
        complaint.status = 'pending'
        complaint.save()
        return JsonResponse({"status": "success"})

# Complaint records view
class complaint_records(LoginRequiredMixin, View):
    login_url = 'frontend:login'
    def get(self, request):

        locations = Location.objects.all()
        tasks = TakenComplaint.objects.all()

        date_filter = request.GET.get('date_filter', None)
        if date_filter:
            tasks = tasks.filter(complaint__created_at__range=(date_filter['firstDate'], date_filter['lastDate']))

        location_filter = request.GET.get('location_filter', None)
        if location_filter:
            tasks = tasks.filter(complaint__location=location_filter)

        status_filter = request.GET.get('status_filter', None)
        if status_filter:
            tasks = tasks.filter(complaint__status=status_filter)

        paginator = Paginator(tasks, 2)
        page_number = request.GET.get('page', 1)
        try:
            tasks_page = paginator.get_page(page_number)
        except:
            tasks_page = paginator.get_page(1)

        if request.GET.get('is_ajax'):
            # Render only the complaints list partial as HTML snippet
            html = render(request, 'frontend/includes/complaints_taken_partial.html', {'locations': locations, 'tasks': tasks_page}).content.decode('utf-8')
            return JsonResponse({'html': html})
            

        return render(request, 'frontend/complaint_records.html', {'locations': locations, 'tasks': tasks_page})

# Update complaint status view
class update_complaint_status(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({"status": "error", "message": "User not authenticated."})
        

        if not request.user.has_perm('core.admin_perm'):
            return JsonResponse({"status": "error", "message": "You do not have permission to update complaints."})

        complaint_id = request.POST.get("complaint_id")
        status = request.POST.get("status")

        take_complaint = TakenComplaint.objects.filter(id=complaint_id).first()
        if not take_complaint:
            return JsonResponse({"status": "error", "message": "Complaint not found."})

        complaint = take_complaint.complaint
        complaint.status = status
        try:
            complaint.clean()
        except ValidationError as e:
            return JsonResponse({"status": "error", "message": e.message_dict.get('status', ['Invalid status update.'])[0]})

        complaint.save()

        return JsonResponse({"status": "success"})
    

# How it works view
class how_it_works(View):
    def get(self, request):
        return render(request, 'frontend/how_it_works.html')