chrome.storage.sync.get({fromStored: "", toStored: "", turnedOn: "false"}, function(result) {
    if(result.turnedOn === "true") {
        var html = document.querySelector('html');
        var walker = document.createTreeWalker(html, NodeFilter.SHOW_TEXT);
        var node;

        while (node = walker.nextNode()) {
            var fromText = result.fromStored
            var toText = result.toStored

            var re = new RegExp(fromText,"gi")
            node.nodeValue = node.nodeValue.replace(re, toText); 
        }
    }
});