



// When the button is clicked
document.addEventListener('DOMContentLoaded', function () {
  var checkbox = document.querySelector('input[type="checkbox"]');
  
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




