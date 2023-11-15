import sys
from random import randint
from enum import IntEnum
import sqlite3
import database
import tkinter


# uppercase letters
UPPER_CASE_LETTERS = [chr(L) for L in list(range(65, 91))]
# lowercase letters
LOWER_CASE_LETTERS = [chr(l) for l in list(range(97, 123))]
# numbers
NUMBERS = [chr(n) for n in list(range(48, 58))]
# special chars
SPECIAL_CHARS_FULL = list(range(33, 48)) + list(range(58, 65)) + list(range(91, 97)) + list(range(123, 127))
SPECIAL_CHARS_FULL = [chr(l) for l in SPECIAL_CHARS_FULL]

# Enumeration of values to avoid hardcoded numbers
class GeneratedCharacterType(IntEnum):
    UPPER = 1
    LOWER = 2
    NUMBER = 3
    SPECIAL = 4


# generate password of desired length
def generatePassword(passwordLength):
    password = ""
    securityChecks = [[False, 0] for i in range(GeneratedCharacterType.SPECIAL)] 
    
    for i in range(0, passwordLength): # only used to loop for password length chars
        # generate number(1-4)
        randomType = randint(GeneratedCharacterType.UPPER, GeneratedCharacterType.SPECIAL)
        if(randomType == GeneratedCharacterType.UPPER):
            password += UPPER_CASE_LETTERS[randint(0, len(UPPER_CASE_LETTERS) - 1)]
        elif(randomType == GeneratedCharacterType.LOWER):
            password += LOWER_CASE_LETTERS[randint(0, len(LOWER_CASE_LETTERS) - 1)]
        elif(randomType == GeneratedCharacterType.NUMBER):
            password += NUMBERS[randint(0, len(NUMBERS) - 1)]
        elif(randomType == GeneratedCharacterType.SPECIAL):
            password += SPECIAL_CHARS_FULL[randint(0, len(SPECIAL_CHARS_FULL) - 1)]

        # handle security checks
        securityChecks[randomType - 1][0] = True
        securityChecks[randomType - 1][1] += 1

    #print("Security checks:", securityChecks)
    
    for check in securityChecks:
        if(check[0] == False):
            print("Error, one or more character types not generated, reruning")
            return generatePassword(passwordLength)

    return (True, password)





# main function for password generation workflow
def mainGenerate(dbConnection):
    print("+--------------------+\n| Password Generator |\n+--------------------+")
    database.generateDBTable(dbConnection)

    pwLength = int(input("-> Password length(10-50 characters): "))
    
    if pwLength < 10:
        sys.exit("-> Desired password length is too short!")
    if pwLength > 50:
        sys.exit("-> Desired password length is too long!")
    
    status, generatedPassword = generatePassword(pwLength)
    
    print("\n+====================+\nGenerated password:", generatedPassword)
    print("Valid:", status, "\n+====================+\n")

    if(status == False):
        sys.exit("Error occured, please re-run the script!")

    savePassword = input("-> Save password in database (y/n): ")
    
    if(savePassword == 'Y' or savePassword == 'y'):
        description = input("-> Enter password description(max. 20 characters): ")
        if len(description) > 20:
            sys.exit("-> Description is too long!")
        elif len(description) == 0:
            sys.exit("-> Empty description not allowed!")
        
        database.insertPasswordInDB(dbConnection, generatedPassword, description, pwLength)
    
    print("-> Generation complete. Bye!")


# main method for displaying passwords
def mainView(dbConnection):
    print("Password viewer start")
    print("All entries in database:")
    database.readAll(dbConnection)
    print("View complete. Bye!")


# returns pass at certain description (uses wildcards)
def mainGetPasswordForDesc(dbConnection, desc):
    print("Get specific password viewer start")
    print("Required password:")
    database.readPassword(dbConnection, desc)
    print("View complete. Bye!")


# update password at desc
def mainUpdatePasswordForDesc(dbConnection,desc, newLength):
    print("Update password viewer start, newLength must match old length!")
    # read before update
    database.readPassword(dbConnection, desc)
    status, generatedPassword = generatePassword(int(newLength))
    if(status == False):
        sys.exit("Error occured, please re-run the script!")

    database.updatePassword(dbConnection, desc, generatedPassword, newLength)
    print("Updated password:")
    # read after update
    database.readPassword(dbConnection, desc)

    print("Update complete. Bye!")


if __name__ == "__main__":
    execMode = sys.argv[1]
    
    dbConnection = sqlite3.connect("pwadmin.db")

    if execMode == '-g' or execMode == '-generate':
        mainGenerate(dbConnection)
    elif execMode == '-v' or execMode == '-view':
        mainView(dbConnection)
    elif execMode == '-d' or execMode == '-description':
        mainGetPasswordForDesc(dbConnection, sys.argv[2])
    elif execMode == '-u' or execMode == '-update':
        mainUpdatePasswordForDesc(dbConnection, sys.argv[2], sys.argv[3])
    else:
        sys.exit("Supported modes [-g, -v, -d [desc], -u [desc] [newLength]")
    

    dbConnection.close()


