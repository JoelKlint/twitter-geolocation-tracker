const superagent = require('superagent')
const cheerio = require('cheerio')

const locations = [
    "Woonsocket, Rhode Island",
    "San Marcos, CA",
    "Arizonugh, USA",
    "Dorset",
    "Godamn Usa",
    "Woodinville, WA.",
    "Wherever this RV takes us, USA",
    "With JC",
    "DeWitt, MI",
    "Trabuco Cyn, CA",
    "Dunellen",
    "Poetry texas",
    "Tuscaloosa, AL USA",
    "Tri-State Area",
    "Wherever my muse takes me.",
    "Dupont, IN",
    "eaglerock ca",
    "CF10",
    "Deus, qui est a figmento",
    "Punkin' Bottom,Alabama",
    "Ceres, Ca",
    "Jasper, GA",
    "Osaka",
    "Oregon, WI",
    "Dublin City, Ireland",
    "somewhere in the mitten",
    "Down on your muffin",
    "Lubbock, TX  and NYC",
    "Flat 6, Door 10, NW2 5TA",
    "DARK SIDE OF MOON",
    "Central Point, OR",
    "Waterloo, IL",
    "Crested Butte, CO",
    "Verona, NJ",
    "lafayette, la",
    "West Springfield, VA",
    "In Custody",
    "Kaltland",
    "the place",
    "Madison-WI",
    "People's Republic Of Arizona",
    "La Verne, CA.",
    "not where I dreamed of!",
    "Not Where I Want To Be",
    "Bacolod City",
    "Sofia Bulgaria",
    "Meadow Bridge, WV",
    "The great state of Missouri",
    "Majadahonda Madrid",
    "Nebraska, USA.  MAGA.",
    "front of house",
    "Secret Bunker",
    "Okiehoma",
    "Los Angeles, Ca 90049",
    "Dowagiac, Michigan",
    "Planet Earth 1.0",
    "Los Banos, CA",
    "Freedom Bay, USA",
    "Wragby, England",
    "Orion Spur: S. Milky Way",
    "toledo ohio Livin Large in the Rust Belt",
    "Concordia ,Kansas",
    "Pennsylvania",
    "jacksonville FL",
    "Marine City, MI",
    "Kingman Arizona",
    "hopewell va",
    "Wilkes Barre, PA",
    "Groveville, NJ",
    "大阪2号車両",
    "埼玉県羽生市【30人学級という位なので追加はやめておきます】",
    "Madison, Wi",
    "In a crazy blue state!!",
    "barnsley, south yorkshire",
    "Dansville, NY",
    "Small Town, USofA",
    "boro in the South USA",
    "Santo Domingo, Dominican Republic",
    "Venice Beach... aka Venus",
    "Jabba's Palace",
    "Marlton, New Jersey",
    "MIssouri",
    "Los Angeles, Red Gulch",
    "Phila.",
    "Mülheim",
    "Central Valley California USA",
    "Small corrupt-town in Ohio",
    "Germantown Ohio",
    "Cantonment, FL",
    "TDot ... Toronto, Salinas",
    "北海道札幌市手稲区",
    "feel like capn crunch",
    "East Norriton, PA",
    "New England",
    "hello...?",
    "Dirtayy B-Low",
    "CENTRAL NY",
    "Aruba",
    "cumming, ga",
]

const get_data_for_location = (location) => {

    const base_url = "http://www.google.com/maps?q="
    const request_url = base_url + location

    superagent
    .get(request_url)
    .then(res => {

        console.log("Current request")
        console.log(request_url)

        // Parse HTML
        $ = cheerio.load(res.text);

        // Only save the necessary stuff
        var textNode = $('script').get()[0].children[0].data
        var identifiers = ["cacheResponse(", ");"]
        var index = textNode.indexOf(identifiers[0])
        textNode = textNode.substring(index + identifiers[0].length)
        index = textNode.indexOf(identifiers[1])
        textNode = textNode.substring(0, index)

        // Parse JSON
        var json_string = JSON.parse(textNode)

        // Fetch the base array containing the interesting data
        var base_array = json_string[8]

        // Stop if there was no hit
        if(!base_array) {
            console.log("No data found")
            console.log("\n")
            return
        }

        // Fetch data
        var location_array = base_array[0]
        var latitude = location_array[2][0]
        var longitude = location_array[2][1]
        var city_and_country = location_array[1]

        var city_string = base_array[1]
        var country_array = base_array[2]

        console.log("Longitude: " + longitude)
        console.log("Latitude: " + latitude)
        console.log("City: " + city_string)
        console.log("Country: " + country_array)
        console.log("City and Country: " + city_and_country)
        console.log("\n")

    })
    .catch(err => {
        console.log(request_url)
        console.log("An error was caught")
        console.log("Status code: " + err.status)
        console.log("\n")
    })

}

// locations.map( location => {

//     get_data_for_location(location)

// })

get_data_for_location("Pennsylvania")