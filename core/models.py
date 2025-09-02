from django.db import models

# Location model represents a physical or administrative area
class Location(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        permissions = (
            ('admin_perm', 'admin can take complaints'),
        )

    def __str__(self):
        return self.name

# complaints_handler model maps admins to locations they manage
class complaints_handler(models.Model):
    admin = models.ForeignKey("users.users", on_delete=models.CASCADE, related_name="locations")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="admins")

    class Meta:
        unique_together = ('admin', 'location')  # prevent duplicate mapping

    def __str__(self):
        return f"{self.admin.username} -> {self.location.name}"