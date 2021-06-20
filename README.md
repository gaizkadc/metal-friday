# metal-friday
Metal Friday! Fuck yes!

This bot:
* retrieves a list of albums
* creates a video with the covers of the albums and adds some cool music to it
* tweets it
* instagrams it

## Environment variables
Some env vars can be provided in an `.env` file:
```
APP_NAME=metal-friday
LOGS_FOLDER_PATH=logs

INPUT_FOLDER_PATH=input
OUTPUT_FOLDER_PATH=output
FONTS_PATH=fonts

TWITTER_POST=1
INSTAGRAM_POST=1

TWITTER_CONSUMER_KEY=<consumer key>
TWITTER_CONSUMER_SECRET=<consumer secret>
TWITTER_ACCESS_TOKEN=<access token>
TWITTER_ACCESS_TOKEN_SECRET=<access token secret>TWITTER_ACCESS_TOKEN_SECRET=gE3TD0Kmc39G5FEvEQKrhn9Yg8KTCKOmlw2wlq4cKR6mH

IG_USERNAME=<username>
IG_PASSWORD=<password>
```

## Considerations
* 8 albums max, as Twitter won't allow videos longer than 30s
* folder format for every Metal Friday: `YYYYMMdd`  
* check the `example_input_folder` to see how the list of albums and covers must be passed:
    * list format: `band_twitter_user | band name | album name` for each entry
    * cover must be `jpeg`, `png` or `webp`
