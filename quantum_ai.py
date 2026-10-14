"""
Quantum AI Engine for Q-Tac-Toe
Implements probabilistic evaluation and Minimax-inspired quantum decision making
for move selection and wavefunction collapse resolution.
"""

import random
from typing import Tuple, List, Optional
from quantum_board import QuantumBoard, QuantumMove, WINNING_LINES

# Square position weights (center > corners > edges)
POSITION_WEIGHTS = {
    4: 1.4,          # Center
    0: 1.1, 2: 1.1,  # Corners
    6: 1.1, 8: 1.1,
    1: 1.0, 3: 1.0,  # Edges
    5: 1.0, 7: 1.0
}

class QuantumAI:
    def __init__(self, ai_player: str = 'O', difficulty: str = "hard"):
        self.ai_player = ai_player  # 'O' or 'X'
        self.human_player = 'X' if ai_player == 'O' else 'O'
        self.difficulty = difficulty.lower()  # 'normal' or 'hard'

    def evaluate_board(self, board: QuantumBoard) -> float:
        """
        Heuristic evaluation of a board state from the perspective of ai_player.
        Higher score favors AI, lower score favors human.
        """
        if board.game_over:
            if board.winner == self.ai_player:
                return 10000.0
            elif board.winner == self.human_player:
                return -10000.0
            else:
                return 0.0  # Draw

        score = 0.0

        # 1. Classical marks evaluation
        for line in WINNING_LINES:
            marks = [board.classical[sq] for sq in line]
            ai_count = sum(1 for m in marks if m is not None and m.player == self.ai_player)
            human_count = sum(1 for m in marks if m is not None and m.player == self.human_player)
            empty_count = sum(1 for m in marks if m is None)

            if ai_count == 3:
                return 10000.0
            if human_count == 3:
                return -10000.0

            if ai_count == 2 and empty_count == 1:
                score += 350.0  # Threatening a win
            elif human_count == 2 and empty_count == 1:
                score -= 400.0  # Opponent threatening a win (high defensive priority)
            elif ai_count == 1 and empty_count == 2:
                score += 30.0
            elif human_count == 1 and empty_count == 2:
                score -= 35.0

        # 2. Position weights for classical marks
        for sq, move in board.classical.items():
            if move is not None:
                mult = POSITION_WEIGHTS.get(sq, 1.0)
                if move.player == self.ai_player:
                    score += 25.0 * mult
                else:
                    score -= 25.0 * mult

        # 3. Superposition presence evaluation
        for sq in range(9):
            if board.classical[sq] is None:
                spooky = board.get_spooky_marks_in_square(sq)
                ai_spooky = sum(1 for m in spooky if m.player == self.ai_player)
                hu_spooky = sum(1 for m in spooky if m.player == self.human_player)
                mult = POSITION_WEIGHTS.get(sq, 1.0)
                score += (ai_spooky * 12.0 - hu_spooky * 12.0) * mult

        return score

    def choose_collapse(self, board: QuantumBoard) -> int:
        """
        When Human triggers a cycle, AI chooses which square trigger_move collapses into.
        Simulates both options and selects the one with maximum score for AI.
        """
        if board.pending_collapse is None:
            return 0

        options = board.pending_collapse["options"]
        best_choice = options[0]
        best_score = -float('inf')

        for opt in options:
            sim_board = board.clone()
            sim_board.resolve_collapse(opt)
            score = self.evaluate_board(sim_board)

            # In normal mode, add slight randomness
            if self.difficulty == "normal":
                score += random.uniform(-15.0, 15.0)

            if score > best_score:
                best_score = score
                best_choice = opt

        return best_choice

    def choose_quantum_move(self, board: QuantumBoard) -> Tuple[int, int]:
        """
        Selects the best pair of squares (sq1, sq2) for the AI's quantum move.
        Evaluates potential cycles, collapse outcomes, and positional advantages.
        """
        available = board.get_available_squares()
        if len(available) < 2:
            return (0, 1)

        candidate_pairs = []
        for i in range(len(available)):
            for j in range(i + 1, len(available)):
                candidate_pairs.append((available[i], available[j]))

        scored_moves = []

        for sq1, sq2 in candidate_pairs:
            sim_board = board.clone()
            result = sim_board.make_quantum_move(sq1, sq2)

            if result["status"] == "cycle_detected":
                # Opponent (Human) gets to resolve the collapse!
                # By Minimax, assume human will pick the option worst for AI
                opts = sim_board.pending_collapse["options"]
                branch_scores = []
                for opt in opts:
                    branch_board = sim_board.clone()
                    branch_board.resolve_collapse(opt)
                    branch_scores.append(self.evaluate_board(branch_board))
                # Human minimizes AI score
                expected_score = min(branch_scores)
            else:
                expected_score = self.evaluate_board(sim_board)

            # Positional bias
            expected_score += (POSITION_WEIGHTS.get(sq1, 1.0) + POSITION_WEIGHTS.get(sq2, 1.0)) * 10.0

            scored_moves.append((expected_score, (sq1, sq2)))

        # Sort descending by score
        scored_moves.sort(key=lambda x: x[0], reverse=True)

        if self.difficulty == "normal" and len(scored_moves) > 3:
            # Softmax / probabilistic choice among top 3 candidates
            top_candidates = scored_moves[:3]
            weights = [3, 2, 1]
            chosen = random.choices(top_candidates, weights=weights, k=1)[0]
            return chosen[1]

        # In Hard mode, pick the top move
        return scored_moves[0][1]
