// Check for SpeechRecognition support in the browser
window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();
recognition.interimResults = false;
recognition.lang = 'en-US'; // Language preference


// DOM elements
const transcriptOutput = document.getElementById('output');
const startBtn = document.getElementById('start-btn');
const wave = document.getElementById('wave');
const chatBox = document.getElementById('chat-box');
const responseDiv = document.getElementById('response'); // Define the response div

// Text-to-Speech variables
let voices = [];
const synth = window.speechSynthesis;

// Fetch available voices
function loadVoices() {
    voices = synth.getVoices();
    // Check if voices are available immediately or wait for the 'voiceschanged' event
    if (voices.length) {
        selectVoice(); // Call the function to set the preferred voice
    }
}

// Set the desired voice
function selectVoice() {
    // You can change the voice name below to match your desired voice
    const preferredVoiceName = "Google US English"; // Change to desired voice name
    const preferredVoice = voices.find(voice => voice.name === preferredVoiceName);
    
    if (preferredVoice) {
        // Store the preferred voice globally for later use
        window.preferredVoice = preferredVoice;
    } else {
        console.warn("Preferred voice not found, defaulting to the first available voice.");
        window.preferredVoice = voices[0]; // Fallback to the first available voice
    }
}

const chatMessages = document.createElement('div');
chatMessages.classList.add('chat-messages');
chatBox.appendChild(chatMessages);

// Function to add message to chat box
function addMessageToChatBox(message, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('chat-message');

    if (sender === 'user') {
        messageDiv.classList.add('user-message');
    } else {
        messageDiv.classList.add('assistant-message');
    }
    // Set the message content
    const messageText = document.createElement('p');
    messageText.textContent = message;
    messageDiv.appendChild(messageText);

    // Append the message to the chat box
    chatMessages.appendChild(messageDiv);

    // Scroll to the bottom of the chat box
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Add initial message to chat box

// When user clicks start
startBtn.addEventListener('click', () => {
    transcriptOutput.textContent = "• Listening...";
    recognition.start();
    wave.style.animationPlayState = 'running'; // Start the pulse animation
    startBtn.disabled = true; // Disable button while listening
});

// When speech is detected
recognition.addEventListener('result', (e) => {
    const transcript = e.results[0][0].transcript;
    addMessageToChatBox(transcript, 'user');
    handleResponse(transcript);
    
});
// When recognition ends
recognition.addEventListener('end', () => {
    wave.style.animationPlayState = 'paused'; // Stop the pulse animation
    startBtn.disabled = false; // Re-enable the button
});

// Command handling logic
function handleResponse(transcript) {
    try {
        // Send request to FastAPI backend
        fetch('http://localhost:8000/process_query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: transcript })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('Error:', data.error);
                addMessageToChatBox(data.error, 'assistant');
            } else {
                const responseText = data.response; // Define responseText variable
                responseDiv.innerHTML = responseText; // Update the response div
                addMessageToChatBox(responseText, 'assistant');
                speakResponse(responseText);
            }
            
        
        })
        .catch(error => console.error('Error:', error));
    } catch (error) {
        console.error('Error handling response:', error);
    }
}

// Text-to-Speech function
function speakResponse(text) {
    if (!text) {
        console.error("No text to speak");
        return;
    }

    try {
        const utterance = new SpeechSynthesisUtterance(text);

        if (!window.preferredVoice && !voices.length) {
            console.error("No voices available");
            return;
        }

        utterance.voice = window.preferredVoice || voices[1]; // Use the preferred voice or fallback
        utterance.pitch = 1.2; // Slightly higher pitch for a more natural female tone
        utterance.rate = 0.9; // Normal speed
        utterance.volume = 1; // Maximum volume

        utterance.onstart = function(event) {
            console.log("Speech started");
        };

        utterance.onend = function(event) {
            console.log("Speech ended");
        };

        utterance.onerror = function(event) {
            console.error("Speech error", event);
        };

        console.log("Speaking response:");
        console.log(text);
        console.log(utterance);
        console.log(window.speechSynthesis.pending);
        console.log(window.speechSynthesis.speaking);
        console.log(window.speechSynthesis.paused);

        // Add a 1-second delay before speaking the text
        setTimeout(() => {
            window.speechSynthesis.speak(utterance);
        }, );
    } catch (error) {
        console.error("Error speaking response:", error);
    }
}

// Function to greet the user according to the time
function greetUser() {
    const currentTime = new Date().getHours();
    let greeting = '';

    if (currentTime < 12) {
        greeting = 'Good morning!';
    } else if (currentTime < 18) {
        greeting = 'Good afternoon!';
    } else {
        greeting = 'Good evening!';
    }

    addMessageToChatBox(greeting, 'assistant');
    speakResponse(greeting);
}

greetUser()

// Load voices when the page is ready
window.addEventListener('load', () => {
    loadVoices();
    // Listen for voices changed event
    speechSynthesis.onvoiceschanged = loadVoices;
    document.getElementById('theme-toggle').addEventListener('click', function() {
        document.body.classList.toggle('dark-mode');
        // Add theme toggle functionality here
    });
});