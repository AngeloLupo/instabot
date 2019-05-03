import json
import os

files = os.listdir('followers')
files.sort()

followers_file = open('followers/{}'.format(files[-1]))

followers = json.loads(followers_file.read())
followers = list(followers.keys())

files = os.listdir('following')
files.sort()

following_file = open('following/{}'.format(files[-1]))

following = json.loads(following_file.read())
following = list(following.keys())

people_i_follow_that_dont_follow_me = [x for x in following if x not in followers]

people_following_me_that_i_dont_follow = [x for x in followers if x not in following]

print("People I follow that don't follow me")
print(people_i_follow_that_dont_follow_me)
print("People following me that I don't follow")
print(people_following_me_that_i_dont_follow)

print("I follows {} people that don't follow me".format(len(people_i_follow_that_dont_follow_me)))
print("{} people follow me but I don't follow them".format(len(people_following_me_that_i_dont_follow)))
