document.getElementById('register-form').addEventListener('submit', async function (event) {
    event.preventDefault(); // Prevent default form submission

    // Get form data
    const name = document.getElementById('new-name').value;
    const password = document.getElementById('new-password').value;
    const confirmPassword = document.getElementById('confirm-password').value;

    // Validate form fields
    if (!name || !password || !confirmPassword) {
        alert('All fields are required!');
        return;
    }

    // Check if passwords match
    if (password !== confirmPassword) {
        alert('Passwords do not match');
        return;
    }

    // Get the profile picture URL from the user input
    const profilePicInput = document.getElementById('profile-input');
    let profilePicUrl = '';

    if (profilePicInput.files && profilePicInput.files[0]) {
        const reader = new FileReader();
        reader.onload = function (e) {
            profilePicUrl = e.target.result; // Store the base64 string for the profile picture
            // Send the data to the server
            sendRegisterData(name, password, profilePicUrl);
        };
        reader.readAsDataURL(profilePicInput.files[0]);
    } else {
        // If no profile picture is chosen, use a default or empty value
        sendRegisterData(name, password, profilePicUrl);
    }
});

// Function to send registration data to the server
async function sendRegisterData(name, password, profilePicUrl) {
    try {
        const response = await fetch('http://localhost:5000/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, password, profilePicUrl }),
        });

        const result = await response.json();
        if (response.ok) {
            alert(result.message); // Success message
            window.location.href = 'login.html'; // Redirect to login
        } else {
            alert(result.message); // Error message
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while registering.');
    }
}

// Handle profile picture click event to select a picture
const profilePic = document.getElementById('profile-pic');
const profileInput = document.getElementById('profile-input');

profilePic.addEventListener('click', function() {
    profileInput.click(); // Trigger the file input when the profile picture is clicked
});

profileInput.addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            profilePic.style.backgroundImage = `url(${e.target.result})`;
            profilePic.textContent = ''; // Remove the "+" text when an image is selected
            profilePic.style.backgroundSize = 'cover';
            profilePic.style.backgroundPosition = 'center';
        };
        reader.readAsDataURL(file);
    }
});

document.getElementById('register-form').addEventListener('submit', async function (event) {
    event.preventDefault();

    // Get form data
    const name = document.getElementById('new-name').value;
    const password = document.getElementById('new-password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    const profilePicInput = document.getElementById('profile-input');

    // Check if passwords match
    if (password !== confirmPassword) {
        alert('Passwords do not match');
        return;
    }

    let profilePicUrl = "";

    // Convert profile picture to Base64
    if (profilePicInput.files.length > 0) {
        const reader = new FileReader();
        reader.onload = async function (e) {
            profilePicUrl = e.target.result;
            await sendRegisterData(name, password, profilePicUrl);
        };
        reader.readAsDataURL(profilePicInput.files[0]);
    } else {
        await sendRegisterData(name, password, profilePicUrl);
    }
});

// Function to send data to FastAPI
async function sendRegisterData(name, password, profilePicUrl) {
    try {
        const response = await fetch('http://localhost:8000/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, password, profilePic: profilePicUrl })
        });

        const result = await response.json();
        if (response.ok) {
            alert(result.message);
            window.location.href = 'login.html'; // Redirect to login page
        } else {
            alert(result.detail);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while registering.');
    }
}