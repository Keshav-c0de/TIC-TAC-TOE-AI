import math
import random

class Player():
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        pass

class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            # Note: Changed prompt to '0-8' since Tic-Tac-Toe is 9 squares (0 through 8)
            square = input(self.letter + '\'s turn. Input move (0-8): ') 
            try:
                val = int(square)
                # Check that the number is a valid square and is available
                if val not in range(9) or val not in game.available_moves(): 
                    raise ValueError
                valid_square = True
            except ValueError:
                print('Invalid square. Try again.')
        return val

class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        square = random.choice(game.available_moves())
        return square

class SmartComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            # Optimization: pick a random corner/center for the first move
            return random.choice([0, 2, 4, 6, 8]) 
        else:
            # CRITICAL FIX: The Minimax function is called on the game state
            square = self.minimax(game, self.letter)['position']
            return square

    def minimax(self, state, player):
        max_player = self.letter  # The smart computer player (yourself)
        other_player = 'O' if player == 'X' else 'X'

        # --- BASE CASES ---
        if state.current_winner == other_player:
            # Score proportional to how quickly the win was achieved
            score = 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (state.num_empty_squares() + 1)
            return {'position': None, 'score': score}
        elif not state.empty_squares():
            return {'position': None, 'score': 0}

        # --- INITIALIZATION ---
        if player == max_player:
            best = {'position': None, 'score': -math.inf}
        else:
            best = {'position': None, 'score': math.inf}

        # --- RECURSION ---
        for possible_move in state.available_moves():
            
            # CRITICAL FIX: 1. Create a copy of the state for this branch
            temp_state = state.copy()
            
            # 2. Make the move on the temporary state
            temp_state.make_move(possible_move, player) 
            
            # 3. Recurse on the temporary state
            # This isolates changes, eliminating the need for manual 'undo move'
            sim_score = self.minimax(temp_state, other_player) 

            sim_score['position'] = possible_move  # Store the move that led to this score

            # 4. Update the best move
            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
                    
        return best