Dinosaur Escape!
===============

Background
----------

In this problem, you will use Monte Carlo simulation to estimate the probability of a 
desired outcome in a stochastic process.  The idea is that you: 
1. Perform `n` independent simulations of a stochastic process
2. Count the number of desired outcomes (`m`)
3. Estimate the probability as `m/n`

For example, this would estimate the probability of rolling 7 on a pair of dice.  

    import random
    def got_seven():
        dice = list(range(1,7))
        return random.choice(dice) + random.choice(dice) == 7

    num_trials = 10000
    num_sevens = 0
    for i in range(num_trials):
        if got_seven():
            num_sevens += 1
    print(num_sevens/num_trials)
    
Note that we need a fairly large number of independent simulations to get close to the 
analytical answer (1/6).  In this case, the analytical answer is simple to derive, but 
Monte Carlo is a powerful tool for processes for which an analytical answer may be 
extremely difficult or practically impossible.

The Game
--------

My son and I play the board game "Dinosaur Escape".  The rules are in this repo 
(`dino_escape_rules.png`), and the manufacturers have a video tutorial here:

https://youtu.be/cn-o905A3aE?t=23

The game is cooperative (all players win or all players lose), and winning depends 
on both the players' memory and randomness.  Many preschoolers' games like this are
biased towards the players' winning, but it's hard to tell with this one.  

Your task is to estimate the probability of winning "Dinosaur Escape" by simulating 
the game many times.  Furthermore, you should provide an estimate for two different skill 
levels:
* A player that has perfect recollection of the fern tokens they've already turned-over
* A player that keeps turning over fern tokens randomly, with no recollection whatsoever

Approach
--------

Try to take an object-oriented approach.  This may rely on heavy use of composition.  Start
with a `Game` class that instantiates a new game.  It should at least have a method `play()` 
that runs the game to completion and returns true been won.  

Also consider how to implement the two skill levels.  It may be more reasonable to use 
inheritance, or it may be more reasonable to given an argument to `Game.play()` that 
specifies the skill level.

You can make use of any standard library modules, especially the `random` module 
(https://docs.python.org/3.7/library/random.html)
