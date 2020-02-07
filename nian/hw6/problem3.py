from random import randrange

class Board:
    ## 15 15 matrix representing the scrabble board.
    def __init__(self, shape=(15, 15)):
        self.shape = shape
        self._board = [['_' for i in range(shape[1])] for i in range(shape[0])]

    def __str__(self):
        header_list = ["  "]
        for i in range(len(self._board[0])):
            header_list.append('{:>2}'.format(i))
        res = [" ".join(header_list), ]

        for i, row in enumerate(self._board):
            row_list = ["{:>2}".format(i), ]
            for x in row:
                row_list.append("{:>2}".format(x))
            res.append(" ".join(row_list))
        return "\n".join(res)

    def place_word(self,word,i,j,direction):
        i = int(i)
        j = int(j)
        if direction == 'across':
            for letter in word:
                self._board[i][j] = letter
                j = j+1
        if direction == 'down':
            for letter in word:
                self._board[i][j] = letter
                i = i+1

    def check_intersection(self,word,i,j,direction,round1):
        i = int(i)
        j = int(j)
        flag = False
        print()
        if direction == 'across':
            for letter in word:
                if self._board[i][j] == letter:
                    flag = True
                j = j+1
        if direction == 'down':
            for letter in word:
                if self._board[i][j] == letter:
                    flag = True
                i = i+1
        if round1 == 1:
            flag = True
        return flag

    def display(self):
        print([str(i) for i in range(16)])
        row = 0 
        for i in self._board:
            print(row,i)
            row = row + 1

## check your input is in the dictionary
    def check_dictionary(self,filename,word):
        flag= False
        dictionary = []
        lines = open(filename,"rb").read().split()
        for l in lines:
            l = l.decode("utf-8")
            dictionary.append(l)

        for w in dictionary:
            if w == word:
                flag = True
        return flag

## check your input is in 7 letters considering what is on the board.
    def check_currentletter(self,current_letter,word,i,j,direction):
        i = int(i)
        j = int(j)
        ## check the letter of word is in current_letter
        ## if not, check the letter is in board
        ## if not return false
        flag1 = True
        ## flag2 is to check whether the board already have the letter.
        if direction == 'across':
            for letter in word:
                if ((letter in current_letter) or (letter == self._board[i][j])) == False:
                    flag1 = False
                j = j+1

        if direction == 'down':
            for letter in word:
                if ((letter in current_letter) or (letter == self._board[i][j])) == False:
                    flag1 = False
                i = i+1
        return flag1

#############################################
class player:
    # A list of letters that the player currently has
    # The player’s current score
    # Method(s) for updating the list of letters and score
    def __init__(self,name):
        self.name = name
        self.score = 0
        self.current_letter = []
        self.bag = LetterBag()
    

    def choose_word(self,input):
        ## check in dictionary or not?
        parse = input.strip().split()
        word = parse[0]
        i = parse[1]
        j = parse[2]
        direction =parse[3]
        return (word,i,j,direction)

    ## get more letter up to 7
    def get_letter(self,bag):
        if len(self.current_letter) == 7:
            return self.current_letter
        else:
            for i in range(7-len(self.current_letter)):
                self.current_letter.append(bag.random_pull())
      
    def update_score(self,word):
        LETTER_VALUES = {"a": 1,
                 "b": 3,
                 "c": 3,
                 "d": 2,
                 "e": 1,
                 "f": 4,
                 "g": 2,
                 "h": 4,
                 "i": 1,
                 "j": 8,
                 "k": 5,
                 "l": 1,
                 "m": 3,
                 "n": 1,
                 "o": 1,
                 "p": 3,
                 "q": 10,
                 "r": 1,
                 "s": 1,
                 "t": 1,
                 "u": 1,
                 "v": 4,
                 "w": 4,
                 "x": 8,
                 "y": 4,
                 "z": 10}
        for letter in word:
            if letter in LETTER_VALUES:
                self.score = self.score + LETTER_VALUES[letter]
            else:
                self.score = self.score

    def remove_letters(self,word):
        for letter in word:
            for i in self.current_letter:
                if letter == i :
                    self.current_letter.remove(i)
                else:
                    continue

######################################################3
class LetterBag:
    def __init__(self):
        l = [['a']*9,['b']*2,['c']*2,['d']*4,['e']*12,['f']*2,['g']*3,['h']*2,
        ['i']*9,['j']*1,['k']*1,['l']*4,['m']*2,['n']*6,['o']*8,['p']*2,['q']*1,
        ['r']*6,['s']*4,['t']*6,['u']*4,['v']*2,['w']*2,['x']*1,['y']*2,['z']*1]
        a = []
        for sublist in l:
            for item in sublist:
                a.append(item)
        self.collection = a



    def random_pull(self):
        index = randrange(0,len(self.collection))
        return self.collection[index]


###################################################
class Game:

    def __init__(self):
        self.board = Board()
        self.players = []
        self.bag = LetterBag()

## switch players each round
## this method can also check the error if you do not input any player
    def switch_player(self,players,round1):
        if len(players) == 0:
            raise ValueError("no player!")
        if len(players) == 1:
            return players[0]
        else:
            index = ((round1-1) % len(players))
            return players[index]

## This method update board and players each round.
    def next_play(self,p,input1):
        ## word
        word,i,j,direction = p.choose_word(input1)
        ## validation

        ## update the board
        self.board.place_word(word,i,j,direction)
        self.board.display()
        ## update the players
        p.remove_letters(word)
        p.get_letter(self.bag)
        p.update_score(word)
        print(p.name+"  score is: "+ str(p.score))
        p.get_letter(self.bag)
        print(str(p.name) + "'s current letter are :" + str(p.current_letter))


## the main method
    def main(self):
        player_list = input("Who will play?")
        ## initialte all the players you give
        for p in player_list.split():
            self.players.append(player(p))
        round1 = 1
        ## switch to the first player,display the board and get 7 letters from bag.
        p = self.switch_player(self.players,round1)
        self.board.display()
        p.get_letter(self.bag)
        while True:
            ## player keep the same as long as the round1 does not change.
            p = self.switch_player(self.players,round1)
            print(str(p.name)+"'s round")
            p.get_letter(self.bag)
            print(str(p.name) + "'s current letter are :" + str(p.current_letter))
            try:
                next_move = input("enter word, i, j, and direction: ")
                ## if Exit the game, print the highest score player's name. If equal, print all of them.
                if next_move == "EXIT":
                    max1 = 0
                    for p1 in (self.players):
                        if p1.score > max1:
                            max1 = p1.score
                    for p2 in (self.players):
                        if p2.score == max1:
                            print(str(p2.name)+"   Won !")
                    break

                ## If this step has error, it means that your input is in wrong format, then my program
                ## will give an exception as "wrong input format"
                word,i,j,direction = p.choose_word(next_move)

                ## check your input is in you 7 letters.
                if self.board.check_currentletter(p.current_letter,word,i,j,direction) == False:
                    print("you choose a word not in these 7 letters")
                    continue
                ## check your inputs has intersection with word on the board.
                if self.board.check_intersection(word,i,j,direction,round1) == False:
                    print("no intersection!")
                    continue
                ## check your inputs is in your dictionary.
                if self.board.check_dictionary('words.txt',word) == False:
                    print("not in the dictionary or you do not import word.txt file!")
                    continue
                else:
                    self.next_play(p,next_move)
                    round1 = round1+1

            except Exception as e:
                print("wrong input format")


if __name__ == '__main__':
    
    game = Game()
    game.main()