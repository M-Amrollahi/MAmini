According to recent events in Iran due to the murdered 22-year-old girl called [__Mahsa Amini__](https://en.wikipedia.org/wiki/Death_of_Mahsa_Amini), her name has been a trend on social media platforms like Twitter(__#MahsaAmini #مهسا_امینی__). She died on September 16, 2022, and since then, many protests have been held in Iran.
We are supposed to collect the data on Twitter related to her and analyze the data.

There are many packages(in pip) to collect the data from Twitter, but I have used the pure one, which uses the Curl to send and receive the requests and responses. However, for all apps, we need to have Twitter API Key, which you can get for different purposes (which means with different licenses). The API key can be registered on [Twitter Developer](https://developer.twitter.com/en/portal/dashboard).

There are some restrictions on Twitter API, so we cannot retrieve any data from it. It depends on the license that we have from Twitter. For example, if we want to search on tweets based on any phrase or hashtag, we have a limitation of 300 requests per 15 minutes, and in each request, we will get a maximum of 100 results(tweets). Overall, we have a limitation on the total number of tweets per month.

## Demo
The charts and illustrations have been implemented using [Streamlit](https://streamlit.io/) and they are available on [here](https://mahsaamini.streamlitapp.com/).

## Technical

As I have used the Curl to retrieve data from Twitter API, here is the URL we use:
```https://api.twitter.com/2/tweets/counts/all?query=(#MahsaAmini+OR+#مهسا_امینی)+-is:retweet+-is:retweet&start_time=2022-09-14T00:00:00Z&end_time=2022-09-30T04:23:06Z&```

Please note that we should send the Authorization Key in header of our HTTP request. The key is provided to you when you register an account on [Twitter Developer](https://developer.twitter.com).
