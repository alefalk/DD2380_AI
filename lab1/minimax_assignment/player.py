#!/usr/bin/env python3
import math


from fishing_game_core.game_tree import Node
from fishing_game_core.player_utils import PlayerController
from fishing_game_core.shared import ACTION_TO_STR


class PlayerControllerHuman(PlayerController):
    def player_loop(self):
        """
        Function that generates the loop of the game. In each iteration
        the human plays through the keyboard and send
        this to the game through the sender. Then it receives an
        update of the game through receiver, with this it computes the
        next movement.
        :return:
        """

        while True:
            # send message to game that you are ready
            msg = self.receiver()
            if msg["game_over"]:
                return


class PlayerControllerMinimax(PlayerController):

    def __init__(self):
        super(PlayerControllerMinimax, self).__init__()
        self.start_time = None

    def player_loop(self):
        """
        Main loop for the minimax next move search.
        :return:
        """

        # Generate first message (Do not remove this line!)
        first_msg = self.receiver()

        while True:
            msg = self.receiver()
            self.start_time = time()
            # Create the root node of the game tree
            node = Node(message=msg, player=0)

            _, best_move = self.search_best_next_move(initial_tree_node=node, depth=6, alpha=-999999, beta=999999, player=0)
            # Execute next action
            self.sender({"action": ACTION_TO_STR[best_move], "search_time": None})

    def search_best_next_move(self, initial_tree_node, depth, alpha, beta, player):
        """
        Use minimax (and extensions) to find best possible next move for player 0 (green boat)
        :param initial_tree_node: Initial game tree node
        :type initial_tree_node: game_tree.Node
            (see the Node class in game_tree.py for more information!)
        :return: either "stay", "left", "right", "up" or "down"
        :rtype: str
        """

        # EDIT THIS METHOD TO RETURN BEST NEXT POSSIBLE MODE USING MINIMAX ###

        # NOTE: Don't forget to initialize the children of the current node
        #       with its compute_and_get_children() method!

        children = initial_tree_node.compute_and_get_children()

        if len(children) == 0 or depth == 0 or time() - self.start_time >= 0.06:
            v = self.heuristic(initial_tree_node)
            return v, initial_tree_node.move
        elif player == 0:
            v = -999
            action = 0
            for child in children:
                child_score, child_action = self.search_best_next_move(child, depth - 1, alpha, beta, 1)
                if child_score > v:
                    v = child_score
                    action = child_action
                alpha = max(alpha, child_score)
                if beta <= alpha:
                    break
            return v, action
        else: # player == 1
            v = 999
            action = 0
            for child in children:
                child_score, child_action = self.search_best_next_move(child, depth - 1, alpha, beta, 0)
                if child_score < v:
                    v = child_score
                    action = child_action
                beta = min(beta, child_score)
                if beta <= alpha:
                    break
            return v, action

    def heuristic(self, curr_node):
        p0_fish_caught = curr_node.state.get_caught()[0]
        current_score_diff = curr_node.state.get_player_scores()[0] - curr_node.state.get_player_scores()[1]
        # if player 0 caught a fish in this state
        if p0_fish_caught:
            return current_score_diff + p0_fish_caught
        else: # if not caught calculate the value of this state f(n) = g(n) + h(n)
            return current_score_diff + self.distance_value(curr_node, 0) - self.distance_value(curr_node,1)

    def distance_value(self, curr_node, player):
        hook_pos = curr_node.state.get_hook_positions()
        fish_pos = curr_node.state.get_fish_positions()
        fish_scores = curr_node.state.get_fish_scores()

        best_fish_score = 0
        for fish_id, fish_pos in fish_pos.items():
            # [x/y][player] ==> [0][0] = x coordinate for player 0
            xDist, yDist = hook_pos[player][0] - fish_pos[0], hook_pos[player][1] - fish_pos[1]
            euclideanDist = math.sqrt((min(xDist, 20 - xDist))**2 + yDist**2)
            # calculate new fish score as a function of fish score and the distance to that fish
            fish_score = fish_scores[fish_id] * (1 / (1 if euclideanDist == 0 else euclideanDist))
            # maximize the new fish score value
            best_fish_score = max(fish_score, best_fish_score)

        return best_fish_score

