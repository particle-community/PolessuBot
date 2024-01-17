# PolesSU Bot

![PolesSU Bot Picture]()

**[PolesSU Bot](https://t.me/polessu_schedule_bot)** is a **telegram bot** for viewing the class schedule of Polessky State University.

## Description

This **bot** is developed for PolesSU students. Its primary purpose is to provide quick access to the university's class schedule.

## Bot structure

The **bot** consists of three components:
- Client-side (the body of the bot and its handlers)
- Database (stores the schedule)
- Scraper (fetches the schedule and saves it to the database)

The client-side utilizes the schedule from the database and provides it to users.
The scraper allows fetching data from the university website, which is then saved in the database.
Currently, a separate script is used for this purpose.

*The actual structure of the project differs, but it will be refined over time.*

## License

## Changelog
