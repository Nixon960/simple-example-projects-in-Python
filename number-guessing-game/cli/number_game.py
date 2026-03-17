import random
import time
import sys
import logging

# ====================== LOGGING SETUP (Best Practice) ======================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("number_guessing_game.log", mode='a'),  # Append to log file
        logging.StreamHandler(sys.stdout)  # Also show in console
    ]
)
logger = logging.getLogger(__name__)

class NumberGuessingGame:
   
    def __init__(self):
        self.difficulty_levels = {
            'easy': {'range': (1, 50), 'attempts': 10},
            'medium': {'range': (1, 100), 'attempts': 7},
            'hard': {'range': (1, 200), 'attempts': 5},
            'expert': {'range': (1, 500), 'attempts': 8}
        }
       
        self.game_stats = {
            'games_played': 0,
            'games_won': 0,
            'total_attempts': 0,
            'best_score': float('inf')
        }
   
    def print_banner(self):
        print("=" * 60)
        print("🎮 NUMBER GUESSING GAME 🎮")
        print("=" * 60)
        print("Try to guess the secret number!")
        print("You'll get hints to help you find it.")
        print("=" * 60)
        logger.info("Game banner displayed")
   
    # ... (keep display_difficulty_menu, get_difficulty_choice, get_hint, show_instructions exactly as you had them) ...

    def play_round(self, difficulty):
        config = self.difficulty_levels[difficulty]
        min_num, max_num = config['range']
        max_attempts = config['attempts']
       
        secret_number = random.randint(min_num, max_num)
        attempts_used = 0
        start_time = time.time()
       
        logger.info(f"New game started - Difficulty: {difficulty.upper()}, Range: {min_num}-{max_num}, Secret: {secret_number} (hidden from user)")
       
        print(f"\n🎲 New Game Started!")
        print(f"Difficulty: {difficulty.upper()}")
        print(f"Range: {min_num} - {max_num}")
        print(f"Maximum attempts: {max_attempts}")
        print(f"Secret number generated... Good luck! 🍀")
        print("-" * 50)
       
        while attempts_used < max_attempts:
            attempts_left = max_attempts - attempts_used
           
            try:
                print(f"\nAttempt {attempts_used + 1}/{max_attempts} (📍 {attempts_left} left)")
                guess_input = input(f"Enter your guess ({min_num}-{max_num}): ").strip()
                
                if not guess_input:
                    raise ValueError("Empty input")
                    
                guess = int(guess_input)
               
                if guess < min_num or guess > max_num:
                    print(f"⚠️ Number must be between {min_num} and {max_num}!")
                    logger.warning(f"Out of range guess: {guess} (expected {min_num}-{max_num})")
                    continue
               
                attempts_used += 1
                logger.info(f"Guess {attempts_used}: {guess} (Difficulty: {difficulty})")
               
                if guess == secret_number:
                    elapsed_time = round(time.time() - start_time, 1)
                    self.handle_win(attempts_used, max_attempts, elapsed_time, secret_number)
                    return True
               
                elif guess < secret_number:
                    hint = self.get_hint(guess, secret_number, min_num, max_num)
                    print(f"📈 Too low! {hint}")
                else:
                    hint = self.get_hint(guess, secret_number, min_num, max_num)
                    print(f"📉 Too high! {hint}")
               
                # Additional hints
                difference = abs(guess - secret_number)
                if difference <= 5:
                    print("🔥 You're very close!")
                elif difference <= 15:
                    print("🌡️ Getting warmer...")
                elif difference <= 30:
                    print("❄️ Getting colder...")
               
            except ValueError as e:
                print("❌ Please enter a valid number!")
                logger.error(f"ValueError on input: {e} | Difficulty: {difficulty}")
            except KeyboardInterrupt:
                print("\n\n👋 Game interrupted. Goodbye!")
                logger.info("Game interrupted by user (KeyboardInterrupt)")
                return False
            except Exception as e:  # Only as last resort now
                logger.exception(f"Unexpected error in play_round (Difficulty: {difficulty})")
                print("❌ An unexpected error occurred. Check the log for details.")
                return False
       
        # Player lost
        self.handle_loss(secret_number, difficulty)
        return False
   
    def handle_win(self, attempts, max_attempts, time_taken, secret_number):
        self.game_stats['games_played'] += 1
        self.game_stats['games_won'] += 1
        self.game_stats['total_attempts'] += attempts
       
        if attempts < self.game_stats['best_score']:
            self.game_stats['best_score'] = attempts
       
        logger.info(f"WIN! Secret: {secret_number}, Attempts: {attempts}, Time: {time_taken}s, Difficulty: unknown")  # You can pass difficulty if needed
        
        # (keep your original beautiful win print statements)
        print("\n" + "🎉" * 20)
        print("🏆 CONGRATULATIONS! YOU WON! 🏆")
        print("🎉" * 20)
        print(f"✅ You found the number in {attempts} attempts!")
        print(f"⏱️ Time taken: {time_taken} seconds")
        # ... rest of your performance rating ...
   
    def handle_loss(self, secret_number, difficulty):
        self.game_stats['games_played'] += 1
        logger.info(f"LOSS - Secret was {secret_number} | Difficulty: {difficulty}")
        
        # (keep your original loss print statements)
        print("\n" + "💀" * 20)
        print("😞 GAME OVER!")
        print("💀" * 20)
        print(f"The secret number was: {secret_number}")
        print("Better luck next time! 💪")
   
    # Keep show_statistics, main_menu, show_instructions, run exactly as before 
    # (but in run(), you can make the broad except log with logger.exception)

    def run(self):
        try:
            self.print_banner()
            self.main_menu()
        except KeyboardInterrupt:
            print("\n\n👋 Game interrupted. Goodbye!")
            logger.info("Game exited via KeyboardInterrupt in run()")
        except Exception as e:
            logger.exception("Critical unexpected error in game run()")
            print(f"\n❌ A critical error occurred: {e}")
            print("Please check number_guessing_game.log for details.")

# ====================== MAIN ======================
def main():
    logger.info("=== Number Guessing Game Started ===")
    game = NumberGuessingGame()
    game.run()
    logger.info("=== Game Session Ended ===")

if __name__ == "__main__":
    main()
