from database.database import Database

db = Database("twitter-geo")

print ("Connection Established")

file = open("allCountries.txt", 'r')


progress = 0

for line in file:
    entries = line.split('\t')
    remove_newline_from_last = entries[-1].split('\n')[0]

    i = 0
    for entry in entries:
        if entries[i] == '':
            entries[i] = None
        i+=1

    db.loadCountries(entries[0], entries[1], entries[2], entries[3], entries[4],
                     entries[5], entries[6], entries[7], entries[8], entries[9],
                     entries[10], entries[11], entries[12], entries[13], entries[14],
                     entries[15], entries[16], entries[17], remove_newline_from_last)
    progress += 1
    if (progress%100000 == 0):
        print ("Processed lines: ", progress)