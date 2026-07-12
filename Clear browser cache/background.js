chrome.action.onClicked.addListener(async (tab) => {
  chrome.browsingData.remove(
    {},
    {
      cache: true
    },
    () => {

      chrome.tabs.reload(tab.id);

    }
  );

});
