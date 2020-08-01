# Game Planning Portal - For serious gamers by the gamers!
 
 A portal that makes efficient squads of people trying to play games like Valorant,CounterStrike,PUBG,etc.
 

## The Backend
The backend server (ie this repo) is split up in the following components: 

- A Django+GraphQL webapp
- A SQLite Database for primary data storage

## Setting up the Server
 The following steps should help you set up the server:
 
  1. `git clone https://github.com/lminxous/game_planner`
 
  2. `cd game_planner`
  
  3. `pip3 install -r requirements.txt`
  
  4. `python manage.py runserver`
  
## Explanation of Models
A player must create a Listing for the game he wants to play with attributes:

    game
    start
    end

Here, start & end denote the waiting period of the user in isoformat.

In words:

`A wants to play PUBG on 16th May. He is free around 11pm-2am. `

This makes a Listing by user A. 

A Group is a squad of people who will play. A squad can have 1-4 members (members are Listings),with attributes:

    game
    start
    end

In words:

`A squad containing 3 people will play PUBG on 16th May anytime around 11pm-2am. `

The above makes a squad containing maximum 4 members. 

The server automatically adds a listing into an existing squad or creates a new squad when a new listing is created. 
A listing once created cannot be and _should not_ be changed. 
 
## The Algorithm
  
  ### A new listing is created
  Looks for half-filled groups of the specific game.

  #### Case 1. Set is not empty - Existing half filled groups of the specific game
  Find groups whose time_range(`(start, end)`) overlaps with the time_range of the listing & order them with decreasing overlap_range.
  ##### Case 1.1 Set is not empty - Existing half filled groups of the specific game with max overlap
  Add listing in half filled group with max overlap   
  ##### Case 1.2 Set is empty - No overlap with any existing half filled groups of the specific game
  Make a new group with the attributes same as that of the listing. The listing is a member of this new group. 
  #### Case 2. Set is empty - No Existing groups of the specific game
  Make a new group with the attributes same as that of the listing. The listing is a member of this new group. 
  
  Basically find the most suitable group. If no group exists , create a new group for the player
  
  
   
## Contributions & Roadmap
  If you wanna contribute, contact me. The following is the roadmap of things to be done:
  1. Implement Google authentication
  2. Making more effecient grouping method through ML

  If you are a Frontend developer or an App developer and are interested in making a frontend/application for this then hit me up. 
