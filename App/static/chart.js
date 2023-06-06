
function decodeHtmlEntities(encodedString) {
    var textArea = document.createElement('textarea');
    textArea.innerHTML = encodedString;
    return textArea.value;
    };
for (var i = 0; i < x.length; i++) {
    var decodedString = decodeHtmlEntities(myArray[i]);
    console.log(decodedString);
    // Utilisez la chaîne de caractères décryptée comme souhaité
};