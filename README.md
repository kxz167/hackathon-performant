# HackCWRU 2022: Performant

## By Kris Zhao

Welcome to my Hack CWRU Fintech submission!

## Problem Statement:

Successful investments is all about managing risk and evaluating factors that may be beneficial. As such, there are many calculations, averages and metrics associated with it. Even more so with technicalities such as FIFO selling designations especially when it comes to tax calculations. All of this information can make the investment space hyper cluttered with simple fundamentals hidden to a user.

## Solution:

Performant hopes to remedy this by providing a single, simple, and semi-automated process for getting a high level overview of your investment portfolio. This could then inform you of your risk tolerance, or the general market trends. Perhaps it might even illustrate how bad you are at this, saving you money in the long run by pushing you towards safer strategies such as ETFs and Funds.

More in the details, Performant provides a simple account funding and transactions page, which pulls and calculates metrics automatically, then allows you to explore graphs and summary metrics. In this regard, it is heavily oriented as a summary tool and not meant for high frequency or intra day trading.

## Overal structure:

This project is organized into four primary components, the backend, market data source (TDAmeritrade API), a database, and frontend. Each folder will have more in depth READMEs but a high level overview is provided here:

### Backend

The backend for ths project is built up in `Python (3.8.6)` in anticipation of various calculations and aggregations as well as it's ability to simply link various components together. As a light weight API backend, I decided to use `Flask` running on my computer paired with the `requests` python library for API calls. Additionally, the Python backend had to connect with the database and used the `psycopg2` driver.

### Market Data:

Market data (price history) was queried through the TDAmeritrade developer API. This API requires a trading account with TDA as well as setup of a secondary developer account. This was chosen as it had an allotment of up to 120 requests per minute, or 2 requests per second. This was much better than the nearest competition.

For an alternative, Yahoo finance has a free tier which, out of development when this app would only make a low number of calls anyways, could suffice. It allows for 100 free requests per day.

### Database:

In order to manage all of the user information and calculations, I went ahead with a Postgres relational database. The reason was that I was more familiar with this (as apposed to a noSQL database), and hosting a local instance means there will be no latency or rate limiting.

The database ended up as version 14.2 running on a NAS and was able to serve all requests / queries with ease.

### Frontend:

Finally, everything on the user-facing side is taken care of with an Angular SPA. I like using angular for user interfaces because I believe web-based applications are easily scalable, deployable, and fast to create. The application was purely developed with the build in development server for ease hosted on my computer.