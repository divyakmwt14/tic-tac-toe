"""
Interactive Quantum Mechanics Tutorial Overlay for Q-Tac-Toe
Provides illustrated slides explaining Superposition, Entanglement, Collapse, and Goff Rules.
"""

import pygame
from ui_theme import (
    COLOR_CRUST, COLOR_BASE, COLOR_SURFACE0, COLOR_SURFACE1,
    COLOR_TEXT, COLOR_SUBTEXT, COLOR_CYAN, COLOR_MAUVE,
    COLOR_YELLOW, COLOR_GREEN, draw_neon_rect, draw_glowing_text
)

SLIDES = [
    {
        "title": "1. Superposition (सुपरपोजिशन)",
        "badge": "QUANTUM PRINCIPLE: |ψ⟩ = 1/√2 (|A⟩ + |B⟩)",
        "badge_color": COLOR_CYAN,
        "paragraphs": [
            "Traditional Tic-Tac-Toe is deterministic and almost always ends in a dull draw.",
            "In Q-Tac-Toe, each move exists in a quantum superposition across TWO different boxes.",
            "When it is your turn, click two different empty/spooky boxes to place your quantum mark (e.g., X₁ or O₂).",
            "At this stage, the mark has a 50% probability amplitude of existing in either box."
        ],
        "tip": "Tip: You can use boxes that already hold spooky marks, but not classical (solid) marks!"
    },
    {
        "title": "2. Entanglement (एंटैंगलमेंट)",
        "badge": "QUANTUM PRINCIPLE: NON-LOCAL CORRELATION",
        "badge_color": COLOR_MAUVE,
        "paragraphs": [
            "As players continue placing marks into overlapping boxes, the moves become entangled.",
            "The boxes act as nodes and moves act as edges in a dynamic quantum graph.",
            "Glowing quantum threads connect entangled boxes on the board.",
            "The eventual state of one box is now inextricably tied to the fate of its entangled partners."
        ],
        "tip": "Tip: Watch the glowing entanglement threads to anticipate where cycles might form!"
    },
    {
        "title": "3. Wavefunction Collapse (वेवफंक्शन कोलैप्स)",
        "badge": "QUANTUM PRINCIPLE: MEASUREMENT & OBSERVATION",
        "badge_color": COLOR_YELLOW,
        "paragraphs": [
            "When a sequence of moves completes a closed circuit (cycle) in the entanglement graph, quantum uncertainty is broken!",
            "Measurement occurs: The OPPONENT of whoever closed the loop gets to choose which box the move collapses into.",
            "Once chosen, a domino-like cascade collapses every entangled mark in the cluster into a solid classical X or O state."
        ],
        "tip": "Tip: Closing a loop gives your opponent control of the collapse. Use loops strategically!"
    },
    {
        "title": "4. Winning & Allan Goff's Rule",
        "badge": "QUANTUM PRINCIPLE: TIE-BREAKER MECHANICS",
        "badge_color": COLOR_GREEN,
        "paragraphs": [
            "A player wins by aligning 3 solid classical marks in a row (horizontal, vertical, or diagonal).",
            "Quantum Tie-Breaker: Because collapses happen simultaneously, both players can achieve 3-in-a-row at the exact same instant!",
            "In this case, the player whose winning line has the lowest maximum move subscript wins (they completed their line earlier in quantum time)."
        ],
        "tip": "Ready to test your quantum strategy? Switch between 2-Player and AI mode anytime!"
    }
]

class TutorialOverlay:
    def __init__(self, screen_width=900, screen_height=700):
        self.w = screen_width
        self.h = screen_height
        self.current_slide = 0
        self.is_open = False
        
        # Dialog box dimensions
        self.dialog_w = 760
        self.dialog_h = 520
        self.dialog_x = (self.w - self.dialog_w) // 2
        self.dialog_y = (self.h - self.dialog_h) // 2

        # Button rects
        self.prev_btn = pygame.Rect(self.dialog_x + 35, self.dialog_y + self.dialog_h - 65, 120, 42)
        self.next_btn = pygame.Rect(self.dialog_x + self.dialog_w - 185, self.dialog_y + self.dialog_h - 65, 150, 42)
        self.close_btn = pygame.Rect(self.dialog_x + self.dialog_w - 48, self.dialog_y + 16, 32, 32)

    def open(self):
        self.is_open = True
        self.current_slide = 0

    def close(self):
        self.is_open = False

    def handle_event(self, event, sound_mgr=None) -> bool:
        """Returns True if the event was consumed by the tutorial overlay."""
        if not self.is_open:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.close()
                if sound_mgr:
                    sound_mgr.play('click')
                return True
            elif event.key in (pygame.K_RIGHT, pygame.K_SPACE):
                if self.current_slide < len(SLIDES) - 1:
                    self.current_slide += 1
                else:
                    self.close()
                if sound_mgr:
                    sound_mgr.play('click')
                return True
            elif event.key == pygame.K_LEFT:
                if self.current_slide > 0:
                    self.current_slide -= 1
                    if sound_mgr:
                        sound_mgr.play('click')
                return True

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            if self.close_btn.collidepoint(pos):
                self.close()
                if sound_mgr:
                    sound_mgr.play('click')
                return True
            elif self.prev_btn.collidepoint(pos) and self.current_slide > 0:
                self.current_slide -= 1
                if sound_mgr:
                    sound_mgr.play('click')
                return True
            elif self.next_btn.collidepoint(pos):
                if self.current_slide < len(SLIDES) - 1:
                    self.current_slide += 1
                else:
                    self.close()
                if sound_mgr:
                    sound_mgr.play('click')
                return True
            # Absorb clicks inside dialog so they don't click board
            dialog_rect = pygame.Rect(self.dialog_x, self.dialog_y, self.dialog_w, self.dialog_h)
            if dialog_rect.collidepoint(pos):
                return True

        return True  # Consume all events while tutorial is open

    def draw(self, surface, fonts):
        if not self.is_open:
            return

        font_title = fonts["title"]
        font_body = fonts["body"]
        font_small = fonts["small"]
        font_badge = fonts.get("badge", font_small)

        # 1. Dark semi-transparent backdrop
        backdrop = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        backdrop.fill((10, 10, 18, 220))
        surface.blit(backdrop, (0, 0))

        # 2. Main dialog card
        dialog_rect = pygame.Rect(self.dialog_x, self.dialog_y, self.dialog_w, self.dialog_h)
        pygame.draw.rect(surface, COLOR_BASE, dialog_rect, border_radius=18)
        draw_neon_rect(surface, COLOR_CYAN, dialog_rect, border_radius=18, width=2, glow_layers=3)

        slide_data = SLIDES[self.current_slide]

        # 3. Slide Title & Badge
        title_surf = font_title.render(slide_data["title"], True, COLOR_TEXT)
        surface.blit(title_surf, (self.dialog_x + 35, self.dialog_y + 26))

        # Badge
        badge_color = slide_data["badge_color"]
        badge_text = slide_data["badge"]
        b_surf = font_badge.render(badge_text, True, badge_color)
        b_rect = b_surf.get_rect(topleft=(self.dialog_x + 35, self.dialog_y + 70))
        pad_rect = b_rect.inflate(16, 8)
        pygame.draw.rect(surface, COLOR_SURFACE0, pad_rect, border_radius=6)
        pygame.draw.rect(surface, badge_color, pad_rect, 1, border_radius=6)
        surface.blit(b_surf, b_rect)

        # 4. Paragraphs
        y_cursor = self.dialog_y + 120
        for p in slide_data["paragraphs"]:
            # Word wrapping
            words = p.split(" ")
            line = ""
            for word in words:
                test_line = line + word + " "
                if font_body.size(test_line)[0] < self.dialog_w - 70:
                    line = test_line
                else:
                    p_surf = font_body.render(line, True, COLOR_TEXT)
                    surface.blit(p_surf, (self.dialog_x + 35, y_cursor))
                    y_cursor += 28
                    line = word + " "
            if line:
                p_surf = font_body.render(line, True, COLOR_TEXT)
                surface.blit(p_surf, (self.dialog_x + 35, y_cursor))
                y_cursor += 36

        # 5. Pro Tip Box
        tip_rect = pygame.Rect(self.dialog_x + 35, self.dialog_y + self.dialog_h - 135, self.dialog_w - 70, 52)
        pygame.draw.rect(surface, COLOR_SURFACE0, tip_rect, border_radius=10)
        pygame.draw.rect(surface, COLOR_YELLOW, tip_rect, 1, border_radius=10)
        tip_surf = font_small.render(slide_data["tip"], True, COLOR_YELLOW)
        surface.blit(tip_surf, (tip_rect.x + 16, tip_rect.y + 16))

        # 6. Pagination Dots
        for idx in range(len(SLIDES)):
            dot_x = self.dialog_x + self.dialog_w // 2 + (idx - 1.5) * 22
            dot_y = self.dialog_y + self.dialog_h - 44
            color = COLOR_CYAN if idx == self.current_slide else COLOR_SURFACE1
            radius = 6 if idx == self.current_slide else 4
            pygame.draw.circle(surface, color, (int(dot_x), int(dot_y)), radius)

        # 7. Navigation Buttons
        mouse_pos = pygame.mouse.get_pos()

        # Prev Button
        if self.current_slide > 0:
            hover = self.prev_btn.collidepoint(mouse_pos)
            bg_col = COLOR_SURFACE1 if hover else COLOR_SURFACE0
            pygame.draw.rect(surface, bg_col, self.prev_btn, border_radius=8)
            pygame.draw.rect(surface, COLOR_TEXT, self.prev_btn, 1, border_radius=8)
            prev_txt = font_body.render("← Previous", True, COLOR_TEXT)
            surface.blit(prev_txt, prev_txt.get_rect(center=self.prev_btn.center))

        # Next / Finish Button
        hover_next = self.next_btn.collidepoint(mouse_pos)
        is_last = (self.current_slide == len(SLIDES) - 1)
        next_color = COLOR_GREEN if is_last else COLOR_CYAN
        bg_col = (*next_color, 40) if hover_next else COLOR_SURFACE0
        pygame.draw.rect(surface, COLOR_SURFACE0, self.next_btn, border_radius=8)
        draw_neon_rect(surface, next_color, self.next_btn, border_radius=8, width=2, glow_layers=2)
        label = "Start Game ⚡" if is_last else "Next →"
        next_txt = font_body.render(label, True, next_color)
        surface.blit(next_txt, next_txt.get_rect(center=self.next_btn.center))

        # Close 'X' Button
        close_hover = self.close_btn.collidepoint(mouse_pos)
        close_col = COLOR_RED if close_hover else COLOR_SUBTEXT
        pygame.draw.circle(surface, COLOR_SURFACE0, self.close_btn.center, 16)
        pygame.draw.circle(surface, close_col, self.close_btn.center, 16, 1)
        x_surf = font_body.render("✕", True, close_col)
        surface.blit(x_surf, x_surf.get_rect(center=self.close_btn.center))
