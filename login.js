
var CryptoJS = require("crypto-js");
function encryptByDES(message, key){
	var keyHex = CryptoJS.enc.Utf8.parse(key);
	var encrypted = CryptoJS.DES.encrypt(message, keyHex, {
		mode: CryptoJS.mode.ECB,
		padding: CryptoJS.pad.Pkcs7
	});
	return encrypted.ciphertext.toString();
}
let pwd = '293910xy'
var transferKey =  "u2oh6Vu^HWe40fj";
pwd = encryptByDES(pwd, transferKey);
console.log(pwd)