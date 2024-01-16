document.addEventListener('DOMContentLoaded', (event) => {
    
    let mediaRecorder;
    let audioChunks = [];
    let audioBlob; 
    let isRecording = false;
    let transcript = "";
    let recognition;

    function loadNextQuestion() {
        fetch('/fr/next-question')
        .then(response => response.json())  // Convert the response to JSON
        .then(data => {
            // Update the page with the new question
            document.getElementById("original").textContent = data.original;
            document.getElementById("translation").textContent = data.translation;
    
            // Clear feedback and score
            document.getElementById("feedback").textContent = "";
            document.getElementById("score").textContent = "";
    
            // Hide the next question button until the user gets a high enough score again
            document.getElementById("nextQuestion").style.display = 'none';
    
            // Reset the lastScorein localStorage, since the user is moving to a new question
            localStorage.removeItem('lastScore');
            })
            .catch(error => {
            console.error('Error fetching the next question:', error);
            });
            }
            
            // You can call this function when the 'Next Question' button is clicked
            document.getElementById('nextQuestion').addEventListener('click', function() {
            loadNextQuestion();})



    if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
        recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'fr-FR';
        recognition.interimResults = false;
    } else {
        alert("Your browser doesn't support speech recognition. Please switch to Google Chrome or another supported browser.");
        return;
    }
    
    document.getElementById("startRecording").addEventListener("click", function() {
        navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.ondataavailable = function(event) {
                audioChunks.push(event.data);
            };

            mediaRecorder.onstop = function() {
                audioBlob = new Blob(audioChunks, {'type' : 'audio/wav; codecs=opus' });
                audioChunks = [];
                console.log('MediaRecorder stopped, blob created.');
                };

            mediaRecorder.start();
            console.log('MediaRecorder started');
            recognition.start();
            console.log('SpeechRecognition started');
            document.getElementById("feedback").textContent = "Listening...";
            isRecording = true;
        })
        .catch(error => {
            console.error("Error accessing the microphone", error);
        });
    });

        document.getElementById("playRecording").addEventListener("click", playRecording);

        recognition.onresult = function(event) {
            transcript = event.results[0][0].transcript.trim();
            let originalText = document.getElementById("original").textContent.trim();
            compareTranscript(originalText, transcript);
            console.log('Transcript:', transcript);
            let score = calculateScore(originalText, transcript);
            localStorage.setItem('lastScore', score); // Store the score in localStorage
            displayFeedbackAndHandleNextQuestion(score); 

        };
        
    // Function to calculate the score based on the transcript
    function calculateScore(original, transcript) {
        let similarity = compareTranscript(original, transcript);
        return Math.round(similarity * 100); // Convert similarity ratio to percentage
    }
        recognition.onend = function() {
            if (isRecording) {
                mediaRecorder.stop();
                isRecording = false;
                console.log('SpeechRecognition ended');
            }
        };
        
        document.getElementById("playRecording").addEventListener("click", function() {
            if (audioBlob) {
                const audioUrl = URL.createObjectURL(audioBlob);
                const audio = new Audio(audioUrl);
                audio.play();
            } else {
                console.log('No recording to play.');
            }
        });
        
        // Function to calculate the score based on the transcript
    function calculateScore(original, transcript) {
        let similarity = calculateSimilarity(original, transcript);
        return Math.round(similarity * 100); // Convert similarity ratio to percentage
    }

    // Function to display feedback and handle the next question button
    function displayFeedbackAndHandleNextQuestion(score) {
        let feedback = "";
        if (score >= 95) {
            feedback = "Great Job!";
            nextQuestionButton.style.display = ''; // Show the button
        } else if (score >= 80) {
            feedback = "You're Getting There! Keep Practicing.";
            nextQuestionButton.style.display = 'none'; // Hide the button
        } else {
            feedback = "Try again, focus on your pronunciation.";
            nextQuestionButton.style.display = 'none'; // Hide the button
        }
        document.getElementById("feedback").textContent = feedback;
        document.getElementById("score").textContent = `Score: ${score}%`;

        // Only allow the user to click 'Next Question' if their score is 95 or above
        nextQuestionButton.disabled = score < 95;
    }


    function compareTranscript(original, transcript) {
        let similarity = calculateSimilarity(original, transcript);
        let feedback = "";
        let score = Math.round(similarity * 100); // Convert similarity ratio to percentage
        if (similarity > 0.95) {
            feedback = "Great Job!";
        } else if (similarity > 0.8) {
            feedback = "You're Getting There! Keep Practicing.";
        } else {
            feedback = "Try again, focus on your pronunciation.";
        }
        // Display feedback and score
        document.getElementById("feedback").textContent = `${feedback} Score: ${score}%`;
        }
            
        

    function calculateSimilarity(s1, s2) {
        let longer = s1;
        let shorter = s2;
        if (s1.length < s2.length) {
            longer = s2;
            shorter = s1;
        }
        let longerLength = longer.length;
        if (longerLength === 0) {
            return 1.0;
        }
        return (longerLength - editDistance(longer, shorter)) / parseFloat(longerLength);
    }
    
    function editDistance(s1, s2) {
        s1 = s1.toLowerCase();
        s2 = s2.toLowerCase();
    
        let costs = new Array();
        for (let i = 0; i <= s1.length; i++) {
            let lastValue = i;
            for (let j = 0; j <= s2.length; j++) {
                if (i === 0)
                    costs[j] = j;
                else {
                    if (j > 0) {
                        let newValue = costs[j - 1];
                        if (s1.charAt(i - 1) !== s2.charAt(j - 1))
                            newValue = Math.min(Math.min(newValue, lastValue),
                                costs[j]) + 1;
                        costs[j - 1] = lastValue;
                        lastValue = newValue;
                    }
                }
            }
            if (i > 0)
                costs[s2.length] = lastValue;
        }
        return costs[s2.length];
    }

    // Ensure this element exists in your HTML and has the correct ID
    let playPronunciationButton = document.getElementById("playPronunciation");
    if (playPronunciationButton) {
        playPronunciationButton.addEventListener("click", playPronunciation);
    } else {
        console.error("Play Pronunciation button not found");}

    function playPronunciation() {
    const sentence = document.getElementById("original").textContent;
    let utterance = new SpeechSynthesisUtterance(sentence);
    utterance.lang = 'fr-FR';
    speechSynthesis.speak(utterance);
    }

    function playRecording() {
        if (audioBlob) {
        const audioUrl = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioUrl);
        audio.play();
        } else {
        console.log('No recording to play.');
        }
        }

    // Ensure this element exists in your HTML and has the correct ID
    let nextQuestionButton = document.getElementById("nextQuestion");

    // Load the next question if the user had achieved a high enough score previously
    let lastScore = localStorage.getItem('lastScore');
    if (lastScore && lastScore >= 95) {
        nextQuestionButton.style.display = '';
        nextQuestionButton.disabled = false;
    } else {
        nextQuestionButton.style.display = 'none';
        nextQuestionButton.disabled = true;
    }
            
    });

