from typing import List, Optional
from playwright.async_api import async_playwright, Page, Browser
from src.models.game_state import Person, Status


class GameScraper:
    def __init__(self, headless: bool = False):
        self.headless = headless
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.url = "https://cluesbysam.com"

    async def start(self):
        """Launch the browser and navigate to the game."""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        self.page = await self.browser.new_page()
        await self.page.goto(self.url)

        # Handle Start Modal
        try:
            start_btn = self.page.locator("button.btn.start")
            if await start_btn.is_visible(timeout=5000):
                await start_btn.click()
                await self.page.wait_for_selector(".modal-overlay", state="hidden")
        except Exception:
            pass

        # Wait for grid to load
        try:
            await self.page.wait_for_selector("#grid", timeout=15000)
        except Exception:
            pass

    async def stop(self):
        """Close the browser."""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    async def get_grid_state(self) -> List[Person]:
        """Scrape the current state of all 20 people."""
        people = []

        # Iterate through all card containers in the grid
        cards = self.page.locator(".card-container .card")
        count = await cards.count()

        if count == 0:
            return []

        for i in range(count):
            card = cards.nth(i)

            # Extract ID (Coordinate)
            coord_el = card.locator(".coord")
            coord = await coord_el.text_content()
            coord = coord.strip()

            # Extract Name
            name_el = card.locator("h3.name")
            name = await name_el.text_content()
            name = name.strip().title()

            # Extract Profession
            prof_el = card.locator(".profession")
            profession_str = await prof_el.text_content()
            profession = self._extract_profession(profession_str)

            # Extract Status & Clue
            # Check classes on the card div
            classes = await card.get_attribute("class")
            status = Status.UNKNOWN
            clue_text = None

            if "innocent" in classes:
                status = Status.INNOCENT
            elif "criminal" in classes:
                status = Status.CRIMINAL

            # Check for clue on the back if the card is flipped/revealed
            if status != Status.UNKNOWN:
                clue_el = card.locator(".hint")
                if await clue_el.count() > 0:
                    clue_text = await clue_el.text_content()

            # Parse Row/Col from Coord
            col = coord[0]
            row = int(coord[1])

            person = Person(
                id=coord,
                name=name,
                profession=profession,
                row=row,
                col=col,
                status=status,
                clue=clue_text,
            )
            people.append(person)

        # Calculate neighbors for each person
        for p in people:
            p.neighbors = []
            for other in people:
                if p.name == other.name:
                    continue

                row_diff = abs(p.row - other.row)
                col_p = ord(p.col) - ord("A")
                col_o = ord(other.col) - ord("A")
                col_diff = abs(col_p - col_o)

                if row_diff <= 1 and col_diff <= 1:
                    p.neighbors.append(other.name)

        return people

    async def get_visible_clues(self) -> List[str]:
        """Extract text of all currently visible clues."""
        clues = []

        # Clues on any card (Innocent or Criminal) that has a hint
        cards = self.page.locator(".card .hint")
        count = await cards.count()
        for i in range(count):
            text = await cards.nth(i).text_content()
            if text:
                clues.append(text.strip())

        return clues

    async def mark_person(self, name: str, status: Status):
        """Click a person and set their status."""
        if status == Status.UNKNOWN:
            return

        # 1. Click the card to open modal
        name_lower = name.lower()

        # Locator for the card containing the name
        card_loc = self.page.locator(
            f".card:has(h3.name:text-is('{name_lower}'))"
        ).first

        if await card_loc.count() == 0:
            # Fallback: try case-insensitive text match
            card_loc = self.page.locator(f".card:has(h3.name:text('{name}'))").first

        await card_loc.scroll_into_view_if_needed()
        await card_loc.click()

        # 2. Wait for modal
        modal = self.page.locator(".modal-overlay .modal")
        await modal.wait_for(state="visible")

        # 3. Click "Innocent" or "Criminal" button
        if status == Status.INNOCENT:
            btn = modal.locator("button.btn-innocent")
        else:
            btn = modal.locator("button.btn-criminal")

        if await btn.is_visible():
            await btn.click()
            # Wait for modal to close
            await modal.wait_for(state="hidden")
        else:
            # Close modal to recover
            close_btn = modal.locator("button.btn-close")
            if await close_btn.is_visible():
                await close_btn.click()

    async def check_for_mistake(self) -> bool:
        """Check if the 'Not enough evidence' modal is visible."""
        try:
            # Short timeout because we expect it to appear immediately if at all
            modal = self.page.locator(".modal-overlay .modal.warning")
            if await modal.is_visible(timeout=2000):
                # Click Continue to dismiss
                btn = modal.locator("button.btn-warn")
                if await btn.is_visible():
                    await btn.click()
                    await modal.wait_for(state="hidden")
                return True
        except Exception:
            pass
        return False

    async def check_for_win_modal(self) -> bool:
        """Check if the 'Game Won' modal is visible."""
        try:
            modal = self.page.locator(".modal-overlay .modal.complete")
            if await modal.is_visible(timeout=2000):
                return True
        except Exception:
            pass
        return False

    async def is_game_complete(self) -> bool:
        """Check if all 20 cards have been solved (no longer unknown)."""
        try:
            solved_count = await self.page.locator(
                ".card.innocent, .card.criminal"
            ).count()
            return solved_count == 20
        except Exception:
            return False

    async def take_screenshot(self, path: str):
        """Take a screenshot of the current page."""
        if self.page:
            await self.page.screenshot(path=path, full_page=True)

    def _extract_profession(self, text: str) -> str:
        return text.lower().strip()
