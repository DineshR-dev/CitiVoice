// User related functions

// Signup function with validation and AJAX
function signup() {
    const username = $('#username').val();
    const email = $('#email').val();
    const password = $('#password').val();
    const confirm_password = $('#confirmPassword').val();
    const csrf_token = getcsrf_token();
    const signup_url = $('#signupButton').data('signup-url');

    $('#signupAlert').hide().removeClass("alert-danger alert-success");

    if (!username_validation(username)) {
        $('#signupAlert').text("Invalid username.").show().addClass("alert-danger");
        return;
    }
    if (!email_validation(email)) {
        $('#signupAlert').text("Invalid email.").show().addClass("alert-danger");
        return;
    }
    if (!password_validation(password)) {
        $('#signupAlert').text("Invalid password.").show().addClass("alert-danger");
        return;
    }
    if (!password_validation(confirm_password)) {
        $('#signupAlert').text("Invalid confirm password.").show().addClass("alert-danger");
        return;
    }
    if (password !== confirm_password) {
        $('#signupAlert').text("Passwords do not match.").show().addClass("alert-danger");
        return;
    }

    $.ajax({
        url: signup_url,
        type: "POST",
        data: {
            username: username,
            email: email,
            password: password,
            confirm_password: confirm_password,
            csrfmiddlewaretoken: csrf_token
        },
        success: function(response) {
            if (response.status === "success") {
                $('#signupAlert').show().removeClass("alert-danger").addClass("alert-success").text("Signup successful!");
                setTimeout(() => {
                    window.location.href = "/login/";
                }, 2000);
            } else {
                const firstKey = Object.keys(response.message)[0];
                const firstError = response.message[firstKey][0];
                $('#signupAlert').show().addClass("alert-danger").removeClass("alert-success").text(firstError);
            }
        }
    });
}

// Login function with validation and AJAX
function login() {
    const username = $('#username').val();
    const password = $('#password').val();
    const login_url = $('#loginButton').data('login-url');
    const csrf_token = getcsrf_token();

    $('#loginAlert').hide().removeClass("alert-danger alert-success");

    if (!username_validation(username)) {
        $('#loginAlert').text("Invalid username.").show().addClass("alert-danger");
        return;
    }

    if (!password_validation(password)) {
        $('#loginAlert').text("Invalid password.").show().addClass("alert-danger");
        return;
    }

    $.ajax({
        url: login_url,
        type: "POST",
        data: {
            username: username,
            password: password,
            csrfmiddlewaretoken: csrf_token
        },
        success: function(response) {
            if (response.status === "success") {
                $('#loginAlert').show().removeClass("alert-danger").addClass("alert-success").text("Login successful!");
                setTimeout(() => {
                    if (response.profile_verified) {
                        window.location.href = "/";
                    } else {
                        window.location.href = "/profile-update/";
                    }
                }, 2000);
            } else {
                const firstKey = Object.keys(response.message)[0];
                const firstError = response.message[firstKey][0];
                $('#loginAlert').show().addClass("alert-danger").removeClass("alert-success").text(firstError);
            }
        }
    });
}

// Update profile function with validation and AJAX
function updateProfile() {
    const username = $('#username').val();
    const full_name = $('#full_name').val();
    const phone_number = $('#phone_number').val();
    const location = $('#location').val();
    const csrf_token = getcsrf_token();
    const url = $('#updateProfileBtn').data('url');

    $('#profileUpdateAlert').hide().removeClass("alert-success alert-danger").text("");

    if (!username_validation(username)) {
        $('#profileUpdateAlert').show().addClass("alert-danger").removeClass("alert-success").text("Invalid username.");
        return;
    }

    if (!full_name_validation(full_name)) {
        $('#profileUpdateAlert').show().addClass("alert-danger").removeClass("alert-success").text("Invalid full name.");
        return;
    }

    if (!phone_number_validation(phone_number)) {
        $('#profileUpdateAlert').show().addClass("alert-danger").removeClass("alert-success").text("Invalid phone number.");
        return;
    }

    if (!location_validation(location)) {
        $('#profileUpdateAlert').show().addClass("alert-danger").removeClass("alert-success").text("Invalid location.");
        return;
    }

    $.ajax({
        url: url,
        type: "POST",
        data: {
            fullname: full_name,
            username: username,
            phone: phone_number,
            location: location,
            csrfmiddlewaretoken: csrf_token
        },
        success: function(response) {
            if (response.status === "success") {
                $('#profileUpdateAlert').show().removeClass("alert-danger").addClass("alert-success").text("Profile updated successfully!");
                setTimeout(() => {
                    window.location.href = "/profile/";
                }, 2000);
            } else {
                const firstKey = Object.keys(response.message)[0];
                const firstError = response.message[firstKey][0];
                $('#profileUpdateAlert').show().addClass("alert-danger").removeClass("alert-success").text(firstError);
            }
        }
    });
}