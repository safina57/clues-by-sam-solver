import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv
from src.browser.scraper import GameScraper
from src.translator.translator import ClueTranslator
from src.solver.engine import GameSolver
# Load environment variables
load_dotenv()

async def main():
    print("Starting Clues by Sam Solver...")

    # Initialize components
    scraper = GameScraper(headless=False) 
    translator = ClueTranslator()
    
    try:
        await scraper.start()
        print("Browser started. Navigate to the game if not already there.")
        
        # Initial State
        people = await scraper.get_grid_state()
        if not people:
            print("Error: No people found. Exiting.")
            return

        solver = GameSolver(people)
        processed_clues = set()
        
        # Main Loop
        iteration = 0
        while True:
            iteration += 1
            print(f"\n--- Turn {iteration} ---")
            
            # 1. Get current state (including new clues)
            current_people = await scraper.get_grid_state()
            
            new_clues = []
            for p in current_people:
                if p.clue:
                    # Check if this specific clue from this person has been processed
                    if (p.name, p.clue) not in processed_clues:
                        new_clues.append((p.name, p.clue))
            
            if new_clues:
                print(f"Found {len(new_clues)} new clues.")
                people_names = [p.name for p in people]
                
                for name, clue_text in new_clues:
                    print(f"\nTranslating clue from {name}: \"{clue_text}\"")
                    try:
                        result = await translator.translate(clue_text, people_names, speaker=name)
                        
                        if result.is_flavor_text:
                            print("Detected flavor text. Skipping.")
                            processed_clues.add((name, clue_text))
                            continue

                        print(f"Generated Logic: {result.logic_code}")
                        print(f"Reasoning: {result.reasoning}")
                        print(f"Confidence: {result.confidence}")
                        
                        # Human verification
                        if result.confidence > 0.8:
                            print("High confidence. Adding constraint automatically.")
                            solver.add_constraint(result.logic_code)
                            processed_clues.add((name, clue_text))
                        else:
                            confirm = input("Confidence low. Add this constraint? (y/n): ")
                            if confirm.lower() == 'y':
                                solver.add_constraint(result.logic_code)
                                processed_clues.add((name, clue_text))
                    except Exception as e:
                        print(f"Translation failed: {e}")
            else:
                print("No new clues to process.")
            
            # 2. Solve
            print("Running solver...")
            actions = solver.solve()
            
            if actions:
                print(f"Found {len(actions)} proven facts!")
                for name, status in actions:
                    print(f"ACTION: Mark {name} as {status.value}")
                    
                    # Execute
                    await scraper.mark_person(name, status)
                    
                    # Check for mistake
                    if await scraper.check_for_mistake():
                        print("Mistake detected! Stopping execution.")
                        return

                    solver.add_fact(name, status)
                    
                    # Update local state
                    for p in people:
                        if p.name == name:
                            p.status = status
            else:
                print("No new deductions made.")

            # Log state
            solver.log_state(iteration)

            # Check for win
            if await scraper.check_for_win_modal() or await scraper.is_game_complete():
                print("Game Won! Saving screenshot...")
                await asyncio.sleep(5)
                os.makedirs("winning_strikes", exist_ok=True)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                await scraper.take_screenshot(f"winning_strikes/win_{timestamp}.png")
                break

            # Break after one iteration for testing and debugging
            print("\n--- End of Turn ---")
            # choice = input("Run another turn? (y/n): ")
            # if choice.lower() != 'y':
            #     break
            
            await asyncio.sleep(2)

    except KeyboardInterrupt:
        print("Stopping...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await scraper.stop()

if __name__ == "__main__":
    asyncio.run(main())
