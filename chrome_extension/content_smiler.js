var elements = document.querySelectorAll('img');

elements.forEach((image) => {
    var image_url = encodeURIComponent(image.src);
    var input_url = `http://127.0.0.1:5000/convert-image/?url=${image_url}`;
    image.src = input_url;
});