// General validation functions for user input

function username_validation(username) {
    // Username must be at least 5 characters and alphanumeric
    if (username.length < 5) {
        return false;
    }
    if (!/^[a-zA-Z0-9]+$/.test(username)) {
        return false;
    }
    return true;
}

function email_validation(email) {
    // Basic email format validation
    let emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailPattern.test(email);
}

function password_validation(password) {
    // Password must be at least 8 characters
    if (password.length < 8) {
        return false;
    }
    return true;
}

function full_name_validation(full_name) {
    // Full name must be at least 5 characters and only letters/spaces
    if (full_name.length < 5) {
        return false;
    }
    return /^[a-zA-Z\s]+$/.test(full_name);
}

function phone_number_validation(phone_number) {
    // Phone number must be exactly 10 digits
    if (phone_number.length !== 10) {
        return false;
    }
    return /^[0-9]+$/.test(phone_number);
}

function location_validation(location) {
    // Location must not be empty
    return location.length > 0;
}

// Get CSRF token from cookies
function getcsrf_token() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith("csrftoken=")) {
                cookieValue = cookie.substring("csrftoken=".length);
                break;
            }
        }
    }
    return cookieValue;
}

// Fetch complaints for a given page (AJAX)
function getComplaints(pageNumber) {
    const location_filter = $('#filter').val();
    if ($('#is_user_login').val() !== 'true') {
        window.location.href = "/login";
    }
    $.ajax({
        url: window.location.href,
        method: "GET",
        data: { page: pageNumber, is_ajax: true, location_filter: location_filter },
        success: function (data) {
            $("#complaints-list").html(data.html);
        }
    });
}

// Fetch taken complaints for a given page (AJAX)
function getTakenComplaints(pageNumber) {
    const status_filter = $('#status-filter').val();
    const location_filter = $('#location-filter').val();

    const data = {
        page: pageNumber,
        is_ajax: true,
        status_filter: status_filter,
        location_filter: location_filter
    };
    $.ajax({
        url: window.location.href,
        type: "GET",
        data: data,
        success: function(response) {
            $('#complaints-list').html(response.html);
        }
    });
}
