const Jimp = require('jimp');
const fs = require('fs');
const parse = require('csv-parse');

var inputFile = 'nouns.csv';
var cardData = [];
var parser = parse({delimiter:','},function(err,data){
    data.forEach(function(line){
        cardData.push(line);
    });
    console.log(cardData);
});
fs.createReadStream(inputFile).pipe(parser);



//747x1122 at 300dpi
let CARD_WIDTH_300DPI = 747;
let CARD_HEIGHT_300DPI = 1122;
let CARD_BACKGROUND_COLOR = Jimp.rgbaToInt(255, 255, 255, 255); // e.g. converts 255, 255, 255, 255 to 0xFFFFFFFF

function createCard(cardId,filepath){
    let image = new Jimp(CARD_WIDTH_300DPI,CARD_HEIGHT_300DPI,CARD_BACKGROUND_COLOR,(err, image) => {
        console.log("error making image");
    });

    Jimp.loadFont(Jimp.FONT_SANS_32_BLACK).then(font => {
        image.print(font, 10, 10, cardData[cardId][0]);

        image.write(filepath,(successful,image) =>{
            console.log("successfully saved image to file");
        }); // Node-style callback will be fired when write is successful
    });
    //image.rgba(false); // set whether PNGs are saved as RGBA (true, default) or RGB (false)
    //image.filterType(number); // set the filter type for the saved PNG
    //image.deflateLevel(number); // set the deflate level for the saved PNG
    //Jimp.deflateStrategy(number); // set the deflate for the saved PNG (0-3)
    
    image.write(filepath,(successful,image) =>{
        console.log("successfully saved image to file");
    }); // Node-style callback will be fired when write is successful
}

createCard(1,'test.png');

