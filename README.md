# Pointboard
A bot that can track your progress in terms of points

Monsters that you cannot defeat alone; you have to defeat them with multiple players. The problem is that 'important' monsters give very few rewards. Not everyone will always get something. As players, we decided to work with a points system. After defeating monsters, we turn in all the rewards to the bank. For a specific monster, you get certain amount of points. The players can bid with their points, the player that bids the highest in a set time interval can redeem their reward from the bank.

The problem is, who or what keeps track of all the points for all the players?

This bot will help your team keep track of the amount of points everyone has.

## Important Note

There is a hierarchy involved in which who can use what.

'host commands', 'leader commands', and 'clansman commands' change message.channel.id to the appropriate channels.

Last line of code in main.py, you will need to insert the API key from your discord bot, make sure to hide the key well.

## Commands

**Host commands:**

%decay (starts decay)

%reset leaderboard (resets all points on leaderboard)

%reset everyone gp (resets everyones gained points)

%reset everyone tp (resets everyones total points)

%reset everyone lt (resets everyones lifetime points)

**Leader commands:**

%add player {name} {priority} {class} {subclass} (add player to database)

%delete player {name} (removes player from database)

%update player info {name} {priority/class/subclass} (changes player's info details)


%set tp {name} {dkp} (set player's total points to desired amount)

%set gp {name} {dkp} (set player's gained points to desired amount)

%set lt {name} {dkp} (set player's lifetime points to desired amount)


%buy {name} {dkp} (subtract amount of dkp from total points)

%give {name} {dkp} (add amount of dkp on total points)

%boss {bossname} {star} {playername1} {playername2} {etc....} (gives every participant amount of dkp from boss)

%camp {bossname} {playername1} {playername2} {etc....} (gives every participant amount of dkp from boss camping)

**Clansman commands:**

%leaderboard p1 (shows the leaderboard page 1)

%classboard {class} (shows leaderboard of class only type)

%score {name} (shows specific player status)

