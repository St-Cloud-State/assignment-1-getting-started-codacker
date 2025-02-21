// Function to submit a new application
function submitApplication() {
    let name = document.getElementById("name").value;
    let zipcode = document.getElementById("zipcode").value;

    fetch('/api/apply', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, zipcode })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("applicationResponse").textContent = `Application ID: ${data.application_id}`;
    })
    .catch(error => console.error("Error:", error));
}

// Function to check application status
function checkStatus() {
    let appId = document.getElementById("appIdCheck").value;

    fetch(`/api/status/${appId}`)
    .then(response => response.json())
    .then(data => {
        document.getElementById("statusResult").textContent = data.status ? `Status: ${data.status}` : data.error;
    })
    .catch(error => console.error("Error:", error));
}

// Function to update application status
function updateStatus() {
    let appId = document.getElementById("appIdUpdate").value;
    let newStatus = document.getElementById("newStatus").value;

    fetch(`/api/update/${appId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("updateResponse").textContent = data.message;
    })
    .catch(error => console.error("Error:", error));
}
