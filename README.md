# Goal

This repo is a teaching tool built around Tic-Tac-Toe (morpion) to help students understand the Minimax algorithm and game theory.

The core idea: a single game engine powers three interfaces — a CLI, a Flask web app, and an MCP server that lets Claude Desktop play the game. This illustrates how a clean engine can be reused across very different integration patterns.

The web interface (also available as a static page deployable to GitHub Pages) lets students set up any board position and ask Minimax to analyse it. The full decision tree is displayed level by level, showing every position Minimax considered, the outcome of each branch, and which move it considers optimal. This makes the algorithm's reasoning visible and inspectable rather than a black box.

# Insights

Great question — and the answer reveals something fundamental about minimax.

Minimax assumes the opponent plays perfectly. And in tic-tac-toe, against a perfect opponent, every opening move is a draw regardless of where you start. So minimax is actually correct: all first moves are equivalent (score 0) because no starting move can force a win against optimal play.

The intuition that "center and corners are harder to defend" is true against a human who might slip up — those moves create more threats and require more precise responses. But minimax doesn't model imperfect opponents. It always assumes the opponent will find the best reply.

This is the key limitation/feature of minimax: it's the worst-case optimal strategy. It never loses against anyone, but it also doesn't exploit weaknesses — it just guarantees a draw (or win if one exists).
