# homeful
> Find yourself a home
> https://blog.rodfer.cloud/blog/posts/rent_chaos.txt

## Motivation
> quick and dirty i wrote this late at night while wearing my blackhat hoodie, skipped sleep, grabbed two energy drinks one in each hand and got a room in the late afternoon
````
On a real life problem...
In 2022 I was looking to rent a room in London, but the market 
was at it's worse (and still is bad now), and I couldn't find a room
while working part time and doing my 3rd year of Computer Science.
I had to leave my current room before I was even able to find a place
as I was planning to move with friends and one of them decided with 
two days prior and part of the deposit paid to walk off the deal.
What happened at this point was that the market was so bad that finding
a place to stay was extremely difficult. You would have hundreds of people
interested in a room in London in less than 24. the agency people couldn't
handle all the demand, and the supply was shorter. If you wanted a property 
you needed to be the first person to schedule an interview in the shortest 
span of time. I went to plenty of terrible houses and really bad deals but 
I eventually found a good deal in less than a 4 days after over 2 months of search.
I was sleeping at some friend's sofa next week when I realised that I needed a 
creative solution to my problem so I spent an entire night programming a
solution. 
I wrote a bot to scrape and auto apply to rooms listed online and funnel as many 
phone numbers to WhatsApp as possible so I can schedule a house view as quickly as possible. 
The bot alerted and send me the number during class, I quickly scheduled a house
viewing and left right after my Decentralised and Secure Systems class, ran for
the house viewing and paid the deposit and got a nice place to live with a great garden for BBQs.
````

## Documentation
````
./.env -- USERNAME and PASSWORD env vars as HM_MAIL and HM_PASS
./data -- directory for data
./data/places.txt -- file for newline separated homes
./data/message.txt -- file for home searching message copy
./data/places_failed.txt -- autogenerated file for failed home messages (premium)
./data/places_spammed.txt -- autogenerated file for spammed places
./data/places_spammed.txt -- autogenerated file for cities/boroughs to search and add to places.txt
````

