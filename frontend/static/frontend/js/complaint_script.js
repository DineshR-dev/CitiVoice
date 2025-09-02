// Complaint related AJAX functions for CitiVoice

// Add a new complaint via AJAX
function addComplaint() {
    const title = $('#title').val();
    const description = $('#description').val();
    const location = $('#location').val();
    const url = $('#addComplaintBtn').data('url');
    const csrf_token = getcsrf_token();

    $('#addComplaintAlert').hide().removeClass("alert-success alert-danger").text("");
    if (!title || !description || !location) {
        $('#addComplaintAlert').show().addClass("alert-danger").removeClass("alert-success").text("All fields are required.");
        return;
    }

    if (title.length > 50) {
        $('#addComplaintAlert').show().addClass("alert-danger").removeClass("alert-success").text("Title must be at most 50 characters long.");
        return;
    }

    $.ajax({
        url: url,
        type: "POST",
        data: {
            title: title,
            description: description,
            location: location,
            csrfmiddlewaretoken: csrf_token
        },
        success: function(response) {
            if (response.status === "success") {
                $('#addComplaintAlert').show().removeClass("alert-danger").addClass("alert-success").text("Complaint submitted successfully!");
                setTimeout(() => {
                    window.location.href = "/";
                }, 2000);
            } else {
                const firstKey = Object.keys(response.message)[0];
                const firstError = response.message[firstKey][0];
                $('#addComplaintAlert').show().addClass("alert-danger").removeClass("alert-success").text(firstError);
            }
        }
    });
}

// Vote for a complaint via AJAX
function voteComplaint(complaintId) {
    if (!confirm("Are you sure you want to vote for this complaint?")) {
        return;
    }
    const url = $('#voteComplaintURL').val();
    const csrf_token = getcsrf_token();

    $.ajax({
        url: url,
        type: "POST",
        data: {
            complaint_id: complaintId,
            csrfmiddlewaretoken: csrf_token
        },
        success: function(response) {
            if (response.status === "success") {
                window.location.href = "/";
            } else {
                alert(response.message);
            }
        }
    });
}

// Assign a complaint to an admin via AJAX
function takeComplaint(complaintId) {
    if (!confirm("Are you sure you want to take this complaint?")) {
        return;
    }

    const url = $('#takeComplaintURL').val();
    const csrf_token = getcsrf_token();

    $.ajax({
        url: url,
        type: "POST",
        data: {
            complaint_id: complaintId,
            csrfmiddlewaretoken: csrf_token
        },
        success: function(response) {
            if (response.status === "success") {
                window.location.href = "/";
            } else {
                alert(response.message);
            }
        }
    });
}

// Show status update dropdown or save new status
function showStatusUpdate(complaintId) {
    let editing = $(`#statusUpdateBtn${complaintId}`).attr('editing');
    if (editing == 'false' || !editing) {
        const statusBadge = $(`#statusBadge${complaintId}`);
        const currentStatus = statusBadge.text();

        const $select = $('<select>', {
            id: `statusSelect${complaintId}`,
            class: 'form-select form-select-sm w-75',
        });
        const statuses = { 'Pending': 'pending', 'Active': 'active', 'Completed': 'completed' };
        Object.entries(statuses).forEach(([text, value]) => {
            $select.append($('<option>', {
                value: value,
                text: text,
                selected: text === currentStatus
            }));
        });
        statusBadge.replaceWith($select);
        $(`#statusUpdateBtn${complaintId}`).text('Save');
        $(`#statusUpdateBtn${complaintId}`).attr('editing', true);
    } else {
        // Save new status
        const $select = $(`#statusSelect${complaintId}`);
        const newStatus = $select.val();

        let new_style = 'badge bg-warning';
        if (newStatus == 'active') {
            new_style = 'badge bg-info';
        } else if (newStatus == 'completed') {
            new_style = 'badge bg-success';
        }
        const $newBadge = $('<span>', {
            id: `statusBadge${complaintId}`,
            class: new_style,
            text: newStatus.charAt(0).toUpperCase() + newStatus.slice(1)
        });

        $select.replaceWith($newBadge);
        $(`#statusUpdateBtn${complaintId}`).text('Update');
        $(`#statusUpdateBtn${complaintId}`).attr('editing', false);
        updateStatus(complaintId, newStatus);
    }
}

// Update complaint status via AJAX
function updateStatus(complaintId, newStatus) {
    const csrf_token = getcsrf_token();
    $.ajax({
        url: '/update-complaint-status/',
        type: 'POST',
        data: {
            'complaint_id': complaintId,
            'status': newStatus,
            'csrfmiddlewaretoken': csrf_token
        },
        success: function(response) {
            if (response.status === "success") {
                alert('Status updated successfully!');
            } else {
                alert(response.message);
            }
        }
    });
}