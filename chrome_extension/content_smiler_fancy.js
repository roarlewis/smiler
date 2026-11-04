var elements = document.querySelectorAll('img');

elements.forEach((image) => {
    var image_url = image.currentSrc || image.src;

    // skip blank, data: and blob: sources that Flask can't download
    if (!image_url.startsWith('http')) return;

    chrome.runtime.sendMessage({ url: image_url }, (reply) => {
        if (!reply || reply.error) return;

        // srcset would override src, so drop it
        image.removeAttribute('srcset');
        image.src = reply.dataUrl;
    });
});