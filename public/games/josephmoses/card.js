var socket = io.connect('/');

socket.on('connect',function(data){});

let CARD_WIDTH_300DPI = 747;
let CARD_HEIGHT_300DPI = 1122;
//let CARD_BACKGROUND_COLOR = Jimp.rgbaToInt(255, 255, 255, 255); // e.g. converts 255, 255, 255, 255 to 0xFFFFFFFF

let backgroundImage = new Image();
backgroundImage.src = "bridge-size-nlbc-purple-base.png";

backgroundImage.onload = function(){
  let c = document.createElement('canvas');
c.id = "cId";
c.width = CARD_HEIGHT_300DPI;
c.height = CARD_HEIGHT_300DPI;
c.style.zIndex = 8;
c.style.position = "absolute";
c.style.border = "1px solid";
var b = document.getElementsByTagName("body")[0];
b.appendChild(c);

let ctx = c.getContext("2d");
// ctx.fillStyle = "rgba(255, 0, 0, 0.2)";
// ctx.fillRect(100, 100, 200, 200);
// ctx.fillStyle = "rgba(0, 255, 0, 0.2)";
// ctx.fillRect(150, 150, 200, 200);
// ctx.fillStyle = "rgba(0, 0, 255, 0.2)";
// ctx.fillRect(200, 50, 200, 200);
// roundRect(ctx,300,300,300,200,50);


ctx.drawImage(backgroundImage,(CARD_HEIGHT_300DPI-CARD_WIDTH_300DPI)/2,0);

//그레이프스2포도
//Grapes2Podo
var texts = [
    "Joseph's Coat of Many Colors",
    "Jacob loved Joseph more than any of his other children because Joseph had been born to him in his old age. So one day Jacob had a special gift made for Joseph—a beautiful robe.",
    "Genesis 37:3",
    "요셉의 화려한 겉옷",
    "야곱은 노년에 요셉을 얻었으므로 다른 아들보다 그를 특별히 사랑하여 화려하게 장식한 긴 겉옷을 만들어 입혔다.",
    "창세기 37:3"
];

var heights = [280,120,10];
var fontSizes = [60,24,36];
var widths = [1200,350,350];

function addText(text,startY,fontSize,width,talign="center"){
    var lines = [];
    var line = '';
    var lineTest = '';
    var words = text.split(' ');
    var currentY;
    //ctx.font = fontSize+"px Comic Sans MS";
    ctx.font = fontSize+"px Helvetica, sans-serif";
    ctx.fillStyle = "rgba(0, 0, 0, 1.0)";
    ctx.textAlign = talign;

    for (var i = 0, len = words.length; i < len; i++) {
        lineTest = line + words[i] + ' ';
    
        // Check total width of line or last word
        if (ctx.measureText(lineTest).width > width) {
            // Calculate the new height
            currentY = lines.length * fontSize + fontSize;
    
            // Record and reset the current line
            lines.push({ text: line, height: currentY });
            line = words[i] + ' ';
        } else {
            line = lineTest;
        }
    }
      
    // Catch last line in-case something is left over
    if (line.length > 0) {
        currentY = lines.length * fontSize + fontSize;
        lines.push({ text: line.trim(), height: currentY });
    }
      
    // Visually output text
    for (var i = 0, len = lines.length; i < len; i++) {
        ctx.fillText(lines[i].text, c.width/2, startY+lines[i].height);
    }
    return startY+currentY;
}

let lastOffset = 0;
ctx.translate(c.width/2,c.height/2);
ctx.rotate(-Math.PI/2);
ctx.translate(-c.width/2,-c.height/2);
// ctx.textAlign = "left";
lastOffset = addText(texts[0],heights[0],fontSizes[0],widths[0]);

ctx.translate(c.width/2,c.height/2);
ctx.rotate(Math.PI/2);
ctx.translate(-c.width/2,-c.height/2);

lastOffset = addText(texts[1],heights[1],fontSizes[1],widths[1]);
lastOffset = addText(texts[2],heights[2]+lastOffset,fontSizes[2],widths[2]);


ctx.translate(c.width,c.height);
ctx.rotate(Math.PI);

ctx.translate(c.width/2,c.height/2);
ctx.rotate(-Math.PI/2);
ctx.translate(-c.width/2,-c.height/2);
lastOffset = addText(texts[3],heights[0],fontSizes[0],widths[0]);

ctx.translate(c.width/2,c.height/2);
ctx.rotate(Math.PI/2);
ctx.translate(-c.width/2,-c.height/2);

lastOffset = addText(texts[4],heights[1],fontSizes[1],widths[1]);
lastOffset = addText(texts[5],heights[2]+lastOffset,fontSizes[2],widths[2]);
}





setInterval(function(){
  let c = document.getElementById('cId');
  let b64 = c.toDataURL('image/png').replace(/^data:image\/(png|jpg);base64,/, ''); //strip off header from base64 imageData
  socket.emit('saveImage',{
    'filename':'card1.png',
    'b64':b64
  });
  location.reload(true);
    
},5000);










/**
 * Draws a rounded rectangle using the current state of the canvas.
 * If you omit the last three params, it will draw a rectangle
 * outline with a 5 pixel border radius
 * @param {CanvasRenderingContext2D} ctx
 * @param {Number} x The top left x coordinate
 * @param {Number} y The top left y coordinate
 * @param {Number} width The width of the rectangle
 * @param {Number} height The height of the rectangle
 * @param {Number} [radius = 5] The corner radius; It can also be an object 
 *                 to specify different radii for corners
 * @param {Number} [radius.tl = 0] Top left
 * @param {Number} [radius.tr = 0] Top right
 * @param {Number} [radius.br = 0] Bottom right
 * @param {Number} [radius.bl = 0] Bottom left
 * @param {Boolean} [fill = false] Whether to fill the rectangle.
 * @param {Boolean} [stroke = true] Whether to stroke the rectangle.
 */
function roundRect(ctx, x, y, width, height, radius, fill, stroke) {
    if (typeof stroke == 'undefined') {
      stroke = true;
    }
    if (typeof radius === 'undefined') {
      radius = 5;
    }
    if (typeof radius === 'number') {
      radius = {tl: radius, tr: radius, br: radius, bl: radius};
    } else {
      var defaultRadius = {tl: 0, tr: 0, br: 0, bl: 0};
      for (var side in defaultRadius) {
        radius[side] = radius[side] || defaultRadius[side];
      }
    }
    ctx.beginPath();
    ctx.moveTo(x + radius.tl, y);
    ctx.lineTo(x + width - radius.tr, y);
    ctx.quadraticCurveTo(x + width, y, x + width, y + radius.tr);
    ctx.lineTo(x + width, y + height - radius.br);
    ctx.quadraticCurveTo(x + width, y + height, x + width - radius.br, y + height);
    ctx.lineTo(x + radius.bl, y + height);
    ctx.quadraticCurveTo(x, y + height, x, y + height - radius.bl);
    ctx.lineTo(x, y + radius.tl);
    ctx.quadraticCurveTo(x, y, x + radius.tl, y);
    ctx.closePath();
    if (fill) {
      ctx.fill();
    }
    if (stroke) {
      ctx.stroke();
    }
  
  }