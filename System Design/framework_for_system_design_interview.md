## No one expects you to design a real-world system in an hour
Then what is the benefit of a system design interview?\
An effective system design interview gives strong signals about a person's ability to collaborate, to work under pressure, and to resolve ambiguity constructively. The ability to ask good questions is also an essential skill, and many interviewers specifically look for this skill.

## Rate limiter
1. What kind of rate limiter are we going to design? Is it a client-side rate limiter or server-side API rate limiter?
2. Does the rate limiter throttle API requests based on IP, the user ID, or other properties?
3. What is the scale of the system? Is it built for a startup or a big company with a large user base?
4. Will the system work in a distributed environment?
5. Is the rate limiter a separate service or should it be implemented in application code?
6. Do we need to inform users who are throttled?

## Design a Key-Value Store
CAP: When choose consistency over availability,(for example bank system usually have extremely high consistent requirements), if inconsistecy occurs due to network partition, bank system returns an error before the inconsistency is resolved.

## Unique Id Generator in Distributed Systems
1. What are the characteristics of unique IDs?(unique and sortable)
2. For each new record, does ID increment by 1?
3. Do IDS only contain numerical values?(Yes)
4. Length requirement?(64bit=2^64-1 20digits)
5. What is the scale of the system?(规模 10,000 IDS/s)

summary: 
* IDs must be unique.
* IDs are numerical values only.
* IDs fit into 64-bit.
* IDs are ordered by date.
* Ability to generate over 10,000 unique IDs per second.

## URL Shortener
1. Can you give an example of how a URL shortener work?
2. traffic volume?
3. length of shortened URL?
4. update and delete?
* hash first 8 digits, conflict? predefined string hash first 8digist, bloom filter, not in db add, in db-conflict, predefined string hash again.
* increment 1 and base 62(for example 11157%62 = 59 -> X 179%62 = 55 -> T 2%62 = 0 -> 2, 2TX)

## Web Crawler
1. main purpose? (search engine indexing)
2. how many web pages does the web crawler collect per month? (1 billion)
3. content type? HTML only? (yes)
4. newly added and edited web pages?(yes)
5. store HTML pages crawled from the web? (yes, up to 5y)
6. duplicate content? (ignore)

## Notification System
1. what types of notifications does system support( PN, SMS, email)
2. real-time?(soft real-time)
3. supported devices(iOS, android, laptop/desktop)
4. opt-out?(yes)
5. how many notifications are sent out each day?(10m PN, 1m SMS, 5m email)

# News Feed System
1. what are the important feature?(publish post and see friends' posts)
2. ordered by most recent created?
3. how many friends can a user have?
4. traffic volume? (10m DAU)
5. feed content?(video and images)

## Chat System
1. 1 on 1 or group
2. mobile? web? both?
3. scale?(50m DAU)
4. group number limit?(100)
5. important features? support attachemnt?(chat, online indicator, only text messages)
6. message size limit?(100,000 chars long)
7. end-to-end encryption?
8. how long store chat history?

## Search AutoComplete
1. only support at the begining of a search query or in the middle as well?(only at the begining)
2. how many autocomplete suggestions should the system return?(5)
3. how does the system know which 5 suggestions to return?(populirity, historical query frenquency)
4. spell check?(no)
5. DAU(10m)

## Design Youtube
1. important features?(upload/watch videos)
2. what clients do we need to support(mobile apps, web browsers, smart TV)
3. DAU?(5m)
4. average daily time spent on the product? (30min)
5. international user?(yes)
6. video resolutions and formats?(accept most of video resolitions and formats)
7. encryption required?(yes)
8. file size limit?(max 1GB)
9. available to use existing cloud service?(yes)



