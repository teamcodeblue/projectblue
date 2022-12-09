document.addEventListener('DOMContentLoaded', function () {
  var checkbox = document.querySelector('input[type="checkbox"]');
  chrome.storage.sync.get(['state'], function(result) {

    checkbox.checked= result.state;
  });
  chrome.tabs.query({ active: true, lastFocusedWindow: true }, tabs => {
        let url = tabs[0].url;
        let current_URL = document.getElementById("current_URL");
        var regex = /\/\/([^\/,\s]+\.[^\/,\s]+?)(?=\/|,|\s|$|\?|#)/g;
        match = regex.exec(url);
        current_URL.innerHTML = match[1];
    });
  checkbox.addEventListener('click', function () {


    chrome.storage.sync.get(['state'], function(result) {
      //console.log('state currently is ' + result.state);
      if(result.state)
      {
        chrome.storage.sync.set({ 'state': 0 }, function () {});
      }else
      {
        chrome.storage.sync.set({ 'state': 1 }, function () {});
      }

    });
  });
});
//let rec_button = document.getElementById("btn btn-primary");
//let rec_text = document.getElementById("rec_text");
//let latest_rec_button = document.getElementById("latest_rec_button");
//let latest_rec_text = document.getElementById("latest_rec_text");
// chrome.storage.sync.get("color", ({ color }) => {
//   changeColor.style.backgroundColor = color;
// });


rec_button.addEventListener("click", async () => {

async function postData(url = '127.0.0.1:30009/api/extension_post', data = {}) {
  // Default options are marked with *
try{
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
    body: JSON.stringify({'url': "",'html': ""}) // body data type must match "Content-Type" header
  });
  //console.log(response.json())
  return response.json(); // parses JSON response into native JavaScript objects
  }catch(error)
  {
    return null;
  }
}
  let data = await postData('http://127.0.0.1:30009/api/force_reccomendations_request', { answer: 42 })
  if(data != null)
  {

  rec_text.innerHTML =data.text;
  }
  else
  {
    rec_text.innerHTML = 'error, connection failed!';
  }

});

latest_rec_button.addEventListener("click", async () => {

async function postData(url = '127.0.0.1:30009/api/extension_post', data = {}) {
  // Default options are marked with *
try{
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
    body: JSON.stringify({'url': "",'html': ""}) // body data type must match "Content-Type" header
  });
  //console.log(response.json())
  return response.json(); // parses JSON response into native JavaScript objects
  }catch(error)
  {

    return null;
  }
}
  let data = await postData('http://127.0.0.1:30009/api/reccomendations_request', { answer: 42 })
  if(data != null)
  {

  latest_rec_text.innerHTML =data.text;
  }
  else
  {
    latest_rec_text.innerHTML = "The latest recommendation list is empty :(";
  }

});
