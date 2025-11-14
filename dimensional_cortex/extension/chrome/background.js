// background.js

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {

  // This is our new, automated action
  if (request.action === "enrichPrompt") {
    console.log("Background script received 'enrichPrompt':", request.text);

    const serverPayload = {
      text: request.text,
      platform: "ChromeExtension_v2"
    };

    // Use fetch() to talk to your local Python server (V4)
    fetch("http://127.0.0.1:8000/process_interaction", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(serverPayload)
    })
    .then(response => response.json())
    .then(data => {
      console.log("Got response from server:", data);
      sendResponse({ status: "ok", data: data });
    })
    .catch(error => {
      console.error("Error fetching from local server:", error);
      sendResponse({ status: "error" });
    });

    return true; // Keep the message channel open for the async response
  }

  // This is our old "ping" test from the popup button
  if (request.action === "pingServer") {
    // ... (the old ping code can stay here, it won't hurt) ...
    return true;
  }
});
