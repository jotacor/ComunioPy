#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from ComunioPy import Comunio
import configparser
import time

config = configparser.ConfigParser()
config.read('../../config.conf')
if not config.has_section('comunio'):
    config.read('config.conf')
    
user=config.get('comunio','user')
passwd=config.get('comunio','passwd')

test = Comunio(user,passwd,'BBVA') # set username and password
test.login()

time.sleep(1)
print("ID: %s" % test.id)
print("Money: %s" % test.money)
print("TeamValue: %s" % test.teamvalue)
print("Title: %s" % test.title)
print("Community ID: %s" % test.community_id)

#===============================================================================
# time.sleep(1)
# print '\n[*] Standings:'
# for i in test.standings():
#     print i
#===============================================================================


#===============================================================================
# time.sleep(1)
# print '\n[*] Info user:'
# for i in test.info_user(test.id):
#     print i
#===============================================================================


#===============================================================================
# time.sleep(1)
# print '\n[*] Lineup user:'
# for i in test.lineup_user(test.id):
#     print i
#===============================================================================


#===============================================================================
# time.sleep(1)
# print '[*] Info community:\n'
# for i in test.info_community('test.community_id'):
#     print i
#===============================================================================


#===============================================================================
# time.sleep(1)
# print '\n[*] Info player:'
# fb_id=test.info_player_id('alcacer')
# print test.info_player(fb_id)
#===============================================================================


#===============================================================================
# plist = []
# x,plist = test.club(test.getteamID('Real Madrid'))
# print "Team: %s"%x
# for i in plist:
#     print i
#===============================================================================


#===============================================================================
# print "\n[*] News"
# for i in test.get_news():
#     print i
#===============================================================================


#===============================================================================
# time.sleep(1)
# print '\n[*] Get your bids:'
# for i in test.bids_from_you():
#     print i
#===============================================================================


#===============================================================================
# time.sleep(1)
# print '\n[*] Get bids to you:'
# for i in test.bids_to_you():
#     print i
#===============================================================================

#===============================================================================
# time.sleep(1)
# print '\n[*] Players on sale:'
# for player in test.players_onsale(test.community_id, only_computer=False):
#     print player
#===============================================================================

test.logout()
