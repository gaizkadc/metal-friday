# metal-friday
Metal Friday! Fuck yes!

This bot:
* retrieves a list of albums
* creates a video with the covers of the albums and adds some cool music to it
* tweets it to your account

## Environment variables
Some env vars can be provided:
* `APP_NAME`: something like `metal-friday`.
* `LOGS_FOLDER_PATH`: could be just `logs`.
* `INPUT_FOLDER_PATH`: could be just `input`.
* `OUTPUT_FOLDER_PATH`: could be just `output`.
* `CONSUMER_KEY`: your Twitter consumer key.
* `CONSUMER_SECRET`: your Twitter consumer secret.
* `ACCESS_TOKEN`: your Twitter access token.
* `ACCESS_TOKEN_SECRET`: your Twitter access token secret.

Additionally, a `settings.py` can be created to avoid having to pass all this env vars. To check its format, just rename `settings.py.sample` to `settings.py` and fill in your actual preferences and credentials.

## Considerations
* 8 albums max, as Twitter won't allow videos longer than 30s
* folder format for every Metal Friday: `YYYYMMdd`  
* check the `example_input_folder` to see how the list of albums and covers must be passed:
    * list format: `band_twitter_user | band name | album name` for each entry
    * cover must be `jpeg`, `png` or `webp`
