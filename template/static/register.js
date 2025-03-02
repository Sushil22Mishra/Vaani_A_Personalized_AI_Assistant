document.getElementById('register-form').addEventListener('submit', async function (event) {
    event.preventDefault(); // Prevent default form submission

    // Get form data
    const name = document.getElementById('new-name').value;
    const password = document.getElementById('new-password').value;
    const confirmPassword = document.getElementById('confirm-password').value;

    // Validate form fields
    if (!name || !password || !confirmPassword) {
        console.error('All fields are required!'); // Log validation failure
        return;
    }

    // Check if passwords match
    if (password !== confirmPassword) {
        console.error('Passwords do not match'); // Log password mismatch
        return;
    }

    // Get the profile picture URL from the user input
    const profilePicInput = document.getElementById('profile-input');
    let profilePicUrl = '';

    if (profilePicInput.files && profilePicInput.files[0]) {
        const reader = new FileReader();
        reader.onload = async function (e) {
            profilePicUrl = e.target.result; // Store the base64 string for the profile picture
            // Send the data to the server
            await sendRegisterData(name, password, profilePicUrl);
        };
        reader.readAsDataURL(profilePicInput.files[0]);
    } else {
        // If no profile picture is chosen, use a default or empty value
        await sendRegisterData(name, password, profilePicUrl);
    }
});

// Function to send data to FastAPI
async function sendRegisterData(name, password, profilePicUrl) {
    try {
        const response = await fetch('http://localhost:8000/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, password, profile_pic: profilePicUrl }) // Ensure the key is correct
        });

        const result = await response.json();
        if (response.ok) {
            // Redirect to vaani page after registration
            window.location.href = 'vaani.html'; 
        } else {
            console.error(result.detail || 'An error occurred during registration.'); // Log registration failure
        }
    } catch (error) {
        console.error('Error:', error);
        console.error('An error occurred while registering.'); // Log registration error
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