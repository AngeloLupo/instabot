import json

file = open('followers/201810061944', 'r')
str_follow = file.read()
file.close()

str_follow = str_follow.replace('][', ']\n[')
pretty_list = str_follow.split('\n')

followers = []
for x in pretty_list:
    followers.append(eval(x))

new = []
old = []

js_fw = {}
for item in pretty_list:
    item = eval(item)
    js_fw[item[0]] = [item[1], item[2]]
    new.append(item)

json_fw = json.dumps(js_fw)
file2 = open('followers/d1', 'w')
file2.write(json_fw)
file2.close()

file = open('followers/first', 'r')
str_follow = file.read()
str_follow = str_follow.replace('][', ']\n[')
pretty_list = str_follow.split('\n')

for x in pretty_list:
    followers.append(eval(x))

js_fw = {}
for item in pretty_list:
    item = eval(item)
    js_fw[item[0]] = [item[1], item[2]]
    old.append(item)

json_fw = json.dumps(js_fw)
file2 = open('followers/d2', 'w')
file2.write(json_fw)
file2.close()

set_old = set(old)

set_new = set(new)

print(list(set_old-set_new))
