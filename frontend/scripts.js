function startListening() {
  const recognition = new webkitSpeechRecognition(); // or SpeechRecognition for Chrome API
  recognition.lang = 'en-US';
  recognition.start();
  document.getElementById("status").innerText = "Listening...";

  recognition.onresult = function(event) {
    const text = event.results[0][0].transcript;
    document.getElementById("status").innerText = "You said: " + text;

    fetch('http://localhost:5050/submit-task', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    })
    .then(response => response.json())
    .then(data => {
      const message = data.message || data.error || "No message returned";
      document.getElementById("status").innerText += "\n" + message;

      // Text-to-speech output
      const utterance = new SpeechSynthesisUtterance(message);
      speechSynthesis.speak(utterance);

      // Refresh task list if loadTasks is defined
      if (typeof loadTasks === "function") {
        loadTasks();
      }
    })
    .catch(err => {
      console.error("Error:", err);
      const utterance = new SpeechSynthesisUtterance("An error occurred while saving the task.");
      speechSynthesis.speak(utterance);
    });
  };
}

function loadTasks() {
  fetch('http://localhost:5050/tasks')
    .then(res => res.json())
    .then(data => {
      const list = document.getElementById("task-list");
      if (!list) return;

      list.innerHTML = "";
      data.forEach(([task, time]) => {
        const li = document.createElement("li");
        li.textContent = `${task} – ${new Date(time).toLocaleString()}`;
        list.appendChild(li);
      });
    })
    .catch(err => {
      console.error("Failed to load tasks:", err);
    });
}
