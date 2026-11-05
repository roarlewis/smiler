// converted images by original URL, so a site resetting src doesn't re-hit Flask
var converted = new Map();

// URLs waiting to be sent, and how many requests are out right now;
// sending everything at once overloads Flask on image-heavy pages like YouTube
var queue = [];
var queued = new Set();
var active = 0;
var MAX_ACTIVE = 3;

function getImageUrl(image) {
    // an empty src attribute resolves to the page's own URL, so check the attribute itself
    if (image.getAttribute('src')) {
        // currentSrc still holds the old picture right after src changes,
        // so only fall back to it when src itself isn't usable
        if (image.src.startsWith('http')) return image.src;
    }
    if (image.getAttribute('srcset')) return image.currentSrc;
    return '';
}

function applyResult(image_url, dataUrl) {
    document.querySelectorAll('img[data-smilr-pending]').forEach((image) => {
        // the site may have reused this <img> for another picture meanwhile
        if (image.dataset.smilrPending !== image_url) return;
        delete image.dataset.smilrPending;

        // srcset would override src, so drop it
        image.removeAttribute('srcset');
        image.src = dataUrl;
    });
}

function sendNext() {
    while (active < MAX_ACTIVE && queue.length > 0) {
        var image_url = queue.shift();
        active++;
        chrome.runtime.sendMessage({ url: image_url }, (reply) => {
            active--;
            queued.delete(image_url);
            if (reply && !reply.error) {
                converted.set(image_url, reply.dataUrl);
                applyResult(image_url, reply.dataUrl);
            }
            sendNext();
        });
    }
}

function smilify(image) {
    var image_url = getImageUrl(image);

    // skip blank, data: and blob: sources that Flask can't download
    if (!image_url.startsWith('http')) return;

    if (converted.has(image_url)) {
        image.removeAttribute('srcset');
        image.src = converted.get(image_url);
        return;
    }

    image.dataset.smilrPending = image_url;

    // already waiting on this URL, so this image just gets the same result
    if (queued.has(image_url)) return;
    queued.add(image_url);
    queue.push(image_url);
    sendNext();
}

document.querySelectorAll('img').forEach(smilify);

new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
        if (mutation.type === 'attributes') {
            smilify(mutation.target);
            return;
        }
        mutation.addedNodes.forEach((node) => {
            if (node.nodeType !== Node.ELEMENT_NODE) return;
            if (node.tagName === 'IMG') smilify(node);
            node.querySelectorAll('img').forEach(smilify);
        });
    });
}).observe(document.documentElement, {
    childList: true,
    subtree: true,
    attributes: true,
    attributeFilter: ['src', 'srcset']
});
