Monte Carlo Chess

Python 3.8


###What is this?

This is a chess engine based on the monte carlo tree search method: https://en.wikipedia.org/wiki/Monte_Carlo_tree_search
Every game you play with the engine makes it better at playing, it only takes a few games for it to learn to 
prevent the scholar's mate.

The monte carlo method is interesting as the computer doesn't need to know every possible move to make a decision,
or even be loaded with chess heuristics to learn. When I was a kid my uncle would teach me things like
control the center, castle early, limit pawn movement etc. that helped me get better, but the computer picks things
up by trial and error by randomly trying different things. I.e. throw spaghetti at the wall and see what sticks


###How to Setup

`pip3 install -r requirements.txt`

###How to Play

Open python3 shell

```python
from monte import *
g.run()
```
Moves are made by typing the starting cell and the ending cell.

E.g. the king's gambit would be 'e2e4'

Promoting a pawn at the 8th rank is done by appending the symbol of the piece desired

E.g. 'e7e8q' would result in a pawn promotion to queen.

1-0 means you win
1/2-1/2 means draw
0-1 means the computer beat you.

```python
g.save() # saves your existing tree to a pickle file to read later
g.load() # loads your pickle file into g so the bot has some preexisting intelligence
```

###Next steps
* Set this up with an http server so that there can be a prettier GUI compared to the terminal
* Implement a new save method that doesn't use pickle as the tree is too recursive
* Rewrite the tree as a graph since there can be identical nodes in the tree that were reached by different paths
    * Not sure how complicated this would actually be to implement
* Let player retry their move if they type an illegal move instead of breaking the game


###Things learned
The limitations of python, I originally wanted to write this in Haskell since the tree uses much recursion,
but OOP paradigm is handier in my opinion since I want to have side effects on the tree used.
That being said python has no tail recursion so some functions originally written as recursive had to be
made imperative to prevent stack overflows as the tree grows large fairly quickly. If I were more familiar
with Scala I would have used that since it supports the OOP paradigm and the compiler can optimize tail recursion.