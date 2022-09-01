import os
import time
import random
from sys import argv

play_easy = ['''

		 
		 
		 
		 
		 
		 
		 ''', '''


		 
		 
		 
		 
		 
=========''','''

	  +
	  ||
	  ||
	  ||
	  ||
	  ||
=========''','''

  +---+
	  ||
	  ||
	  ||
	  ||
	  ||
=========''','''

  +---+
  |   ||
	||
	||
	||
	||
=========''','''

  +---+
  |   ||
  O   ||
	||
	||
	||
=========''','''

  +---+
  |   ||
  O   ||
  |   ||
	||
	||
=========''','''

  +---+
  |   ||
  O   ||
 /|   ||
	||
	||
=========''','''

  +---+
  |   ||
  O   ||
 /|\  ||
	||
	||
=========''','''

  +---+
  |   ||
  O   ||
 /|\  ||
 /    ||
	||
=========''','''

  +---+
  |   ||
  O   ||
 /|\  ||
 / \  ||
	||
========= \n HANGED''']

play_hard = ['''

  +---+
  |   ||
	||
	||
	||
	||
=========''','''

  +---+
  |   ||
  O   ||
	||
	||
	||
=========''','''

  +---+
  |   ||
  O   ||
  |   ||
	||
	||
=========''','''

  +---+
  |   ||
  O   ||
 /|   ||
	||
	||
=========''','''

  +---+
  |   ||
  O   ||
 /|\  ||
	||
	||
=========''','''

  +---+
  |   ||
  O   ||
 /|\  ||
 /    ||
	||
=========''','''

  +---+
  |   ||
  O   ||
 /|\  ||
 / \  ||
	||
========= \n HANGED ''']

def getworddict():
	# Read All the words from the file
	with open('wordlist.txt', 'r') as f:
		words = list(filter(None, f.read().split('\n')))
		return words

class gameboard(object):

	def __init__(self, difficulty, wordlist, name):
		self.difficulty = difficulty
		self.words = wordlist
		self.name = name
		hangmanpics = ''

	def choosedifficulty(self, difficulty):	
		if self.difficulty == "easy":
			hangmanpics = play_easy
			return hangmanpics

		elif self.difficulty == "hard":
			hangmanpics = play_hard
			return hangmanpics
		else:
			hangmanpics = ''		
			print("Please select either EASY or HARD")
			return hangmanpics

	def displaygameboard(self, hangmanpics, missedLetters, correctLetters, secretWord):
		print(hangmanpics[len(missedLetters)])
		print()
		
		print("Missed Letters: ", end=' ')
		for letter in missedLetters:
			print(letter, end = ' ')
		print()
		
		blanks = '_' * len(secretWord)
		
		for i in range(len(secretWord)):
			#changes the guessed blanks
			if secretWord[i] in correctLetters:
				blanks = blanks[:i] + secretWord[i] + blanks[i+1:]
			
		for letter in blanks:
			print(letter, end=' ')
		
		print()
	
class GameLogic(object):

	def __init__(self, board):
		self.gameboard = board
		self.missedLetters = ''
		self.correctLetters = ''
		self.gameisdone = False
	
	def getRandomWord(self, wordList):
		new_list = []
		if self.gameboard.difficulty == 'easy':
			new_list = [word for word in wordList if len(word) <= 5]
		if self.gameboard.difficulty == 'hard':
			new_list = [word for word in wordList if len(word) >= 6]
		wordindex = random.randint(0, len(new_list)-1)
		return new_list[wordindex]
	
	def getGuess(self, alreadyGuessed):
		while True:
			print('Guess a letter...')
			guess = input('> ').lower()
			if len(guess) != 1:
				print("Please choose a single LETTER.")
			elif guess in alreadyGuessed:
				print("This letter is already used please check the list and choose another letter!!")
				print("USED WORDS :- ", alreadyGuessed)
			elif guess not in 'abcdefghijklmnopqrstuvwxyz':
				print("WRONG INPUT!!")
				time.sleep(0.5)
				print('\n'*4)
				print("Plese choose letter.")
			else:
				return guess
	
	def playagain(self):
		print('To play again type YES or NO.')
		return input('> ').lower().startswith('y')
	
	def oneguess(self, secretWord):		
		time.sleep(0.5)
		self.hangmanpics = self.gameboard.choosedifficulty(self.gameboard.difficulty)
		self.gameboard.displaygameboard(self.hangmanpics, self.missedLetters, self.correctLetters, secretWord)
		guess = self.getGuess(self.missedLetters + self.correctLetters)
		if guess in secretWord:
			self.correctLetters = self.correctLetters + guess
			foundAllLetters = True
			for i in range(len(secretWord)):
				if secretWord[i] not in self.correctLetters:
					foundAllLetters = False
					break
			if foundAllLetters:
				print('\n'*4)
				print("*"*60)
				print("*"," "*56,"*")
				print("*"," "*56,"*")
				print("*"," "*18,"!!PERFECT GUESS!!"," "*19,"*")
				print("*"," "*56,"*")
				print("*"," "*56,"*")
				print(" "," "*14,"The secreat word is %s" %(secretWord.upper(),))
				print(" "," "*8,"You have won with %d only incorrect guesses" %len(self.missedLetters)," "*3," ")
				print("*"," "*56,"*")
				print("*"," "*56,"*")
				print("*"*60)
				print('\n'*4)
				result_string = "\nScore of %s: SECRET WORD: %s  MISSED WORDS: %d " %(self.gameboard.name, secretWord.upper(), len(self.missedLetters))
				resultFile = open("results.txt", "a")
				resultFile.write(result_string)
				resultFile.close()
				self.gameisdone = True
		else:
			self.missedLetters = self.missedLetters + guess
			if len(self.missedLetters) >= len(self.hangmanpics) - 1:
				self.gameboard.displaygameboard(self.hangmanpics, self.missedLetters, self.correctLetters, secretWord)
				print("Sorry, you have run out of guesses! You have lost after %d correct guesses, %d incorrect guesses. The word was %s" %(len(self.correctLetters), len(self.missedLetters), secretWord))
				result_string = "\n %s is failed to guess the secreat word" % (self.gameboard.name)
				resultFile = open("results.txt", "a")
				resultFile.write(result_string)
				resultFile.close()
				self.gameisdone = True



class TheGame(object):

	def __init__(self, mygame):
		self.mygame = mygame
	
	def play(self):
		secretWord = self.mygame.getRandomWord(words)
		while True:
			self.mygame.oneguess(secretWord)
			if self.mygame.gameisdone:
				if self.mygame.playagain():
					secretWord = self.mygame.getRandomWord(words)
					self.mygame.missedLetters = ''
					self.mygame.correctLetters = ''
					self.mygame.gameisdone = False
				else:
					quit()

	
if __name__ == '__main__':
	try:	
		script, difficulty = argv
	except(ValueError):
		print("Please enter you name:")
		player_name = input("> ")
		time.sleep(0.5)
		while not player_name:
			if not player_name:
				print('Add proper name.')
				print("Please enter you name:")
				player_name = input("> ")
		if player_name:
			print('\n'*5)
			print("Please select your difficulty, easy or hard:")
			difficulty = input("> ")

	print('\n'*10)
	print("*"*40)
	print("*"*40)
	print("*"," "*36,"*")
	print("*"," "*36,"*")
	print('*	   H A N G M A N	       *')
	print("*"," "*36,"*")
	print("*"," "*36,"*")
	print("*"*40)
	print("*"*40)
	
	time.sleep(0.3)
	print()
	words = getworddict()
	myboard = gameboard(difficulty.lower(), words,player_name.lower())
	mygame = GameLogic(myboard)
	play = TheGame(mygame)
	play.play()
