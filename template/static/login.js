document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission

    const username = document.getElementById('username-input').value;
    const password = document.getElementById('password').value;

    // Add fade-out class to the body before sending the request
    document.body.classList.add('fade-out');

    // Send login request
    fetch('http://localhost:8000/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name: username, password: password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Wait for the fade-out animation to complete before redirecting
            setTimeout(function() {
                window.location.href = 'vaani.html'; // Redirect to vaani page
            }, 1000); // Optional: Adjust the delay if needed
        } else {
            // If login fails, remove the fade-out class and show error
            document.body.classList.remove('fade-out');
            alert('Login failed: ' + data.message); // Keep this alert for login failure
        }
    })
    .catch(error => {
        // Handle error
        console.error('Error:', error);
        document.body.classList.remove('fade-out'); // Ensure the fade-out is removed in case of error
        alert('An error occurred, please try again.'); // Keep this alert for errors
    });
});