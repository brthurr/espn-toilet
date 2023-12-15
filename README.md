# ESPN Fantasy Football Losers Tournament

## Overview

This web application is designed for Python developers who want to create a customized "Toilet Bowl" tournament using ESPN's Fantasy Football API. 

### Why do I care about this? Doesn't ESPN already have a consolation bracket?

Yes, ESPN does have a consolation-type bracket between the bottom teams in the league. But it sucks. It's more of a "participation-trophy" type scenario with a convoluted play-more-than-once system. It's not designed for the third most important activity in fantasy football:

- Crowning the champion
- The draft party
- Shaming the worst team in the league

The "Toilet Bowl" tournament is a losers' bracket that runs in parallel with the ESPN Fantasy Football playoffs, typically taking place during NFL weeks 15 to 17. Unlike ESPN's standard consolation bracket, this application allows you to create a fully automated "Toilet Bowl" tournament with custom rules and brackets.

## Features

### 1. "Toilet Bowl" Tournament
- The tournament is designed as a losers' bracket, where teams that were not successful in the regular playoffs have a chance to compete.
- The bottom six teams from your fantasy football league will participate in this bracket, and they will be seeded from 7th to 12th place based on their standings at the end of NFL week 14.

### 2. Custom Bracket Structure
- The tournament follows a custom bracket structure that includes multiple rounds.
- In week 15, seeds 11 and 12 receive a first-round bye, reducing the number of games they have to "lose" out of the tournament.
- During this week, team 7 plays against team 10, and team 8 plays against team 9, with no home-field advantage considered.

### 3. Automated Game Creation
- Unlike previous versions of the app, this version includes an automation feature for creating games between teams in each round of the tournament.
- Scores are automatically updated using the ESPN Fantasy Football API, eliminating the need for manual score entry.

## How to Use

To use this application effectively, follow these steps:

1. Set up your Python environment and ensure that the necessary dependencies, including the ESPN Fantasy Football API package, are installed.

2. Configure the app with your ESPN Fantasy Football league information, such as league ID and API credentials.

3. Define the custom rules for your "Toilet Bowl" tournament, including the number of participating teams, seeding, and the bracket structure.

4. Use the application to create and manage the "Toilet Bowl" tournament. The app will automatically create games for each round and update scores using the ESPN API.

5. Monitor the progress of the tournament and keep your league members engaged with this exciting losers' bracket.

## Additional Notes

This web application aims to enhance the experience of hosting a "Toilet Bowl" tournament within your ESPN Fantasy Football league. By automating the game creation and score updates, you can save time and ensure a smooth tournament for all participants.

Feel free to contribute to the project, make improvements, or adapt it to your specific needs. Enjoy hosting your "Toilet Bowl" tournament and providing your league members with an exciting competition for the bottom six teams!

**Disclaimer**: This application is not affiliated with ESPN or the NFL. It is a custom tool created by Python developers for fantasy football enthusiasts.
