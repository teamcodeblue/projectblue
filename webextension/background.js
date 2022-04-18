//var url_list = new Array();
var tab_new = Array(1000).fill(0);
var previose_time = new Date() ;
var previose_url;
var timeV;
var previose_html;
function getHTML() {
 return document.documentElement.outerHTML;
}


chrome.storage.sync.set({ 'state': 1 }, function () {
 
});
const url_map = new Map();
const time_map = new Map();
const data_map = new Map();
chrome.tabs.onUpdated.addListener( function (tabId, changeInfo, tab) {
    if (changeInfo.status == 'complete') {
      chrome.storage.sync.get(['state'], function(result) {
        //console.log("state is " + result.state);

   
        if(!result.state)
          tab_new[tabId] = 0;
        if (tab.url != "chrome://newtab/" && result.state)
        {
          if(!tab_new[tabId])
          {
            tab_new[tabId] = 1;
            previose_time = new Date();
            previose_url = tab.url;
          }
          else
          {
            
            timeV = (new Date() - previose_time) / 1000;
            console.log(previose_html)
            
            

            //posing data
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
                body: JSON.stringify({'url': (previose_url).toString(), 'timeSpend' : timeV, 'html' : previose_html[0].result}) // body data type must match "Content-Type" header
              });
              console.log("time spend on " + previose_url + " : " + timeV + " seconds");
            console.log("the previose html file is ");
            console.log(previose_html);
              return response.json(); // parses JSON response into native JavaScript objects
            
            }
            
            postData('http://127.0.0.1:30009/api/extension_post', { answer: 42 })
            
              .then(data => {
                console.log(data); // JSON data parsed by `data.json()` call
              });
            //end of posting data


            
            previose_time = new Date();
            previose_url = tab.url;
          }
        //console.log("current the url is " + tab.url);
     
       //console.log("tab id is " + tabId);
       
        url_map.set(tabId,tab.url);
        time_map.set(tabId,new Date());

        chrome.scripting.executeScript(
          {
            target: {tabId: tabId},
            func: getHTML,
          },
          (htmlfile) => {
           
            previose_html = htmlfile;
              
          });
          


        
       }
      });

      




        

      
     
   
  
    }
  })
  chrome.tabs.onRemoved.addListener(function(tabid, removed) {
   // console.log(tabid);
   chrome.storage.sync.get(['state'], function(result) {
     if(result.state){
       console.log("the tab is now closed");
       console.log("time spend on last url is " + (new Date() - previose_time) / 1000);
     }
  
   })

   tab_new[tabid] = 0 ;
  })
