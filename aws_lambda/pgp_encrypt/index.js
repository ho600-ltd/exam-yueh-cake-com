exports.handler = (event, context, callback) => {
    var openpgp = require('openpgp');
    var keys = [];
    for (var i in event.key_contents) {
        var key_content = event.key_contents[i];
        console.log("key_content: " + key_content);
        keys.push(openpgp.key.readArmored(key_content).keys[0]);
    }
    var raw_content = event.raw_content;
    console.log("raw_content: " + raw_content);
    var options = {data: raw_content, publicKeys: keys};
    openpgp.encrypt(options).then(function(ciphertext) {
        var encrypt_content = ciphertext.data;
        console.log("encrypt_content: " + encrypt_content);
        context.succeed(encrypt_content);
    });
};
