import random
import string
'''
Number Guessing Game - two players A & B

Here’s how it works:

One player (A) picks a secret number and let the other player (B) to guess.  

Player B has 20 attempts to guess.  The game ends when either a correct guess is made 
or the number of attempts reaches 20.

The secret number is a 4-digit number, with no repeated digits, leading zero is fine.  

For examples: 1345, 0913 and 3491 are valid numbers, while 0232 is not.

As each guess is made, player B will receive two additional pieces of information: 
    correct count and misplaced count.

Correct count is the number of digits that appear both in the guess and in the secret number 
AND in the same location.

Misplaced count is the number of digits that appear both in the guess and in the secret number 
BUT in different locations.

Examples: secret-number=1357, guess=9371

correct count=1 (digit 3), misplaced count=2 (digits 1 and 7)
'''
def pick_a_number(length: int) -> str:
    return '1234'

def get_correct_cnt(secret:str, guess:str) -> int:
    return 0

def get_misplaced_cnt(secret:str, guess:str) -> int:
    return 0

def prompt_guess(length:int) -> str:
    guess = input('Enter your guess >')
    # validate input
    return guess

def display_hints(secret, guess, attempt) -> None:
    correct = get_correct_cnt(secret, guess)
    misplaced = get_misplaced_cnt(secret, guess)
    print(f"Attempt-{attempt} Correct-{correct} Misplaced-{misplaced}")

def play(secret, max_attempt):
    attempt = 0
    while attempt < max_attempt:
        guess = prompt_guess(len(secret))
        if guess == secret:
            print('Winner!')
            return
        display_hints(secret, guess, attempt)
        attempt += 1
    print('Game Over!!')
        
def main():
    length = 4
    max_attempt = 20
    secret = pick_a_number(length)
    print(f'secret number is {secret}')
    play(secret, max_attempt)

def test():
    print(pick_a_number(10))
    print(get_correct_cnt('1234', '1243'))
    print(get_correct_cnt('2134', '1243'))
    print(get_misplaced_cnt('2134', '1243'))

main()

