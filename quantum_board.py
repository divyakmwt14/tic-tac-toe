"""
Quantum Tic-Tac-Toe Core Game Engine
Implements quantum superposition, entanglement graphs, cycle detection,
and wavefunction collapse resolution based on quantum mechanics principles.
"""

from collections import deque, defaultdict
from typing import List, Tuple, Optional, Dict, Set

WINNING_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Cols
    (0, 4, 8), (2, 4, 6)             # Diagonals
]

class QuantumMove:
    def __init__(self, move_id: int, player: str, sq1: int, sq2: int):
        self.move_id = move_id
        self.player = player  # 'X' or 'O'
        self.squares = (sq1, sq2)
        self.collapsed = False
        self.final_square: Optional[int] = None

    def other_square(self, sq: int) -> int:
        return self.squares[1] if self.squares[0] == sq else self.squares[0]

    def label(self) -> str:
        # e.g., "X₁", "O₂"
        subscripts = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        return f"{self.player}{str(self.move_id).translate(subscripts)}"

    def plain_label(self) -> str:
        return f"{self.player}{self.move_id}"

    def __repr__(self):
        status = f"-> {self.final_square}" if self.collapsed else "superposition"
        return f"Move({self.plain_label()}: {self.squares} [{status}])"


class QuantumBoard:
    def __init__(self):
        # Classical board: square index -> QuantumMove that collapsed there
        self.classical: Dict[int, Optional[QuantumMove]] = {i: None for i in range(9)}
        # List of all moves made
        self.moves: List[QuantumMove] = []
        # Current turn counter (1-indexed)
        self.turn_number: int = 1
        # Active cycle pending collapse resolution: dict with info or None
        self.pending_collapse: Optional[dict] = None
        # Game over flag and winner info ('X', 'O', 'Draw', or None)
        self.winner: Optional[str] = None
        self.winning_line: Optional[Tuple[int, int, int]] = None
        self.game_over: bool = False
        # Educational explanation log
        self.last_quantum_event: str = "Game started. In superposition, each move exists in two squares simultaneously."

    @property
    def current_player(self) -> str:
        # Turn 1 is X, 2 is O, 3 is X, etc.
        return 'X' if self.turn_number % 2 == 1 else 'O'

    @property
    def opponent_player(self) -> str:
        return 'O' if self.current_player == 'X' else 'X'

    def get_available_squares(self) -> List[int]:
        """Returns list of squares that have not yet collapsed into a classical state."""
        return [sq for sq, move in self.classical.items() if move is None]

    def get_spooky_marks_in_square(self, sq: int) -> List[QuantumMove]:
        """Returns all uncollapsed quantum moves touching this square."""
        if self.classical[sq] is not None:
            return []
        return [m for m in self.moves if not m.collapsed and sq in m.squares]

    def get_entanglement_graph(self) -> Dict[int, List[Tuple[int, QuantumMove]]]:
        """Builds adjacency list of the uncollapsed quantum entanglement graph."""
        adj = defaultdict(list)
        for m in self.moves:
            if not m.collapsed:
                u, v = m.squares
                adj[u].append((v, m))
                adj[v].append((u, m))
        return adj

    def find_cycle_with_new_move(self, sq1: int, sq2: int, new_move: QuantumMove) -> Optional[List[QuantumMove]]:
        """
        Checks if adding new_move between sq1 and sq2 creates a cycle.
        Returns the list of QuantumMove objects that make up the cycle, or None.
        """
        adj = self.get_entanglement_graph()
        # Find if there was already a path between sq1 and sq2
        queue = deque([(sq1, [new_move], set([sq1]))])
        
        while queue:
            curr, path_moves, visited_sqs = queue.popleft()
            for neighbor, move in adj[curr]:
                if neighbor == sq2:
                    # Found a cycle!
                    return path_moves + [move]
                if neighbor not in visited_sqs:
                    visited_sqs_next = set(visited_sqs)
                    visited_sqs_next.add(neighbor)
                    queue.append((neighbor, path_moves + [move], visited_sqs_next))
        return None

    def make_quantum_move(self, sq1: int, sq2: int) -> dict:
        """
        Places a quantum move across sq1 and sq2 in superposition.
        If a cycle is detected, initiates pending_collapse for the opponent to resolve.
        Returns a dict status.
        """
        if self.game_over:
            return {"status": "error", "message": "Game is already over."}
        if self.pending_collapse is not None:
            return {"status": "error", "message": "A wavefunction collapse is pending resolution."}
        if sq1 == sq2:
            return {"status": "error", "message": "Cannot choose the same square twice. Superposition requires two distinct boxes."}
        if self.classical[sq1] is not None or self.classical[sq2] is not None:
            return {"status": "error", "message": "Cannot place spooky mark on an already collapsed classical square."}

        new_move = QuantumMove(self.turn_number, self.current_player, sq1, sq2)
        
        # Check cycle BEFORE adding to moves list
        cycle_moves = self.find_cycle_with_new_move(sq1, sq2, new_move)
        
        self.moves.append(new_move)
        player_placed = self.current_player
        self.turn_number += 1

        if cycle_moves:
            # Cycle detected!
            # The opponent of player_placed resolves the collapse
            resolving_player = 'O' if player_placed == 'X' else 'X'
            self.pending_collapse = {
                "trigger_move": new_move,
                "cycle_moves": cycle_moves,
                "resolving_player": resolving_player,
                "options": [sq1, sq2],
                "message": f"Cycle detected! Opponent ({resolving_player}) must collapse {new_move.label()} into box {sq1+1} or box {sq2+1}."
            }
            self.last_quantum_event = (
                f"Loop created by {new_move.label()} across boxes {sq1+1} & {sq2+1}! "
                f"Wavefunction collapse triggered. Player {resolving_player} must choose the measurement outcome."
            )
            return {
                "status": "cycle_detected",
                "move": new_move,
                "pending_collapse": self.pending_collapse
            }
        else:
            self.last_quantum_event = (
                f"Move {new_move.label()}: Superposition created across boxes {sq1+1} & {sq2+1}. "
                f"Entanglement degree increases."
            )
            return {
                "status": "success",
                "move": new_move
            }

    def resolve_collapse(self, chosen_square: int) -> dict:
        """
        Resolves the pending wavefunction collapse by fixing trigger_move into chosen_square.
        Cascades through entangled moves, collapsing them deterministically.
        Then checks for win conditions.
        """
        if self.pending_collapse is None:
            return {"status": "error", "message": "No collapse pending."}
        
        trigger_move: QuantumMove = self.pending_collapse["trigger_move"]
        if chosen_square not in self.pending_collapse["options"]:
            return {"status": "error", "message": "Chosen square is not one of the valid collapse endpoints."}

        resolving_player = self.pending_collapse["resolving_player"]
        
        # Perform cascade collapse
        collapsed_this_round = []
        occupied_classical = set(sq for sq, m in self.classical.items() if m is not None)
        
        # Queue of (move, square_it_must_take)
        queue = deque([(trigger_move, chosen_square)])
        handled_moves = set([trigger_move])

        while queue:
            curr_move, target_sq = queue.popleft()
            curr_move.collapsed = True
            curr_move.final_square = target_sq
            self.classical[target_sq] = curr_move
            occupied_classical.add(target_sq)
            collapsed_this_round.append(curr_move)

            # Any other uncollapsed move touching target_sq MUST be forced to its other square
            for m in self.moves:
                if not m.collapsed and m not in handled_moves and target_sq in m.squares:
                    other_sq = m.other_square(target_sq)
                    handled_moves.add(m)
                    queue.append((m, other_sq))

        # Check if any remaining moves in the entire connected component can now be settled
        # or if any other squares were forced
        changed = True
        while changed:
            changed = False
            for m in self.moves:
                if not m.collapsed and m not in handled_moves:
                    sq_a, sq_b = m.squares
                    if sq_a in occupied_classical and sq_b not in occupied_classical:
                        handled_moves.add(m)
                        queue.append((m, sq_b))
                        changed = True
                    elif sq_b in occupied_classical and sq_a not in occupied_classical:
                        handled_moves.add(m)
                        queue.append((m, sq_a))
                        changed = True
            while queue:
                curr_move, target_sq = queue.popleft()
                curr_move.collapsed = True
                curr_move.final_square = target_sq
                self.classical[target_sq] = curr_move
                occupied_classical.add(target_sq)
                collapsed_this_round.append(curr_move)

        self.pending_collapse = None
        
        # Check win condition
        win_result = self.check_win()
        
        self.last_quantum_event = (
            f"Measurement complete: Wavefunction collapsed by {resolving_player}! "
            f"{len(collapsed_this_round)} spooky marks resolved into classical states."
        )

        return {
            "status": "collapsed",
            "collapsed_moves": collapsed_this_round,
            "win_result": win_result
        }

    def check_win(self) -> dict:
        """
        Evaluates classical 3-in-a-row states.
        Implements Allan Goff's Quantum Tic-Tac-Toe tie-breaker rule:
        If both players achieve 3-in-a-row in the same collapse, the player whose
        winning line has the lower maximum move subscript wins.
        """
        lines_x = []
        lines_o = []

        for line in WINNING_LINES:
            marks = [self.classical[sq] for sq in line]
            if all(m is not None and m.player == 'X' for m in marks):
                max_subscript = max(m.move_id for m in marks)
                lines_x.append((max_subscript, line))
            elif all(m is not None and m.player == 'O' for m in marks):
                max_subscript = max(m.move_id for m in marks)
                lines_o.append((max_subscript, line))

        if lines_x and not lines_o:
            self.winner = 'X'
            self.winning_line = min(lines_x, key=lambda x: x[0])[1]
            self.game_over = True
            return {"winner": 'X', "line": self.winning_line}
        elif lines_o and not lines_x:
            self.winner = 'O'
            self.winning_line = min(lines_o, key=lambda x: x[0])[1]
            self.game_over = True
            return {"winner": 'O', "line": self.winning_line}
        elif lines_x and lines_o:
            # Both players have 3-in-a-row!
            min_max_x = min(l[0] for l in lines_x)
            min_max_o = min(l[0] for l in lines_o)
            if min_max_x < min_max_o:
                self.winner = 'X'
                self.winning_line = [l[1] for l in lines_x if l[0] == min_max_x][0]
                self.game_over = True
                return {"winner": 'X', "line": self.winning_line, "tiebreaker": True}
            elif min_max_o < min_max_x:
                self.winner = 'O'
                self.winning_line = [l[1] for l in lines_o if l[0] == min_max_o][0]
                self.game_over = True
                return {"winner": 'O', "line": self.winning_line, "tiebreaker": True}
            else:
                self.winner = 'Draw'
                self.game_over = True
                return {"winner": 'Draw'}
        else:
            # Check if all 9 squares have classical marks (board full)
            if all(self.classical[sq] is not None for sq in range(9)):
                self.winner = 'Draw'
                self.game_over = True
                return {"winner": 'Draw'}
            return {"winner": None}

    def clone(self) -> 'QuantumBoard':
        """Creates a deep copy of the board for AI lookahead simulation."""
        new_board = QuantumBoard()
        new_board.turn_number = self.turn_number
        new_board.winner = self.winner
        new_board.winning_line = self.winning_line
        new_board.game_over = self.game_over
        new_board.last_quantum_event = self.last_quantum_event

        # Clone moves
        move_map = {}
        for m in self.moves:
            cm = QuantumMove(m.move_id, m.player, m.squares[0], m.squares[1])
            cm.collapsed = m.collapsed
            cm.final_square = m.final_square
            move_map[m.move_id] = cm
            new_board.moves.append(cm)

        # Clone classical
        for sq, m in self.classical.items():
            if m is not None:
                new_board.classical[sq] = move_map[m.move_id]

        # Clone pending collapse
        if self.pending_collapse is not None:
            trigger_m = move_map[self.pending_collapse["trigger_move"].move_id]
            cycle_ms = [move_map[m.move_id] for m in self.pending_collapse["cycle_moves"]]
            new_board.pending_collapse = {
                "trigger_move": trigger_m,
                "cycle_moves": cycle_ms,
                "resolving_player": self.pending_collapse["resolving_player"],
                "options": list(self.pending_collapse["options"]),
                "message": self.pending_collapse["message"]
            }

        return new_board
