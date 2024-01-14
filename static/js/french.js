let mediaRecorder;
let audioChunks = [];

document.getElementById("playRecording").addEventListener("click", playRecording);

document.getElementById("startRecording").addEventListener("click", function() {
    navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => {
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];

        mediaRecorder.addEventListener("dataavailable", event => {
            audioChunks.push(event.data);
        });

        mediaRecorder.start();
        document.getElementById("feedback").textContent = "Recording started...";
    })
    .catch(error => console.error("Error accessing the microphone", error));
});

// document.getElementById("stopRecording").addEventListener("click", function() {
//     if (mediaRecorder.state !== 'inactive') {
//         mediaRecorder.stop();
//         document.getElementById("feedback").textContent = "Processing...";
//     }
// });

// When the recording stops, package the audio data and send it to the server
document.getElementById("stopRecording").addEventListener("click", function() {
    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
    const formData = new FormData();
    formData.append("audio_data", audioBlob);
    formData.append("sentence", document.getElementById("sentence").textContent);

    // Function to send audio data to server and receive feedback
    sendAudioAndGetFeedback(formData);
});

document.getElementById('playPronunciation').addEventListener('click', function() {
    const sentence = document.getElementById('sentence').textContent;
    playPronunciation(sentence);
});

// This function uses the Speech Synthesis API to pronounce the sentence
function playPronunciation(sentence) {
    let utterance = new SpeechSynthesisUtterance(sentence);
    utterance.lang = 'fr-FR';
    speechSynthesis.speak(utterance);
}

// This function plays the recorded audio
function playRecording() {
    const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
    const audioUrl = URL.createObjectURL(audioBlob);
    const audio = new Audio(audioUrl);
    audio.play();
}

// Function to send audio data to server and receive feedback
function sendAudioAndGetFeedback(formData) {
    fetch("/assess-speech", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("feedback").textContent = `Score: ${data.score}, Feedback: ${data.feedback}`;
    })
    .catch(error => {
        console.error("Error submitting audio to server: ", error);
        document.getElementById("feedback").textContent = "Error occurred.";
    });
}

