document.getElementById('register-form').addEventListener('submit', async function (event) { 
    event.preventDefault(); // Prevent default form submission

    const name = document.getElementById('new-name').value;
    const password = document.getElementById('new-password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    const profilePicInput = document.getElementById('profile-input');
    
    // Validation checks
    if (!name || !password || !confirmPassword) {
        console.error('All fields are required!');
        return;
    }

    if (password !== confirmPassword) {
        console.error('Passwords do not match');
        return;
    }

    // Get profile picture file (if selected)
    const profilePicFile = profilePicInput.files[0] || null; 

    // Send form data to the server
    await sendRegisterData(name, password, profilePicFile);
});

// Function to send data to FastAPI
async function sendRegisterData(name, password, profilePic) {
    const formData = new FormData();
    formData.append("name", name);
    formData.append("password", password);
    if (profilePic) {
        formData.append("profile_pic", profilePic);
    }

    try {
        const response = await fetch("http://localhost:8000/register", {
            method: "POST",
            body: formData,
            redirect: "follow", // Ensures fetch follows redirects
        });

        if (response.redirected) {
            window.location.href = response.url; // Redirect manually
        } else {
            const result = await response.json();
            alert(result.detail || "An error occurred during registration.");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("An error occurred while registering.");
    }
}



// Handle profile picture selection and preview
const profilePic = document.getElementById('profile-pic');
const profileInput = document.getElementById('profile-input');

profilePic.addEventListener('click', function() {
    profileInput.click(); // Open file selection on profile picture click
});

profileInput.addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            profilePic.style.backgroundImage = `url(${e.target.result})`;
            profilePic.textContent = ''; // Remove "+" symbol
            profilePic.style.backgroundSize = 'cover';
            profilePic.style.backgroundPosition = 'center';
        };
        reader.readAsDataURL(file);
    }
});