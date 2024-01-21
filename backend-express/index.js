const express = require('express');
const cors = require('cors')
const request = require('request');
const axios = require('axios');

const app = express();
app.use(express.json());
app.use(cors());

const db = require('./db.json');

//APIS
app.get("/app/get_prophecy", (req, res) => {
    // req = {
    //     "face_shape": "oval",
    //     "eyebrows": ["high", "thin"],
    //     "forehead": "low_and_wide",
    // }
    const attributes = Object.keys(req);

    if (attributes.length === 0) {
        res.status(400).send("Please provide at least one attribute in the request.");
        return;
    }

    const descriptions = [];

    for (const attribute of attributes) {
        const value = req[attribute];
        const attributeObject = findAttributeDescription(attribute, value);
        descriptions.push({ [attribute]: attributeObject });
    }

    res.send({ descriptions });
});

function findAttributeDescription(attribute, value) {
    if (db[attribute]) {
        const attributeArray = db[attribute];

        if (Array.isArray(attributeArray) && Array.isArray(value)) {
            // Handle attributes with more than one key (eg. eyebrows)
            for (const item of value) {
                const itemDescription = attributeArray.find(obj => obj[item]);
                const description = itemDescription[item];
                descriptions.push({ [item]: description });
            }
            return descriptions;
        } else {
            // Handle attributes that take in a single key (eg. face_shape)
            return attributeArray.find(obj => obj[value]);
        }
    }

    return null;
}

const PORT = process.env.PORT || 30001;
app.listen(PORT,() => {
    console.log(`Server running on port ${PORT}`);
})