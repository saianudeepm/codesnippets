/*Download all the slides in the current page of coursera course page*/
var getElementByXpath=  function(path) {
  return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
}

var getElementsByXpath = function(xpathToExecute){
  var result = [];
  var nodesSnapshot = document.evaluate(xpathToExecute, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null );
  for ( var i=0 ; i < nodesSnapshot.snapshotLength; i++ ){
    result.push( nodesSnapshot.snapshotItem(i) );
  }
  return result;
}

var slideAnchors = getElementsByXpath('//a[contains(@href, "slides")]');
/*To run in the chrome browser*/
//var slideAnchors = $x('//a[contains(@href, "slides")]’);

//TODO ned to check why the downloaded file name is not same as the 'download' attribute value
slideAnchors.forEach(
  function(i){ 
    console.log(i.href);
    i.download=i.getElementsByClassName('hidden')[0].textContent;
    i.click();
  }
);
