Name: Sukesh Sangam
UIN: 01060894

Intructions:

requires python 3:

TO play the game run python play.py

The AI can win always if it visits till the end of the tree, for each decisions.

For now in this code I am asking the player, till which level can AI can visit as a difficulty level

Example output screenshot of the play is added in this folder.

The heuristic for calculation the score is 

like total chance of getting 4 in a row * 1000 + total chance of getting 3 in a row *100 + total chance of getting two in a row


The Minmax algorithm using alpha - beta prunning is also done, which is little bit faster than the original one.

Because it visists the unneccessary nodes in the tree while making decisions.

