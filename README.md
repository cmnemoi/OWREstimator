# OWREstimator
A tool allowing you to judge if a world record is optimised compared to TAS.

# Objectives
 * Based on a dataset of existing World Record times and TAS time, we want to predict the time of the first TAS completed for a game.
 * We aim +/-10% of accuracy, +/-5% would be very good (under this is bonus !)

# Roadmap
## Data Collection
The plan is to use [Speedrun.com](speedrun.com)'s [API](https://github.com/speedruncomorg/api) to collect world records for games. 
We can easily get the **game's name**, runs's times (therefore the **WR before first TAS**), **regions** were it has been released, **developpers/editors**,**released year**,**engine**,**number of runs** ... a lot of interesting features for prediction.
The issue will be for the TAS times. We will try to develop a web scrapper to extract the data from [TASvideos](http://tasvideos.org).

### How will the data scrapper work ?
We want to go to http://tasvideos.org/Search.html?key="string" and replace string by the name of the game we want the TAS. Then :

 * To get the **TAS' time**, we click on the first result, find a way to click on "History of the entry" (probably taking the second li in the _tabbernav_ ul) then copy the content of the last link of the last _del_ of the _tabbertab_ div to get the time of the TAS.
 * We can get the **emulator** in which the TAS have been made by accessing the _misc_ class td's first link.
