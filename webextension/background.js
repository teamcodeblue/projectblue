chrome.storage.sync.set({ 'state': 1 }, function () {
 
});
const url_map = new Map();
const time_map = new Map();
const data_map = new Map();
chrome.tabs.onUpdated.addListener( function (tabId, changeInfo, tab) {
    if (changeInfo.status == 'complete') {
      chrome.storage.sync.get(['state'], function(result) {
        //console.log("state is " + result.state);
        if (tab.url != "chrome://newtab/" )
        {
       // console.log(tab.url);
     
       // console.log(tabId);
        url_map.set(tabId,tab.url);
        time_map.set(tabId,new Date());

       }
      });
     // Example POST method implementation:
async function postData(url = '127.0.0.1:30009/api/extension_post', data = {}) {
  // Default options are marked with *
  const response = await fetch(url, {
    method: 'POST', // *GET, POST, PUT, DELETE, etc.
    mode: 'cors', // no-cors, *cors, same-origin
    cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    credentials: 'same-origin', // include, *same-origin, omit
    headers: {
      'Content-Type': 'application/json',
      'Accept' : 'application/json'
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    redirect: 'follow', // manual, *follow, error
    referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
    body: JSON.stringify({'url': (tab.url).toString()}) // body data type must match "Content-Type" header
  });
  console.log(tab.url);
  return response.json(); // parses JSON response into native JavaScript objects

}

postData('http://127.0.0.1:30009/api/extension_post', { answer: 42 })

  .then(data => {
    console.log(data); // JSON data parsed by `data.json()` call
  });}
  })
  chrome.tabs.onRemoved.addListener(function(tabid, removed) {
   // console.log(tabid);
   chrome.storage.sync.get(['state'], function(result) {
     if(result.state){
    var time_dif = (new Date() - time_map.get(tabid) ) / 1000;
    var url = url_map.get(tabid);
    if (url != null){
    if(data_map.has(url))
    {
      var previouse_used_time = data_map.get(url);
      data_map.set(url, previouse_used_time + time_dif);
    }else{
      //console.log(url,time_dif);
      data_map.set(url,time_dif);
    }
    console.log(data_map);}}
   })
  })