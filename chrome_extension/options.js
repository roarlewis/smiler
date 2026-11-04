let fromTextElement = document.getElementById('fromField');
let toTextElement = document.getElementById('toField');
let setButtonElement = document.getElementById('setButton');
let onButtonElement = document.getElementById('onButton');
let isCheckedString = "false";



setButtonElement.addEventListener('click', function() {
    if (onButtonElement.checked) {
        isCheckedString = "true";
    }
    chrome.storage.sync.set({
        fromStored: fromTextElement.value,
        toStored: toTextElement.value,
        turnedOn: isCheckedString});
  });