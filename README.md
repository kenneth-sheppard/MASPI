# A Multi-Agent System Playing Imperial 2030



## Current Features

The game engine allows 2-6 players to play a game of Imperial 2030 using the fixed bond deal and investor card variants.
The four agents presented above are all included in the players folder, and a rudimentary interface allows for human play through the HumanPlayer class.
Any new agents can be easily swapped in, so long as they provide responses for each type of choice needed from a player.
The specific functions are in the Player file in the game engine folder.

The classes in statistics_observer offer basic capabilities of player tracking through one or multiple games.
Game results are stored in three different files.
First, a human-readable list of scores, win counts for each player, and a list of bonds held in each game are stored in recorded_results.txt.
Second, quick_stats.csv has player scores, superpower power values and rankings, along with game number and turn count.
Each line in quick_stats.csv is a single game's results.
Lastly, game_turns.csv is each turn of each game, expanded to the element representation used in training the Neural agent.
To make use of this last file, the record scribe folder holds some methods of extracting information from game_turns.csv to follow patterns across individual games and turns.
