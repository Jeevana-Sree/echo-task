// Submit task via API
function submitTask() {
  const name = document.getElementById("name").value;
  const email = document.getElementById("email").value;
  const message = document.getElementById("message").value;
  const reminder_time = document.getElementById("reminder_time").value;

  fetch("/submit", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, email, message, reminder_time })
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById("output").innerText = data.message || data.error;
    speak(data.message || data.error);
  });
}

// Speak message aloud
function speak(text) {
  const synth = window.speechSynthesis;
  const utter = new SpeechSynthesisUtterance(text);
  synth.speak(utter);
}

// Start voice recognition
function startListening() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const recognition = new SpeechRecognition();

  recognition.onstart = () => {
    document.getElementById("output").innerText = "Listening...";
  };

  recognition.onresult = (event) => {
    const text = event.results[0][0].transcript;
    document.getElementById("message").value = text;
    document.getElementById("output").innerText = `Heard: ${text}`;
    speak("Got it! Now click Add Task to schedule.");
  };

  recognition.onerror = () => {
    document.getElementById("output").innerText = "Could not hear properly. Try again!";
  };

  recognition.start();
}
