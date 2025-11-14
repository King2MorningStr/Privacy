document.getElementById('testButton').addEventListener('click', () => {
  const statusEl = document.getElementById('status');
  statusEl.textContent = 'Pinging...';

  // Send a message to the background script
  chrome.runtime.sendMessage(
    {
      action: "pingServer",
      text: "This is a test from the extension"
    },
    (response) => {
      // This is the callback that runs when the background script replies
      if (response && response.status === "ok") {
        console.log("Response from server:", response.data);
        statusEl.textContent = "Success!";
      } else {
        console.error("Failed to get a good response.");
        statusEl.textContent = "Error!";
      }
    }
  );
});
