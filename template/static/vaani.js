// Check for SpeechRecognition support in the browser
window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();
recognition.interimResults = false;
recognition.lang = 'en-US';
recognition.continuous = true; // Enable continuous listening

// DOM elements
const transcriptOutput = document.getElementById('output');
const startBtn = document.getElementById('start-btn');
const wave = document.getElementById('wave');
const chatBox = document.getElementById('chat-box');
const responseDiv = document.getElementById('response');

// Text-to-Speech variables
let voices = [];
const synth = window.speechSynthesis;

let isListening = false;
let userRequestedStop = false;

// Load voices properly using a Promise
function loadVoicesProperly() {
    return new Promise((resolve) => {
        let voices = synth.getVoices();
        if (voices.length) {
            resolve(voices);
        } else {
            synth.onvoiceschanged = () => {
                voices = synth.getVoices();
                resolve(voices);
            };
        }
    });
}

const chatMessages = document.createElement('div');
chatMessages.classList.add('chat-messages');
chatBox.appendChild(chatMessages);

function addMessageToChatBox(message, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('chat-message');

    if (sender === 'user') {
        messageDiv.classList.add('user-message');
    } else {
        messageDiv.classList.add('assistant-message');
    }

    const messageText = document.createElement('p');
    messageText.textContent = message;
    messageDiv.appendChild(messageText);

    chatMessages.appendChild(messageDiv);

    chatBox.scrollTop = chatBox.scrollHeight;
}

startBtn.addEventListener('click', () => {
    if (!isListening) {
        isListening = true;
        userRequestedStop = false;
        recognition.start();
        transcriptOutput.textContent = "• Listening...";
        wave.style.animationPlayState = 'running';
        startBtn.disabled = true;
    }
});

recognition.addEventListener('result', (e) => {
    const transcript = e.results[e.results.length - 1][0].transcript.trim().toLowerCase();
    addMessageToChatBox(transcript, 'user');

    if (transcript === "stop listening" || transcript === "stop") {
        userRequestedStop = true;
        isListening = false;
        recognition.stop();
        transcriptOutput.textContent = "• Stopped Listening";
        wave.style.animationPlayState = 'paused';
        startBtn.disabled = false;
        addMessageToChatBox("Okay, I stopped listening.", 'assistant');
        speakResponse("Okay, I stopped listening.");
        return;
    }

    handleResponse(transcript);
});

recognition.addEventListener('end', () => {
    wave.style.animationPlayState = 'paused';
    startBtn.disabled = false;

    if (isListening && !userRequestedStop) {
        recognition.start(); // Restart automatically if not stopped by user
    }
});

function handleResponse(transcript) {
    try {
        if (transcript.includes('dark mode')) {
            document.body.classList.add('dark-mode');
            document.body.classList.remove('light-mode');
            addMessageToChatBox("Switched to dark mode.", 'assistant');
            speakResponse("Switched to dark mode.");
            return;
        } else if (transcript.includes('light mode')) {
            document.body.classList.add('light-mode');
            document.body.classList.remove('dark-mode');
            addMessageToChatBox("Switched to light mode.", 'assistant');
            speakResponse("Switched to light mode.");
            return;
        }

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
                const responseText = data.response;
                responseDiv.innerHTML = responseText;
                addMessageToChatBox(responseText, 'assistant');
                speakResponse(responseText);
            }
        })
        .catch(error => console.error('Error:', error));
    } catch (error) {
        console.error('Error handling response:', error);
    }
}

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

        utterance.voice = window.preferredVoice || voices[0];
        utterance.pitch = 1.2;
        utterance.rate = 0.9;
        utterance.volume = 1;

        utterance.onstart = function () {
            console.log("Speech started");
        };

        utterance.onend = function () {
            console.log("Speech ended");
        };

        utterance.onerror = function (event) {
            console.error("Speech error", event);
        };

        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(utterance);
    } catch (error) {
        console.error("Error speaking response:", error);
    }
}

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

window.addEventListener('load', async () => {
    voices = await loadVoicesProperly();
    console.log("Available voices:", voices.map(v => v.name));

    const preferredVoiceName = "Google US English";
    const preferredVoice = voices.find(voice => voice.name === preferredVoiceName);

    if (preferredVoice) {
        window.preferredVoice = preferredVoice;
    } else {
        console.warn("Preferred voice not found, using default.");
        window.preferredVoice = voices[0];
    }

   

    document.getElementById('theme-toggle').addEventListener('click', function () {
        document.body.classList.toggle('dark-mode');
    });

    greetUser();
});