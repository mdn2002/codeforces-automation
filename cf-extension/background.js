chrome.commands.onCommand.addListener((command) => {
  console.log("Hotkey pressed:", command);
  if (command === "send-html") {
    chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
      const tab = tabs[0];
      console.log("Injecting content.js into tab:", tab.id, tab.url);
      chrome.scripting.executeScript({
        target: {tabId: tab.id},
        files: ["content.js"]
      });
    });
  }
}); 