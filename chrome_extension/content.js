var elements = document.getElementsByTagName('div');

var SATURATION_CONSTANT = 1.1;

// conversion functions found at:
// https://stackoverflow.com/questions/13806483/increase-or-decrease-color-saturation

RGBtoHSV= function(color) {
        var r,g,b,h,s,v;
        r= color[0];
        g= color[1];
        b= color[2];
        min = Math.min( r, g, b );
        max = Math.max( r, g, b );


        v = max;
        delta = max - min;
        if( max != 0 )
            s = delta / max;        // s
        else {
            // r = g = b = 0        // s = 0, v is undefined
            s = 0;
            h = -1;
            return [h, s, undefined];
        }
        if( r === max )
            h = ( g - b ) / delta;      // between yellow & magenta
        else if( g === max )
            h = 2 + ( b - r ) / delta;  // between cyan & yellow
        else
            h = 4 + ( r - g ) / delta;  // between magenta & cyan
        h *= 60;                // degrees
        if( h < 0 )
            h += 360;
        if ( isNaN(h) )
            h = 0;
        return [h,s,v];
    };

HSVtoRGB= function(color) {
        var i;
        var h,s,v,r,g,b;
        h= color[0];
        s= color[1];
        v= color[2];
        if(s === 0 ) {
            // achromatic (grey)
            r = g = b = v;
            return [r,g,b];
        }
        h /= 60;            // sector 0 to 5
        i = Math.floor( h );
        f = h - i;          // factorial part of h
        p = v * ( 1 - s );
        q = v * ( 1 - s * f );
        t = v * ( 1 - s * ( 1 - f ) );
        switch( i ) {
            case 0:
                r = v;
                g = t;
                b = p;
                break;
            case 1:
                r = q;
                g = v;
                b = p;
                break;
            case 2:
                r = p;
                g = v;
                b = t;
                break;
            case 3:
                r = p;
                g = q;
                b = v;
                break;
            case 4:
                r = t;
                g = p;
                b = v;
                break;
            default:        // case 5:
                r = v;
                g = p;
                b = q;
                break;
        }
        return [r,g,b];
    }

SATURATE= function(rgb_color, saturation_level) {
   var hsv_color = RGBtoHSV(rgb_color);
   hsv_color[1] *= saturation_level;
   return HSVtoRGB(hsv_color);
}

// var html = document.querySelector('html');
// var walker = document.createTreeWalker(html, NodeFilter.SHOW_TEXT, 
//     {
//         acceptNode: (node) => {
//             if (node.parentNode.nodeName === 'SCRIPT' || node.parentNode.nodeName === 'STYLE') {
//                 return NodeFilter.FILTER_REJECT;
//             }
//             else { return NodeFilter.FILTER_ACCEPT; }
//         }
//     }
// );

chrome.storage.sync.get({fromStored: "", toStored: "", turnedOn: true}, function(result) {
    if (turnedOn) {
        var html = document.querySelector('html');
        var walker = document.createTreeWalker(html, NodeFilter.SHOW_TEXT);
        var node;
        while (node = walker.nextNode()) {
            node.nodeValue = node.nodeValue.replace(/the /gi, 'WHAT');
        }
    }
});

// var node;
// while (node = walker.nextNode()) {
//     node.nodeValue = node.nodeValue.replace(/(?<=\bthe\s)\w+/gi, 'fart');
// }

// for (var i = 0; i < elements.length; i++) {
//    var element = elements[i];

//    var color = getComputedStyle(element).color;
//    var rgb = color.match(/\d+/g).map(Number);

//    var new_color = SATURATE(rgb, SATURATION_CONSTANT);
//    var new_color_string = `rgb(${new_color[0]} ${new_color[1]} ${new_color[2]})`

//    element.style.setProperty(
//       "background-color", 
//       new_color_string);
// }
