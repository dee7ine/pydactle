import string

LETTERS = string.ascii_lowercase
LETTERS = list(LETTERS)


def clean() -> None:
    with open('wiki/titles_list_copy.txt', 'r+') as titles:
        print(LETTERS)
        
        lines = titles.readlines()
        print("i am here")
        for line in lines:
            if len(line) != 1 and '==' not in line:
                print(line)
                index = line.find('\n')
                line = "'" + line[0:index] + "'" + ',' + '\n'
                titles.write(line)
            else:
                print(line) 
                titles.write(line)
                
        
if __name__ == "__main__":
    clean()