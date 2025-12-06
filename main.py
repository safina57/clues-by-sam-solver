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

    # Clear log file
    with open("solver_log.txt", "w") as f:
        f.write(f"Solver Log - Run started at {datetime.now()}\n")

    # Clear translation log file
    with open("translation_log.txt", "w") as f:
        f.write(f"Translation Log - Run started at {datetime.now()}\n")

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
                people_names = [p.name for p in people]

                for name, clue_text in new_clues:
                    try:
                        result = await translator.translate(
                            clue_text, people_names, speaker=name
                        )

                        # Log translation
                        with open("translation_log.txt", "a") as f:
                            f.write(f"\n--- Clue from {name} ---\n")
                            f.write(f"Text: {clue_text}\n")
                            f.write(f"Code: {result.logic_code}\n")
                            f.write(f"Confidence: {result.confidence}\n")
                            f.write(f"Reasoning: {result.reasoning}\n")
                            f.write(f"Is Flavor: {result.is_flavor_text}\n")
                            f.write("-" * 30 + "\n")

                        if result.is_flavor_text:
                            processed_clues.add((name, clue_text))
                            continue

                        # Human verification
                        if result.confidence > 0.8:
                            solver.add_constraint(result.logic_code)
                            processed_clues.add((name, clue_text))
                        else:
                            confirm = input(
                                "Confidence low. Add this constraint? (y/n): "
                            )
                            if confirm.lower() == "y":
                                solver.add_constraint(result.logic_code)
                                processed_clues.add((name, clue_text))
                    except Exception as e:
                        print(f"Translation failed: {e}")
            else:
                pass

            # 2. Solve
            actions = solver.solve()

            if actions:
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
                pass

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
