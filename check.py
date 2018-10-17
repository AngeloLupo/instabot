import json
import os


files = os.listdir('followers')
files.sort()

old_followers_file = open('followers/{}'.format(files[-2]))
new_followers_file = open('followers/{}'.format(files[-1]))

old_followers = json.loads(old_followers_file.read())
new_followers = json.loads(new_followers_file.read())

missing_followers = list(set(old_followers) - set(new_followers))

print('missing followers ({})'.format(len(missing_followers)))
print(missing_followers)

new_followers = list(set(new_followers) - set(old_followers))

print('new followers ({})'.format(len(new_followers)))
print(new_followers)
