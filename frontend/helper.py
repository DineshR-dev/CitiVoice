# Checks if a user is allowed to vote based on their complaints and votes within the current month.
def has_vote(user):
    from complaints.models import Complaint, ComplaintVote

    # Get the date range for the current month
    first_day, last_day = get_month_range()

    # Count the number of complaints and votes made by the user in the current month
    complaints = Complaint.objects.filter(
        created_at__range=(first_day, last_day), 
        user=user
    ).count()

    votes = ComplaintVote.objects.filter(
        voted_at__range=(first_day, last_day), 
        user=user
    ).count()

    # If the user has interactions (complaints + votes), they can't vote
    total_interactions = votes + complaints
    if total_interactions > 0:
        return False
    return True


# Returns the first and last days of the current month.
def get_month_range():
    from datetime import datetime, timedelta, time
    
    today = datetime.today()

    # First day of the current month
    first_day = datetime.combine(today.replace(day=1).date(), time.min)

    # First day of next month
    if today.month == 12:
        next_month = today.replace(year=today.year + 1, month=1, day=1)
    else:
        next_month = today.replace(month=today.month + 1, day=1)

    # Last day of the current month
    last_day = datetime.combine((next_month - timedelta(days=1)).date(), time.max)

    return first_day, last_day


# Checks if the user's profile is complete (location, fullname, and phone).
def is_profile_verified(user):
    if user.location and user.fullname and user.phone:
        return True
    return False


# Determines if a user can take a complaint in the current month (based on profile and taken complaints).
def can_take_complaint(user):
    from complaints.models import TakenComplaint
    
    # Check if the user's profile is verified
    profile_verified = is_profile_verified(user)
    if not profile_verified:
        return False

    # Get the date range for the current month
    first_day, last_day = get_month_range()
    
    # Count the number of complaints the user has taken this month
    taken_count = TakenComplaint.objects.filter(
        assigned_to=user, 
        taken_at__range=(first_day, last_day)
    ).count()

    # If the user has taken 2 or more complaints, they cannot take any more this month
    if taken_count >= 2:
        return False
    
    return True


# Retrieves statistics for a user, including the number of votes, complaints, and the taken ratio.
def get_user_statistics(user):
    from complaints.models import Complaint, ComplaintVote

    # Count the number of votes, complaints, and taken complaints/votes
    vote_count = ComplaintVote.objects.filter(user=user).count()
    complaint_count = Complaint.objects.filter(user=user).count()
    taken_complaint_count = Complaint.objects.filter(user=user).exclude(status='not_taken').count()
    taken_vote_count = ComplaintVote.objects.filter(user=user).exclude(complaint__status='not_taken').count()

    # Calculate the ratio of taken complaints and votes to total interactions (complaints + votes)
    taken_ratio = ((taken_complaint_count + taken_vote_count) / (vote_count + complaint_count) * 100) if complaint_count > 0 else 0

    # Return the counts and the ratio
    return vote_count, complaint_count, round(taken_ratio, 2)
