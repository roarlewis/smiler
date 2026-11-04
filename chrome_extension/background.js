const SERVER = 'http://127.0.0.1:5000/convert-image/?url=';

// Service workers can't use FileReader, so build the base64 string by hand
function toDataUrl(buffer, mimeType) {
    const bytes = new Uint8Array(buffer);
    let binary = '';
    for (let i = 0; i < bytes.length; i += 0x8000) {
        binary += String.fromCharCode(...bytes.subarray(i, i + 0x8000));
    }
    return `data:${mimeType};base64,${btoa(binary)}`;
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    fetch(SERVER + encodeURIComponent(message.url))
        .then((response) => {
            if (!response.ok) throw new Error(`server returned ${response.status}`);
            return response.arrayBuffer().then((buffer) =>
                toDataUrl(buffer, response.headers.get('Content-Type') || 'image/jpeg'));
        })
        .then((dataUrl) => sendResponse({ dataUrl: dataUrl }))
        .catch((error) => sendResponse({ error: error.message }));

    // keeps sendResponse open until the fetch finishes
    return true;
});