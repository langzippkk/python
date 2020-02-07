Correct input: word row column down or across
i.e.  apple 1 1 down

When finished, enter EXIT


├── class Board
│   ├── __str__(self)
│   │ 
│   ├── place_word(self,word,i,j,direction)
│   ├── check_intersection(self,word,i,j,direction,round1)
│   ├── display(self):
│   ├── check_dictionary(self,filename,word)
│   │   
│   └── check_currentletter(self,current_letter,word,i,j,direction)

|
├── class player
│   ├── choose_word(self,input)
│   │ 
│   ├── get_letter(self,bag)
│   ├── check_intersection(self,word,i,j,direction,round1)
│   ├── update_score(self,word):
│   ├── remove_letters(self,word)
│   │   
├── class LetterBag
│   ├── random_pull(self)
│   │__ 

├── class Game
│   ├── switch_player(self,players,round1)
│   │ 
│   ├── next_play(self,p,input1)
│   ├── main(self)

main

