// // Check if the browser supports the Web Speech API
// if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
//     alert('Your browser does not support speech recognition. Please try this in Google Chrome.');
// } else {
//     function startRecognition() {
//         // Initialize the speech recognition object and start recognition...
//         recognition.onresult = function(event) {
//             const spokenText = event.results[0][0].transcript;
    
//             // Send the spoken text to the server
//             fetch('/process_speech', {
//                 method: 'POST',
//                 body: JSON.stringify({ spokenText: spokenText }),
//                 headers: {
//                     'Content-Type': 'application/json'
//                 }
//             })
//             .then(response => response.json())
//             .then(data => {
//                 // Display feedback from the server
//                 document.getElementById('feedback').innerText = data.feedback;
//             });
//         };
//         recognition.start();
//     }
    

//     function sendTextToServer(spokenText) {
//         // Fetch the sentence from the DOM
//         const sentenceElement = document.getElementById('sentence');
//         const sentenceToCompare = sentenceElement ? sentenceElement.innerText : '';

//         // Make a POST request to the server
//         fetch('/compare-sentence', {
//             method: 'POST',
//             body: JSON.stringify({
//                 sentence: sentenceToCompare,
//                 spokenText: spokenText
//             }),
//             headers: {
//                 'Content-Type': 'application/json'
//             }
//         })
//         .then(response => response.json())
//         .then(data => {
//             // Handle the response data from the server
//             console.log('Server response:', data);
//             if (data.similarity > 0.95) {
//                 // If similarity is high, show success message
//                 alert('Great job! Your pronunciation was very close to the target.');
//             } else {
//                 // If not, encourage the user to try again
//                 alert('Keep practicing! You are getting there.');
//             }
//         })
//         .catch(error => {
//             console.error('Error sending text to server:', error);
//         });
//     }
// }

document.getElementById('check').addEventListener('click', function() {
    var recognition = new webkitSpeechRecognition() || new SpeechRecognition();
    recognition.lang = 'fr-FR';  // Set language to French
    recognition.onresult = function(event) {
        var spokenText = event.results[0][0].transcript;
        sendAudioToServer(spokenText);  // Function to send data to server
    };
    recognition.start();  // Start speech recognition
});

function sendAudioToServer(spokenText) {
    fetch('/check_pronunciation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({spokenText: spokenText})
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.feedback);  // Handle feedback
        // Update the DOM with feedback
    })
    .catch(error => console.error('Error:', error));
}


document
  .getElementById("startRecording")
  .addEventListener("click", initFunction);
let isRecording = document.getElementById("isRecording");
function initFunction() {
  // Display recording
  async function getUserMedia(constraints) {
    if (window.navigator.mediaDevices) {
      return window.navigator.mediaDevices.getUserMedia(constraints);
    }
    let legacyApi =
      navigator.getUserMedia ||
      navigator.webkitGetUserMedia ||
      navigator.mozGetUserMedia ||
      navigator.msGetUserMedia;
    if (legacyApi) {
      return new Promise(function (resolve, reject) {
        legacyApi.bind(window.navigator)(constraints, resolve, reject);
      });
    } else {
      alert("user api not supported");
    }
  }
  isRecording.textContent = "Recording...";
  //
  let audioChunks = [];
  let rec;
  function handlerFunction(stream) {
    rec = new MediaRecorder(stream);
    rec.start();
    rec.ondataavailable = (e) => {
      audioChunks.push(e.data);
      if (rec.state == "inactive") {
        let blob = new Blob(audioChunks, { type: "audio/wav" });
        console.log(blob);
        document.getElementById("audioElement").src = URL.createObjectURL(blob);
        console.log(URL.createObjectURL(blob));
      }
    };
  }
  function startusingBrowserMicrophone(boolean) {
    getUserMedia({ audio: boolean }).then((stream) => {
      handlerFunction(stream);
    });
  }
  startusingBrowserMicrophone(true);
  // Stoping handler
  document.getElementById("stopRecording").addEventListener("click", (e) => {
    rec.stop();
    isRecording.textContent = "Click play button to start listening";
  });
}