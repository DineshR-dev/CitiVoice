from django.contrib import admin
from .models import Complaint,ComplaintVote,TakenComplaint

# Register your models here.
admin.site.register(Complaint)
admin.site.register(ComplaintVote)
admin.site.register(TakenComplaint)