var express = require("express");
var app = express();
app.use(express.static("public")).listen(8080);

const http = require("http");
const https = require("https");
const url = require("url");

//https://121.12.76.25:443/por/login_psw.csp
//https://47.95.50.136:80/topics/350138133
var options = 
{
	host : "47.95.50.136",
	port : "80",
	path : "topics/350138133",
	method : 'GET',
}
https.request(options, function(res) {
	console.log("success.");
}).end();