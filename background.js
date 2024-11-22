chrome.runtime.onInstalled.addListener(() => {
  const contextMenus = [
    { id: "openInEdge", title: "Open Link in Edge", contexts: ["link"] },
    { id: "searchInEdge", title: "Search in Edge: '%s'", contexts: ["selection"] },
    { id: "openCurrentTabInEdge", title: "Open Current Tab in Edge", contexts: ["page"] }
  ];
  
  contextMenus.forEach(menu => chrome.contextMenus.create(menu));
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  const actions = {
    "openInEdge": () => info.linkUrl,
    "searchInEdge": () => `https://www.google.com/search?q=${encodeURIComponent(info.selectionText)}`,
    "openCurrentTabInEdge": () => tab.url
  };

  const url = actions[info.menuItemId]?.();
  if (url) {
    chrome.runtime.sendNativeMessage('com.edge.launcher', { url });
  }
});