ComunioPy
=========

Comunio API Python


Introduction
------------

It is a simple API to get the information from your Comunio account and use it for your benefit.

In this API you can see the difference between a player (football) and a user (who plays Comunio).

Comunio is a web game where you are a manager of a team.

Forked from:
[comuniopy-v0.1](https://github.com/sinkmanu/comuniopy)

Installation
-----------

```
python setup.py install
```


Usage
-----

### Config file for testing

You can use a config file with the user and login for testing.

```
[comunio]
user=USERNAME
passwd=PASSWORD
```

### Login into your account and get the information
```
	ComunioPy import Comunio
	test = Comunio(USER,PASS,LEAGUE)
	test.login()
	
	uid = test.get_myid()
	money = test.get_money()
	teamvalue = test.team_value()
```

### Get the latest news from your community
```
	from ComunioPy import Comunio
	test = Comunio(USER,PASS,LEAGUE)
	test.login()
	news = []
	news = test.get_news()
```

### Functions and methods

#### login()
#### logout()
#### load_info()
```
This function is included in login()
```
#### get_money(): string
#### get_myid(): string
#### get_team_value():string
#### get_title():string
#### get_news():list
#### standings():list
```
Get the standings of the community and return a list with the elements:
position    uid     player    points    teamvalue
``` 

#### info_player(userid): list
```
Get the	information of a user and return a list with:
name  email  community_name  points  name  number_notices  list_of_players
```

#### lineup_user(userid): list
```
Return a list with the name of players
```

#### info_comunity(teamid): list
```
position    uid    player    points    teamvalue
```

#### info_player(playerid): list
```
Return info about the football player.
[name,position,team,points,price]
```

#### info_player_id(name): string
```
Return ID of the football player name.
```

#### club(clubid): (string,list)
```
Get info about a real team players using a ID
teamname,[player list]
```

#### team_id(team): string
Returns the ID of a team to use with test.club(cid)
```
	cid = test.team_id('Valencia')
	players = []
	club,players = test.club(cid)
```

#### user_id(user):string
Get the ID of a real user.
```
	pid = test.user_id('username')
	info = []
	info = test.user_info(pid)
```

#### players_onsale(only_computer=False): list(list)
Returns the football players currently on sale.
Yout could retrieve only computer players on sale.
```
[[name, team, min_price, market_price, points, date, owner, position]]
```

#### bids_to_you(): list(list)
Get bids made to you.
```
[[player,owner,team,money,date,datechange,status],]
```

#### bids_from_you(): list(list)
Get your bids made for.
```
[[player,owner,team,money,date,datechange,status],]
```


Author
------
Javier Corbín (javi.corbin@gmail.com/[@korbin](https://twitter.com/korbin)/[Website](http://www.micolabs.com))

