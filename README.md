# vinyl-price-suggester

This is a simple command line tool to generate a price suggestion for vinyl records using the Discogs API.

When you input a Discogs Release ID and record grade, the program will print a suggested sales price for the specific record.

To run this tool, create a file called **secret.py** in the vinyl_price_suggester directory containing the following:

```
PERSONAL_TOKEN = <your discogs personal access token here>
```

To generate a personal access token for use with the Discogs API, go to your Discogs account, and to go _Settings > Developers_ and click the "Generate New Token" button to generate your own personal access token.
