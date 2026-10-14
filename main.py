"""
Q-Tac-Toe: Bridging Quantum Mechanics and Gaming
=================================================
A Modern Quantum Tic-Tac-Toe Game with:
- Quantum Superposition (moves exist in 2 squares at once)
- Entanglement Graphs & Real-time Cycle Detection
- Wavefunction Collapse with Domino Cascade Propagation
- Single-Player vs AI Mode (Probabilistic & Minimax Decision Making)
- Procedural Sci-Fi Sound Effects (via NumPy & Pygame Mixer)
- Catppuccin Neon Theme & Dynamic Quantum Visuals
- Interactive Tutorial Explaining Quantum Mechanics Principles
"""

import sys
import time
import math
import pygame
from typing import Optional, Tuple

from quantum_board import QuantumBoard, QuantumMove, WINNING_LINES
from quantum_ai import QuantumAI
from sound_effects import SoundManager
from ui_theme import (
    COLOR_CRUST, COLOR_MANTLE, COLOR_BASE, COLOR_SURFACE0,
    COLOR_SURFACE1, COLOR_SURFACE2, COLOR_TEXT, COLOR_SUBTEXT,
    COLOR_CYAN, COLOR_MAUVE, COLOR_RED, COLOR_GREEN,
    COLOR_YELLOW, COLOR_LAVENDER, Starfield, draw_neon_rect,
    draw_neon_circle, draw_neon_line, draw_glowing_text
)
from tutorial import TutorialOverlay


class QTacGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Q-Tac-Toe: Quantum Mechanics & Gaming")
        
        self.width = 1040
        self.height = 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        # Audio manager
        self.sounds = SoundManager()

        # Fonts
        self.fonts = self._load_fonts()

        # Game engine & AI
        self.board = QuantumBoard()
        self.vs_ai = True
        self.ai_player = 'O'
        self.ai_difficulty = 'hard'  # 'normal' or 'hard'
        self.ai = QuantumAI(ai_player=self.ai_player, difficulty=self.ai_difficulty)

        # UI state
        self.selected_sq1: Optional[int] = None
        self.starfield = Starfield(self.width, self.height, count=60)
        self.tutorial = TutorialOverlay(self.width, self.height)

        # Timers for smooth AI pacing
        self.ai_move_timer: Optional[float] = None
        self.ai_collapse_timer: Optional[float] = None

        # Layout geometry
        self.board_rect = pygame.Rect(40, 110, 480, 480)
        self.cell_size = self.board_rect.width // 3
        self.side_panel_rect = pygame.Rect(560, 110, 440, 570)

        # Header Buttons
        self.btn_tutorial = pygame.Rect(560, 40, 95, 36)
        self.btn_mode = pygame.Rect(665, 40, 115, 36)
        self.btn_diff = pygame.Rect(790, 40, 110, 36)
        self.btn_sound = pygame.Rect(910, 40, 90, 36)
        self.btn_reset = pygame.Rect(40, 610, 480, 45)

        # Collapse choice buttons (placed dynamically in side panel)
        self.btn_collapse_a = pygame.Rect(580, 320, 180, 50)
        self.btn_collapse_b = pygame.Rect(790, 320, 180, 50)

    def _load_fonts(self):
        font_names = ["segoeui", "helvetica", "arial", "sans-serif"]
        def get_sys_font(size, bold=False):
            for name in font_names:
                try:
                    f = pygame.font.SysFont(name, size, bold=bold)
                    if f: return f
                except Exception:
                    pass
            return pygame.font.Font(None, size)

        return {
            "title_large": get_sys_font(34, bold=True),
            "title": get_sys_font(26, bold=True),
            "subtitle": get_sys_font(18, bold=False),
            "body": get_sys_font(17, bold=False),
            "body_bold": get_sys_font(17, bold=True),
            "small": get_sys_font(14, bold=False),
            "badge": get_sys_font(12, bold=True),
            "symbol_large": get_sys_font(72, bold=True),
            "spooky": get_sys_font(18, bold=True)
        }

    def reset_game(self):
        self.board = QuantumBoard()
        self.selected_sq1 = None
        self.ai_move_timer = None
        self.ai_collapse_timer = None
        self.sounds.play('click')

    def get_cell_rect(self, sq: int) -> pygame.Rect:
        col = sq % 3
        row = sq // 3
        x = self.board_rect.x + col * self.cell_size
        y = self.board_rect.y + row * self.cell_size
        return pygame.Rect(x, y, self.cell_size, self.cell_size)

    def get_cell_center(self, sq: int) -> Tuple[int, int]:
        rect = self.get_cell_rect(sq)
        return rect.center

    def handle_cell_click(self, sq: int):
        if self.board.game_over or self.board.pending_collapse is not None:
            return
        if self.vs_ai and self.board.current_player == self.ai_player:
            return  # Human cannot click during AI turn

        if self.board.classical[sq] is not None:
            # Cannot click already collapsed classical cell
            return

        if self.selected_sq1 is None:
            # First square chosen
            self.selected_sq1 = sq
            self.sounds.play('click')
        elif self.selected_sq1 == sq:
            # Deselect if clicked same square
            self.selected_sq1 = None
            self.sounds.play('click')
        else:
            # Second square chosen -> execute quantum move
            sq1, sq2 = self.selected_sq1, sq
            self.selected_sq1 = None
            result = self.board.make_quantum_move(sq1, sq2)

            if result["status"] == "cycle_detected":
                self.sounds.play('loop')
            elif result["status"] == "success":
                self.sounds.play('move')

    def update_ai(self):
        """Manages AI move execution and collapse choices."""
        if self.board.game_over:
            return

        current_time = time.time()

        # 1. AI Pending Collapse Resolution
        if self.board.pending_collapse is not None:
            resolving_player = self.board.pending_collapse["resolving_player"]
            if self.vs_ai and resolving_player == self.ai_player:
                if self.ai_collapse_timer is None:
                    self.ai_collapse_timer = current_time + 0.8  # 800ms think time
                elif current_time >= self.ai_collapse_timer:
                    choice = self.ai.choose_collapse(self.board)
                    res = self.board.resolve_collapse(choice)
                    self.ai_collapse_timer = None
                    if res["win_result"]["winner"]:
                        self.sounds.play('win')
                    else:
                        self.sounds.play('collapse')
            return

        # 2. AI Turn to make a Quantum Move
        if self.vs_ai and self.board.current_player == self.ai_player:
            if self.ai_move_timer is None:
                self.ai_move_timer = current_time + 0.7  # 700ms think time
            elif current_time >= self.ai_move_timer:
                sq1, sq2 = self.ai.choose_quantum_move(self.board)
                res = self.board.make_quantum_move(sq1, sq2)
                self.ai_move_timer = None
                if res["status"] == "cycle_detected":
                    self.sounds.play('loop')
                elif res["status"] == "success":
                    self.sounds.play('move')

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000.0

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

                # If tutorial is open, it intercepts input
                if self.tutorial.handle_event(event, self.sounds):
                    continue

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = event.pos

                    # Header Buttons
                    if self.btn_tutorial.collidepoint(pos):
                        self.sounds.play('click')
                        self.tutorial.open()
                    elif self.btn_sound.collidepoint(pos):
                        self.sounds.toggle_mute()
                    elif self.btn_mode.collidepoint(pos):
                        self.sounds.play('click')
                        self.vs_ai = not self.vs_ai
                        self.reset_game()
                    elif self.btn_diff.collidepoint(pos):
                        self.sounds.play('click')
                        self.ai_difficulty = 'normal' if self.ai_difficulty == 'hard' else 'hard'
                        self.ai = QuantumAI(ai_player=self.ai_player, difficulty=self.ai_difficulty)
                    elif self.btn_reset.collidepoint(pos):
                        self.reset_game()

                    # Collapse Choice Buttons (When Human must resolve)
                    elif self.board.pending_collapse is not None:
                        res_player = self.board.pending_collapse["resolving_player"]
                        if not self.vs_ai or res_player != self.ai_player:
                            opts = self.board.pending_collapse["options"]
                            if self.btn_collapse_a.collidepoint(pos):
                                res = self.board.resolve_collapse(opts[0])
                                if res["win_result"]["winner"]:
                                    self.sounds.play('win')
                                else:
                                    self.sounds.play('collapse')
                            elif self.btn_collapse_b.collidepoint(pos):
                                res = self.board.resolve_collapse(opts[1])
                                if res["win_result"]["winner"]:
                                    self.sounds.play('win')
                                else:
                                    self.sounds.play('collapse')

                    # Board Cell Clicks
                    elif self.board_rect.collidepoint(pos):
                        col = (pos[0] - self.board_rect.x) // self.cell_size
                        row = (pos[1] - self.board_rect.y) // self.cell_size
                        if 0 <= col < 3 and 0 <= row < 3:
                            sq = row * 3 + col
                            self.handle_cell_click(sq)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()
                    elif event.key == pygame.K_m:
                        self.sounds.toggle_mute()
                    elif event.key in (pygame.K_t, pygame.K_SLASH, pygame.K_QUESTION):
                        self.sounds.play('click')
                        self.tutorial.open()
                    elif event.key == pygame.K_a:
                        self.sounds.play('click')
                        self.vs_ai = not self.vs_ai
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.selected_sq1 = None

            # AI logic update
            self.update_ai()

            # Drawing
            self.draw()
            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def draw(self):
        # 1. Background
        self.screen.fill(COLOR_CRUST)
        self.starfield.update_and_draw(self.screen)

        # 2. Header
        self.draw_header()

        # 3. Board & Cells
        self.draw_board()

        # 4. Entanglement Lines / Graph
        self.draw_entanglement_links()

        # 5. Side Panel (State, Quantum Diagnostics, Collapse, Controls)
        self.draw_side_panel()

        # 6. Tutorial Overlay (if active)
        self.tutorial.draw(self.screen, self.fonts)

    def draw_header(self):
        # Title
        title_surf = self.fonts["title_large"].render("Q-TAC-TOE", True, COLOR_CYAN)
        self.screen.blit(title_surf, (40, 30))

        sub_surf = self.fonts["small"].render("QUANTUM TIC-TAC-TOE • SUPERPOSITION & ENTANGLEMENT", True, COLOR_SUBTEXT)
        self.screen.blit(sub_surf, (42, 68))

        mouse_pos = pygame.mouse.get_pos()

        # Header Buttons Helper
        def draw_hdr_btn(rect, text, active_color=COLOR_CYAN, border_col=COLOR_SURFACE1):
            hover = rect.collidepoint(mouse_pos)
            bg = COLOR_SURFACE1 if hover else COLOR_SURFACE0
            pygame.draw.rect(self.screen, bg, rect, border_radius=8)
            pygame.draw.rect(self.screen, border_col, rect, 1, border_radius=8)
            txt_surf = self.fonts["small"].render(text, True, active_color if hover else COLOR_TEXT)
            self.screen.blit(txt_surf, txt_surf.get_rect(center=rect.center))

        # Tutorial Button
        draw_hdr_btn(self.btn_tutorial, "📖 Guide (?)", COLOR_YELLOW)

        # Mode Button
        mode_text = "🤖 vs AI" if self.vs_ai else "👥 2-Player"
        draw_hdr_btn(self.btn_mode, mode_text, COLOR_MAUVE)

        # Difficulty Button (only relevant in AI mode)
        diff_text = f"AI: {self.ai_difficulty.capitalize()}"
        draw_hdr_btn(self.btn_diff, diff_text, COLOR_GREEN if self.ai_difficulty == 'hard' else COLOR_YELLOW)

        # Sound Button
        snd_text = "🔇 Mute" if self.sounds.muted else "🔊 Sound"
        draw_hdr_btn(self.btn_sound, snd_text, COLOR_CYAN)

    def draw_board(self):
        # Board background card
        board_card = self.board_rect.inflate(16, 16)
        pygame.draw.rect(self.screen, COLOR_BASE, board_card, border_radius=16)
        draw_neon_rect(self.screen, COLOR_SURFACE1, board_card, border_radius=16, width=2, glow_layers=2)

        mouse_pos = pygame.mouse.get_pos()

        # Draw Cells
        for sq in range(9):
            rect = self.get_cell_rect(sq)
            inner_rect = rect.inflate(-8, -8)
            is_hovered = inner_rect.collidepoint(mouse_pos)
            is_classical = self.board.classical[sq] is not None
            is_selected = (self.selected_sq1 == sq)

            # Cell background color
            if is_classical:
                bg_col = COLOR_MANTLE
            elif is_selected:
                bg_col = COLOR_SURFACE1
            elif is_hovered and self.board.pending_collapse is None and not self.board.game_over:
                bg_col = COLOR_SURFACE0
            else:
                bg_col = COLOR_BASE

            pygame.draw.rect(self.screen, bg_col, inner_rect, border_radius=10)

            # Neon highlight if cell is selected for superposition
            if is_selected:
                pulse = (math.sin(time.time() * 8) + 1) * 0.5
                p_col = COLOR_CYAN if self.board.current_player == 'X' else COLOR_MAUVE
                draw_neon_rect(self.screen, p_col, inner_rect, border_radius=10, width=2, glow_layers=3)

            # Square index label in corner (1-9)
            idx_surf = self.fonts["badge"].render(str(sq + 1), True, COLOR_SURFACE2)
            self.screen.blit(idx_surf, (inner_rect.x + 8, inner_rect.y + 6))

            # Render Classical Mark OR Spooky Marks
            if is_classical:
                move = self.board.classical[sq]
                mark_color = COLOR_CYAN if move.player == 'X' else COLOR_MAUVE
                
                # Check if this cell is part of the winning line
                if self.board.winning_line and sq in self.board.winning_line:
                    draw_neon_rect(self.screen, COLOR_GREEN, inner_rect, border_radius=10, width=3, glow_layers=4)
                    mark_color = COLOR_GREEN

                # Large Bold Classical Symbol
                draw_glowing_text(self.screen, move.player, self.fonts["symbol_large"], mark_color, inner_rect.center)
                # Subscript move number at bottom right
                sub_txt = self.fonts["small"].render(f"m{move.move_id}", True, COLOR_SUBTEXT)
                self.screen.blit(sub_txt, (inner_rect.right - 26, inner_rect.bottom - 22))

            else:
                # Render uncollapsed spooky marks in superposition
                spooky_moves = self.board.get_spooky_marks_in_square(sq)
                if spooky_moves:
                    self.draw_spooky_marks(inner_rect, spooky_moves)

        # Grid lines with subtle glow
        for i in range(1, 3):
            # Vertical
            x = self.board_rect.x + i * self.cell_size
            draw_neon_line(self.screen, COLOR_SURFACE1, (x, self.board_rect.y), (x, self.board_rect.bottom), width=2, glow_layers=1)
            # Horizontal
            y = self.board_rect.y + i * self.cell_size
            draw_neon_line(self.screen, COLOR_SURFACE1, (self.board_rect.x, y), (self.board_rect.right, y), width=2, glow_layers=1)

        # Reset button below board
        hover_reset = self.btn_reset.collidepoint(mouse_pos)
        pygame.draw.rect(self.screen, COLOR_SURFACE1 if hover_reset else COLOR_SURFACE0, self.btn_reset, border_radius=10)
        draw_neon_rect(self.screen, COLOR_RED if hover_reset else COLOR_SURFACE2, self.btn_reset, border_radius=10, width=1, glow_layers=1)
        rst_txt = self.fonts["body_bold"].render("↻ New Game (R)", True, COLOR_TEXT)
        self.screen.blit(rst_txt, rst_txt.get_rect(center=self.btn_reset.center))

    def draw_spooky_marks(self, inner_rect: pygame.Rect, spooky_moves: list):
        """Draws small quantum marks in superposition neatly inside the square."""
        total = len(spooky_moves)
        cols = 3 if total > 4 else 2
        
        start_x = inner_rect.x + 14
        start_y = inner_rect.y + 24
        slot_w = (inner_rect.width - 28) // cols
        slot_h = 24

        for idx, move in enumerate(spooky_moves):
            col = idx % cols
            row = idx // cols
            cx = start_x + col * slot_w + slot_w // 2
            cy = start_y + row * slot_h + slot_h // 2

            m_col = COLOR_CYAN if move.player == 'X' else COLOR_MAUVE
            
            # Draw badge background
            badge_rect = pygame.Rect(cx - 16, cy - 10, 32, 20)
            pygame.draw.rect(self.screen, COLOR_MANTLE, badge_rect, border_radius=5)
            pygame.draw.rect(self.screen, m_col, badge_rect, 1, border_radius=5)

            # Spooky text
            spooky_surf = self.fonts["spooky"].render(move.label(), True, m_col)
            self.screen.blit(spooky_surf, spooky_surf.get_rect(center=badge_rect.center))

    def draw_entanglement_links(self):
        """Draws glowing quantum entanglement threads between entangled squares."""
        adj = self.board.get_entanglement_graph()
        drawn_edges = set()

        is_cycle_active = self.board.pending_collapse is not None
        cycle_moves = self.board.pending_collapse.get("cycle_moves", []) if is_cycle_active else []
        cycle_move_ids = set(m.move_id for m in cycle_moves)

        for u in adj:
            for v, move in adj[u]:
                edge_key = tuple(sorted((u, v))) + (move.move_id,)
                if edge_key in drawn_edges:
                    continue
                drawn_edges.add(edge_key)

                c1 = self.get_cell_center(u)
                c2 = self.get_cell_center(v)

                if move.move_id in cycle_move_ids:
                    # Urgent pulsing RED for the loop triggering collapse
                    pulse = (math.sin(time.time() * 10) + 1) * 0.5
                    color = COLOR_RED
                    draw_neon_line(self.screen, color, c1, c2, width=4, glow_layers=4)
                else:
                    # Gentle lavender / cyan quantum entanglement thread
                    color = COLOR_LAVENDER
                    draw_neon_line(self.screen, color, c1, c2, width=2, glow_layers=2)

    def draw_side_panel(self):
        """Draws real-time quantum telemetry, turn indicator, collapse options, and educational log."""
        # Panel container card
        pygame.draw.rect(self.screen, COLOR_BASE, self.side_panel_rect, border_radius=16)
        draw_neon_rect(self.screen, COLOR_SURFACE1, self.side_panel_rect, border_radius=16, width=2, glow_layers=2)

        px = self.side_panel_rect.x + 22
        py = self.side_panel_rect.y + 20

        # 1. Status & Turn Header
        if self.board.game_over:
            self.draw_game_over_banner(px, py)
        elif self.board.pending_collapse is not None:
            self.draw_collapse_panel(px, py)
        else:
            self.draw_turn_status(px, py)

        # 2. Real-Time Educational Physics Feed
        edu_rect = pygame.Rect(px, self.side_panel_rect.y + 360, self.side_panel_rect.width - 44, 185)
        pygame.draw.rect(self.screen, COLOR_SURFACE0, edu_rect, border_radius=12)
        pygame.draw.rect(self.screen, COLOR_SURFACE1, edu_rect, 1, border_radius=12)

        edu_title = self.fonts["body_bold"].render("⚛ QUANTUM PRINCIPLE IN ACTION", True, COLOR_YELLOW)
        self.screen.blit(edu_title, (edu_rect.x + 16, edu_rect.y + 14))

        # Render description with word wrap
        log_text = self.board.last_quantum_event
        words = log_text.split(" ")
        line = ""
        y_text = edu_rect.y + 44
        for w in words:
            test = line + w + " "
            if self.fonts["small"].size(test)[0] < edu_rect.width - 32:
                line = test
            else:
                s = self.fonts["small"].render(line, True, COLOR_TEXT)
                self.screen.blit(s, (edu_rect.x + 16, y_text))
                y_text += 22
                line = w + " "
        if line:
            s = self.fonts["small"].render(line, True, COLOR_TEXT)
            self.screen.blit(s, (edu_rect.x + 16, y_text))

        # Extra quantum state telemetry at bottom of box
        qubit_count = len([m for m in self.board.moves if not m.collapsed])
        classical_count = len([sq for sq, m in self.board.classical.items() if m is not None])
        telemetry = f"Entangled Spooky Pairs: {qubit_count}  |  Classical Observed: {classical_count}/9"
        t_surf = self.fonts["badge"].render(telemetry, True, COLOR_SUBTEXT)
        self.screen.blit(t_surf, (edu_rect.x + 16, edu_rect.bottom - 24))

    def draw_turn_status(self, px, py):
        curr_p = self.board.current_player
        p_color = COLOR_CYAN if curr_p == 'X' else COLOR_MAUVE

        # Status Badge
        is_ai_turn = (self.vs_ai and curr_p == self.ai_player)
        who_label = "AI (Quantum Bot)" if is_ai_turn else ("Player X" if curr_p == 'X' else "Player O")

        lbl_surf = self.fonts["title"].render(f"Turn {self.board.turn_number}: {who_label}", True, p_color)
        self.screen.blit(lbl_surf, (px, py))

        # Instructions / Step
        if is_ai_turn:
            step_text = "AI is computing optimal wavepacket superposition..."
            step_col = COLOR_YELLOW
        elif self.selected_sq1 is None:
            step_text = "Step 1 of 2: Click the 1st box for superposition"
            step_col = COLOR_TEXT
        else:
            step_text = f"Step 2 of 2: Click 2nd box (Box {self.selected_sq1 + 1} chosen)"
            step_col = COLOR_GREEN

        step_surf = self.fonts["body"].render(step_text, True, step_col)
        self.screen.blit(step_surf, (px, py + 36))

        # Mathematical State Representation Card
        math_card = pygame.Rect(px, py + 75, self.side_panel_rect.width - 44, 110)
        pygame.draw.rect(self.screen, COLOR_SURFACE0, math_card, border_radius=12)
        draw_neon_rect(self.screen, p_color, math_card, border_radius=12, width=1, glow_layers=1)

        m_head = self.fonts["badge"].render("QUBIT SUPERPOSITION STATE VECTOR", True, p_color)
        self.screen.blit(m_head, (math_card.x + 16, math_card.y + 14))

        if self.selected_sq1 is not None:
            state_eq = f"|ψ⟩ = 1/√2 ( |Box {self.selected_sq1 + 1}⟩ + |?⟩ )"
        else:
            state_eq = f"|ψ_{self.board.turn_number}⟩ = 1/√2 ( |Box A⟩ + |Box B⟩ )"

        eq_surf = self.fonts["body_bold"].render(state_eq, True, COLOR_TEXT)
        self.screen.blit(eq_surf, (math_card.x + 16, math_card.y + 40))

        prob_desc = "Probability Amplitude: 50% in Box A, 50% in Box B until collapsed."
        p_surf = self.fonts["small"].render(prob_desc, True, COLOR_SUBTEXT)
        self.screen.blit(p_surf, (math_card.x + 16, math_card.y + 75))

        # Strategic Guidance
        guide_y = py + 205
        g_title = self.fonts["body_bold"].render("💡 Tactical Guidance:", True, COLOR_TEXT)
        self.screen.blit(g_title, (px, guide_y))
        
        tips = [
            "• Share boxes with opponent to build entanglement networks.",
            "• Completing a closed loop lets your opponent collapse it!",
            "• Prevent opponent from capturing center or complete rows."
        ]
        for idx, tip in enumerate(tips):
            ts = self.fonts["small"].render(tip, True, COLOR_SUBTEXT)
            self.screen.blit(ts, (px, guide_y + 26 + idx * 22))

    def draw_collapse_panel(self, px, py):
        """Displays prominent neon collapse controls when an entanglement cycle forms."""
        collapse_info = self.board.pending_collapse
        resolving_p = collapse_info["resolving_player"]
        trigger_m = collapse_info["trigger_move"]
        opts = collapse_info["options"]
        is_ai_resolving = (self.vs_ai and resolving_p == self.ai_player)

        # Warning Card Header
        pulse = (math.sin(time.time() * 8) + 1) * 0.5
        warn_card = pygame.Rect(px, py, self.side_panel_rect.width - 44, 280)
        pygame.draw.rect(self.screen, COLOR_SURFACE0, warn_card, border_radius=14)
        draw_neon_rect(self.screen, COLOR_RED, warn_card, border_radius=14, width=2, glow_layers=3)

        w_title = self.fonts["title"].render("⚠️ QUANTUM COLLAPSE!", True, COLOR_RED)
        self.screen.blit(w_title, (warn_card.x + 16, warn_card.y + 16))

        res_name = "AI (Quantum Bot)" if is_ai_resolving else f"Player {resolving_p}"
        sub = f"Closed loop formed! {res_name} must measure the state."
        sub_surf = self.fonts["small"].render(sub, True, COLOR_YELLOW)
        self.screen.blit(sub_surf, (warn_card.x + 16, warn_card.y + 50))

        expl = (
            f"Move {trigger_m.label()} was placed across Box {opts[0] + 1} and Box {opts[1] + 1}. "
            f"Choose which box {trigger_m.label()} will collapse into. "
            f"This forces a domino cascade through all entangled marks!"
        )
        words = expl.split(" ")
        line = ""
        y_c = warn_card.y + 80
        for w in words:
            test = line + w + " "
            if self.fonts["small"].size(test)[0] < warn_card.width - 32:
                line = test
            else:
                self.screen.blit(self.fonts["small"].render(line, True, COLOR_TEXT), (warn_card.x + 16, y_c))
                y_c += 20
                line = w + " "
        if line:
            self.screen.blit(self.fonts["small"].render(line, True, COLOR_TEXT), (warn_card.x + 16, y_c))

        # Collapse Choice Buttons
        mouse_pos = pygame.mouse.get_pos()
        btn_w = (warn_card.width - 42) // 2
        self.btn_collapse_a = pygame.Rect(warn_card.x + 16, warn_card.y + 190, btn_w, 54)
        self.btn_collapse_b = pygame.Rect(warn_card.x + 26 + btn_w, warn_card.y + 190, btn_w, 54)

        if is_ai_resolving:
            ai_lbl = self.fonts["body_bold"].render("🤖 AI is evaluating collapse branches...", True, COLOR_YELLOW)
            self.screen.blit(ai_lbl, (warn_card.x + 20, warn_card.y + 205))
        else:
            # Draw Option A Button
            hov_a = self.btn_collapse_a.collidepoint(mouse_pos)
            pygame.draw.rect(self.screen, COLOR_SURFACE1 if hov_a else COLOR_BASE, self.btn_collapse_a, border_radius=10)
            draw_neon_rect(self.screen, COLOR_CYAN, self.btn_collapse_a, border_radius=10, width=2, glow_layers=2 if hov_a else 1)
            txt_a = self.fonts["body_bold"].render(f"Box {opts[0] + 1} ({trigger_m.label()})", True, COLOR_CYAN)
            self.screen.blit(txt_a, txt_a.get_rect(center=self.btn_collapse_a.center))

            # Draw Option B Button
            hov_b = self.btn_collapse_b.collidepoint(mouse_pos)
            pygame.draw.rect(self.screen, COLOR_SURFACE1 if hov_b else COLOR_BASE, self.btn_collapse_b, border_radius=10)
            draw_neon_rect(self.screen, COLOR_MAUVE, self.btn_collapse_b, border_radius=10, width=2, glow_layers=2 if hov_b else 1)
            txt_b = self.fonts["body_bold"].render(f"Box {opts[1] + 1} ({trigger_m.label()})", True, COLOR_MAUVE)
            self.screen.blit(txt_b, txt_b.get_rect(center=self.btn_collapse_b.center))

    def draw_game_over_banner(self, px, py):
        winner = self.board.winner
        win_card = pygame.Rect(px, py, self.side_panel_rect.width - 44, 280)
        pygame.draw.rect(self.screen, COLOR_SURFACE0, win_card, border_radius=14)

        if winner == 'Draw':
            draw_neon_rect(self.screen, COLOR_YELLOW, win_card, border_radius=14, width=2, glow_layers=3)
            w_text = "QUANTUM DRAW!"
            w_col = COLOR_YELLOW
            sub_text = "All boxes collapsed with no 3-in-a-row alignment."
        else:
            w_col = COLOR_GREEN
            draw_neon_rect(self.screen, COLOR_GREEN, win_card, border_radius=14, width=3, glow_layers=4)
            if self.vs_ai:
                w_text = "VICTORY! YOU WIN! 🎉" if winner == 'X' else "AI WINS! 🤖"
            else:
                w_text = f"PLAYER {winner} WINS! 🎉"
            
            sub_text = "Formed 3 Classical Marks in a row!"

        title_s = self.fonts["title"].render(w_text, True, w_col)
        self.screen.blit(title_s, (win_card.x + 16, win_card.y + 24))

        sub_s = self.fonts["body"].render(sub_text, True, COLOR_TEXT)
        self.screen.blit(sub_s, (win_card.x + 16, win_card.y + 64))

        # Allan Goff Quantum Tie-Breaker Explanation
        if winner in ('X', 'O'):
            info_box = pygame.Rect(win_card.x + 16, win_card.y + 105, win_card.width - 32, 85)
            pygame.draw.rect(self.screen, COLOR_BASE, info_box, border_radius=8)
            pygame.draw.rect(self.screen, COLOR_SURFACE2, info_box, 1, border_radius=8)
            
            h_s = self.fonts["badge"].render("ALLAN GOFF QUANTUM WIN RESOLUTION", True, COLOR_YELLOW)
            self.screen.blit(h_s, (info_box.x + 12, info_box.y + 10))
            
            desc1 = f"Winning classical row completed on collapse."
            desc2 = f"Player {winner} observed classical eigenstate first."
            self.screen.blit(self.fonts["small"].render(desc1, True, COLOR_SUBTEXT), (info_box.x + 12, info_box.y + 32))
            self.screen.blit(self.fonts["small"].render(desc2, True, COLOR_SUBTEXT), (info_box.x + 12, info_box.y + 54))

        # Play Again Button
        play_btn = pygame.Rect(win_card.x + 16, win_card.y + 208, win_card.width - 32, 48)
        mouse_pos = pygame.mouse.get_pos()
        hov = play_btn.collidepoint(mouse_pos)
        pygame.draw.rect(self.screen, COLOR_GREEN if hov else COLOR_SURFACE1, play_btn, border_radius=10)
        p_txt = self.fonts["body_bold"].render("⚡ Play Again (R)", True, COLOR_CRUST if hov else COLOR_GREEN)
        self.screen.blit(p_txt, p_txt.get_rect(center=play_btn.center))
        if hov and pygame.mouse.get_pressed()[0]:
            self.reset_game()


if __name__ == "__main__":
    game = QTacGame()
    game.run()
