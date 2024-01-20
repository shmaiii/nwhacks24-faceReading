const express = require('express');
const cors = require('cors')
const request = require('request');
const axios = require('axios');

const app = express();
app.use(express.json());
app.use(cors());

//APIS

//example endpoint
app.get("/app/helloworld", (req, res) => {
    res.send("Hello World");
})

app.get("/app/get_prophecy", (req, res) => {
    // this is a stub api to get prophecy
    // TODO: implement
    res.send('You are pretty af');
})

const PORT = process.env.PORT || 30001;
app.listen(PORT,() => {
    console.log(`Server running on port ${PORT}`);
})