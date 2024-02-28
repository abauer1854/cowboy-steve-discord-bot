import bot

def decode(message_file):
    # open and read file by line
    message_file = open(message_file, 'r')
    lines = message_file.readlines()

    # convert lines to a dictionary
    dict_lines = {}
    for line in lines:
        line = line.strip().split()
        dict_lines[int(line[0])] = line[1]
    message_file.close()

    # sort dict in ascending order by key
    dict_lines = dict(sorted(dict_lines.items()))   

    # assume that the first number of the pyramid starts with 1
    i = 1
    message = ""
    curr_num = 0
    while curr_num < len(dict_lines):
        curr_num = (i * (i + 1)) // 2 # formula for triangle/pyramid numbers is (n * (n + 1)) / 2
        message += dict_lines[curr_num] + " "
        i += 1
    
    return message.rstrip()

if __name__ == '__main__':
    print(decode('message_file.txt'))