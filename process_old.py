followers_file = open('test_input', 'r')
followers_string = followers_file.read()

followers_list = followers_string.split('\\n')

pretty_list = []
counter = 0

list_len = len(followers_list)

for x in range(0, list_len):
    if counter + 1 > list_len:
        break
    if followers_list[counter + 1] == 'Follow' or followers_list[counter + 1] == 'Following':
        pretty_list.append(
            [
                followers_list[counter],
                '',
                followers_list[counter+1]
            ]
        )
        counter = counter + 2
    else:
        pretty_list.append(
            [
                followers_list[counter],
                followers_list[counter + 1],
                followers_list[counter + 2]
            ]
        )
        counter = counter + 3

file = 'followers/first'
with open(file, 'w') as f:
    for item in pretty_list:
        string_to_print = '{} {} {}\n'. format(item[0], item[1], item[2])
        f.write(str(item))
