document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Add fade-out class to the body before sending the request
    document.body.classList.add('fade-out');

    // Send login request
    fetch('http://localhost:8000/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Wait for the fade-out animation to complete before redirecting
            setTimeout(function() {
                alert('Login successful!');
                window.location.href = 'index.html'; // Change to your main page
            }, 1000); // 1000 ms corresponds to the duration of the fade-out animation
        } else {
            // If login fails, remove the fade-out class and show error
            document.body.classList.remove('fade-out');
            alert('Login failed: ' + data.message);
        }
    })
    .catch(error => {
        // Handle error
        console.error('Error:', error);
        document.body.classList.remove('fade-out'); // Ensure the fade-out is removed in case of error
        alert('An error occurred, please try again.');
    });
});
