from django import forms
from .models import Complaint

# ComplaintForm handles validation and creation of Complaint objects
class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['title', 'description', 'location']

    # Validate the title field
    def clean_title(self):
        title = self.cleaned_data.get("title")
        if not title or len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")
        if len(title) > 50:
            raise forms.ValidationError("Title must be at most 50 characters long.")
        return title

    # Validate the description field
    def clean_description(self):
        description = self.cleaned_data.get("description")
        if not description or len(description) < 10:
            raise forms.ValidationError("Description must be at least 10 characters long.")
        return description

    # Validate the location field
    def clean_location(self):
        location = self.cleaned_data.get("location")
        if not location:
            raise forms.ValidationError("Location is required.")
        return location

    # Save the complaint instance, assigning the user
    def save(self, commit=True, user=None):
        if not user:
            raise ValueError("User must be provided to save the complaint.")
        instance = super().save(commit=False)
        instance.user = user
        if commit:
            instance.save()
        return instance
