import json

old_followers_file = open('followers/d2')
new_followers_file = open('followers/d1')

old_followers = json.loads(old_followers_file.read())
new_followers = json.loads(new_followers_file.read())


missing_followers = list(set(old_followers) - set(new_followers))

print('missing followers ({})'.format(len(missing_followers)))
print(missing_followers)


new_followers = list(set(new_followers) - set(old_followers))

print('new followers ({})'.format(len(new_followers)))
print(new_followers)
