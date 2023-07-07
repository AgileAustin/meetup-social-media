## meetup-social-media
Automatic posting of Agile Austin Meetup events on social media (LinkedIn, Facebook, Twitter, and Slack).

## Problem Statement
Agile Austin uses Meetup to publicize its online and in-person events. Currently, there is no automated solution to then send announcements of these posts to social media networks, where additional prospective attendees can learn about the events.

## Solution
Agile Austin has developed a solution that utilizes [Pipedream](https://pipedream.com) to interact with APIs from the following services:

* [Meetup API](https://www.meetup.com/api/general/)
* [Slack API](https://api.slack.com/)
* [LinkedIn API](https://developer.linkedin.com/product-catalog)
* [Twitter API](https://developer.twitter.com/en/docs/twitter-api)
* [Facebook API](https://developers.facebook.com/docs/) 

## Pipedream Configuration

Pipedream offers low code and no code solutions for interacting with popular services. Of the ones mentioned above, Pipedream's no code solution is used for:

* Slack
* Twitter
* Facebook

Low code is required for:

* Meetup
* LinkedIn

The Pipedream job is run every day at 9 AM Central Time. When triggered, it:

* Connects to the Meetup API to scrape the upcoming events for Agile Austin. [01-meetup.js](01-meetup.js)
* Compares the title of events that it finds to what is available in a Pipedream key/value map store. [02-compare-meetup-to-datastore.py](02-compare-meetup-to-datastore.py)
* If it finds the event already in the key/value map store, it exits. [03-slack-no-code.txt](03-slack-no-code.txt)
* If it does not find the event, it proceeds to connect to the Slack API via a no code step and send a message in the Agile Austin Slack channel with details for the event. [04-linkedin.py](04-linkedin.py)
* It then connects to the LinkedIn API via a low code step and sends details about the Meetup invite to the [Agile Austin LinkedIn feed](https://www.linkedin.com/company/3707917). [05-twitter-no-code.txt](05-twitter-no-code.txt)
* After that, it connects to the Twitter API via a no code step and sends details about the Meetup invite to the [Agile Austin Twitter feed](twitter.com/agileaustin). [06-facebook-no-code.txt](06-facebook-no-code.txt)
* After that, it connects to the Facebook API via a no code step and sends details about the Meetup invite to the [Agile Austin Facebook feed](https://www.facebook.com/AgileAustin/). [07-append-to-data-store-no-code.txt](07-append-to-data-store-no-code.txt)
* Finally, it will add the event to the Pipedream key/value map store for comparison on future runs, and then it exits.

Visually, this looks like the following sequential diagram (Facebook is not represented, but you get the point :).

![pipedream-aa](https://github.com/benson8/meetup-social-media/assets/1530537/999a5f20-3b4b-44e0-90dc-1798be778b1d)


