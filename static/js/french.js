// let mediaRecorder;
// let audioChunks = [];

// document.getElementById("playRecording").addEventListener("click", playRecording);

// document.getElementById("startRecording").addEventListener("click", function() {
//     navigator.mediaDevices.getUserMedia({ audio: true })
//     .then(stream => {
//         console.log('Stream active state:', stream.active);
//         mediaRecorder = new MediaRecorder(stream);
//         audioChunks = [];

//         mediaRecorder.addEventListener("dataavailable", event => {
//             audioChunks.push(event.data);
//             console.log('Audio data available:', audioChunks.length);
//         });

//         mediaRecorder.start();
//         document.getElementById("feedback").textContent = "Recording started...";
//     })
//     .catch(error => console.error("Error accessing the microphone", error));
// });

// // When the recording stops, package the audio data and send it to the server
// document.getElementById("stopRecording").addEventListener("click", function() {
//     const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
//     console.log(audioChunks.length)
//     const formData = new FormData();
//     formData.append("audio_data", audioBlob);
//     formData.append("sentence", document.getElementById("sentence").textContent);

//     // Function to send audio data to server and receive feedback
//     sendAudioAndGetFeedback(formData);
// });

// // document.getElementById('playPronunciation').addEventListener('click', function() {
// //     const sentence = document.getElementById('sentence').textContent;
// //     playPronunciation(sentence);
// // });

// document.getElementById("playPronunciation").addEventListener("click", playPronunciation);

// // This function uses the Speech Synthesis API to pronounce the sentence
// function playPronunciation(sentence) {
//     let utterance = new SpeechSynthesisUtterance(sentence);
//     utterance.lang = 'fr-FR';
//     speechSynthesis.speak(utterance);
// }

// // This function plays the recorded audio
// function playRecording() {
//     try {
//         const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
//         const audioUrl = URL.createObjectURL(audioBlob);
//         const audio = new Audio(audioUrl);

//         // Add an event listener to handle playback errors
//         audio.addEventListener('error', function() {
//             console.error('Audio playback error:', audio.error);
//         });

//         audio.play();
//     } catch (error) {
//         console.error('Error playing audio:', error);
//     }
// }

// // Function to send audio data to server and receive feedback
// function sendAudioAndGetFeedback(formData) {
//     fetch("/assess-speech", {
//         method: "POST",
//         body: formData
//     })
//     .then(response => response.json())
//     .then(data => {
//         document.getElementById("feedback").textContent = `Score: ${data.score}, Feedback: ${data.feedback}`;
//     })
//     .catch(error => {
//         console.error("Error submitting audio to server: ", error);
//         document.getElementById("feedback").textContent = "Error occurred.";
//     });
// }
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

        mediaRecorder.addEventListener("stop", () => {
            console.log('Recording stopped. Chunks collected: ', audioChunks.length);
        });

        mediaRecorder.start();
        console.log('Recording started');
        document.getElementById("feedback").textContent = "Recording started...";
    })
    .catch(error => {
        console.error("Error accessing the microphone", error);
        document.getElementById("feedback").textContent = "Error accessing the microphone";
    });
});

document.getElementById("stopRecording").addEventListener("click", function() {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
        console.log('Recording stopped by user');
        document.getElementById("feedback").textContent = "Recording stopped";
    } else {
        console.error("Recorder not active or not started");
        document.getElementById("feedback").textContent = "Recorder not active or not started";
    }
});

document.getElementById("playPronunciation").addEventListener("click", playPronunciation);

function playPronunciation() {
    const sentence = document.getElementById("sentence").textContent;
    let utterance = new SpeechSynthesisUtterance(sentence);
    utterance.lang = 'fr-FR';
    speechSynthesis.speak(utterance);
}

function playRecording() {
    if (audioChunks.length > 0) {
        const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
        const audioUrl = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioUrl);

        audio.addEventListener('error', function() {
            console.error('Audio playback error:', audio.error);
        });

        audio.play();
    } else {
        console.error('No audio data to play');
    }
}

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
