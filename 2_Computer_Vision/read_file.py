
crimefile = open('data_all_classes.txt', 'r')
yourResult = [line.rstrip('\n') for line in crimefile.readlines()]
print(yourResult)