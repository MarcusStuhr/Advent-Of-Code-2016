from hashlib import md5

DOOR_ID = "cxdnnyjw"
PASSWORD_LENGTH = 8

password = ""
index = 0
while len(password) < PASSWORD_LENGTH:
    hash = md5((DOOR_ID + str(index)).encode('utf-8')).hexdigest()
    if hash.startswith("00000"):
        password+=hash[5]
    index+=1
print(password) #part 1 answer

password = [-1]*PASSWORD_LENGTH
positionsUsed = set()
index = 0
while len(positionsUsed) < PASSWORD_LENGTH:
    hash = md5((DOOR_ID + str(index)).encode('utf-8')).hexdigest()
    if hash.startswith("00000") and hash[5].isdigit():
        positionToInsert = int(hash[5])
        charToInsert = hash[6]
        if positionToInsert < PASSWORD_LENGTH and positionToInsert not in positionsUsed:
            password[positionToInsert] = charToInsert
            positionsUsed.add(positionToInsert)
    index+=1
print(''.join(map(str, password))) #part 2 answer