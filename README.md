This shonkily simulates several iterations of a 1v1 pokemon rby battle to give
you an idea what beats what.

You need to write code for each pokemon to decide what move it will choose. So
a function that takes a user and opponent and returns the move the user will
choose for that turn.

Then call battle. Pass in pokemon 1, pokemon 2, the function to select 1's move
and the function to select 2's move. It will run the battle and tell you who
won. To get actual meaningful results call battle thousands of times.

battle will return a tuple containing all the pokemon that 1. So either a
single element tuple that contains the winner, or if the tuple is length 2 then
it was a draw.

You can pass in a function to check the result as well. That function should
return a tuple of the pokemon that one, or an empty tuple (or False) if the
battle should continue.

There are examples in tauros\_wars.py and mie\_v\_chansey.py

* A lot of the moves I couldnt actually find accurate details on, so I just
guessed them? So yeah, its probably only accurate to within a couple of
percent or two.
* Also no tests, so pretty likely to just give wildly incorrect results anyway.
But it usually looks pretty sensible to me.
* The battle events get logged as DEBUG.
* 10,000 iterations quickly enough on my old Macbook.
