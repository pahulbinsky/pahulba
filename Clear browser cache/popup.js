document.getElementById("clearBtn").addEventListener("click", async () => {

  chrome.browsingData.remove(
    {},
    {
      cache: true
    },
    async () => {

      const [tab] = await chrome.tabs.query({
        active: true,
        currentWindow: true
      });

      chrome.tabs.reload(tab.id);

      alert("Кэш в очке!");
    }
  );

});