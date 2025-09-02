from django.db import models
from django.forms import ValidationError

from users.models import users as User
from core.models import Location

from django.utils.text import slugify
from django.urls import reverse


# Complaint model stores citizen complaints and their status
class Complaint(models.Model):
    STATUS_CHOICES = [
        ('not_taken', 'Not Taken'),
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_taken')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="complaints")
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.status})"
    
    # Ensure status is valid before saving
    def clean(self):
        valid_choices = [choice[0] for choice in self.STATUS_CHOICES]
        if self.status not in valid_choices:
            raise ValidationError({'status': 'Invalid status update. Must be within defined choices.'})

    # Auto-generate slug from title if not set
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    # Get URL for complaint detail page
    def get_absolute_url(self):
        return reverse("frontend:complaint", kwargs={"slug": self.slug})

# ComplaintVote model tracks votes on complaints by users
class ComplaintVote(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="complaint_votes")
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("complaint", "user")  # one user can vote only once per complaint

    def __str__(self):
        return f"{self.user.username} voted on {self.complaint.title}"

# TakenComplaint model assigns complaints to admins for handling
class TakenComplaint(models.Model):
    complaint = models.OneToOneField("Complaint", on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    taken_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Task: {self.complaint.title} → {self.assigned_to.username}"
