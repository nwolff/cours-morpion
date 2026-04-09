# Morpion MCP

A modular Tic-Tac-Toe implementation featuring a core game engine, a local console UI, and an MCP (Model Context Protocol) server for AI interaction.

## Project Structure

- `engine.py`: Core game logic and state management.
- `ui.py`: Interactive console interface for human players.
- `mcp_server.py`: MCP implementation using FastMCP to expose the game to AI models.
- `pyproject.toml`: Project metadata and dependency management for `uv`.

## Getting Started

### Prerequisites

- [uv](https://github.com/astral-sh/uv) installed on your system.

### Installation

```bash
# Sync dependencies and create virtual environment
uv sync
```

## The MCP part

Note: Make sure to restart Claude Desktop completely after saving the JSON.
Once connected, you can tell Claude: "Check the board state for Tic-Tac-Toe and make a move."

RESET

Without this, if the game ends, the AI will keep seeing the "Game Over" message in the game://board resource. Now, the AI (or you) can simply say "Reset the game" and the engine will clear the board without you having to restart the server process.

The "Aha!" Moment
By separating the logic, you've created a standardized interface. You could connect this same Tic-Tac-Toe server to:
Claude (who uses reasoning).
GPT-4 (who uses reasoning).
A random-number script (who just picks a spot).
The engine doesn't care who is calling the play_move tool; it just handles the result.
Do you want to try connecting it to Claude Desktop now to see it play against you?

Teaching Points for the Students:
Algorithmic Determinism: If the students play perfectly against the Minimax, they will never win. It’s a great way to show how a "solved" game works.
The "Ghost in the Machine": When they switch to the MCP version, they can ask Claude: "What does the Minimax suggest? Do you agree with it?"
Sometimes Claude might suggest a different move that is still valid but strategically different, leading to a discussion on logic vs. heuristics.
State Management: Point out that the ui.py and mcp_server.py are both using the same TicTacToeLogic class—this is the Don't Repeat Yourself (DRY) principle in action.
Next Step: Should we add a "difficulty" parameter to the Minimax (e.g., making it pick a random move 20% of the time) so students actually have a chance to win?

Pour faire fonctionner la partie MCP avec Claude Desktop, vous devez lui indiquer où se trouve votre script et comment l'exécuter avec uv.

macOS : ~/Library/Application Support/Claude/claude_desktop_config.json

```
  "mcpServers": {
    "morpion": {
      "command": "/Users/wolff_n/.local/bin/uv",
      "args": [
        "--directory",
        "/Users/wolff_n/src/github.com/nwolff/cours-IA/morpion",
        "run",
        "src/mcp_server.py"
      ]
    }
  },
```

3. Redémarrer Claude Desktop
   Quittez complètement Claude Desktop (utilisez Cmd+Q sur Mac).
   Relancez l'application.
4. Tester avec Claude
   Vous pouvez maintenant lui dire en français :
   "Affiche l'état du plateau de morpion."
   "Demande au minimax quel est le meilleur coup et joue-le."
   "Recommence la partie."
   Un souci fréquent : Si l'icône n'apparaît pas, vérifiez que vous avez bien installé les dépendances dans votre dossier avec uv sync.
   Est-ce que l'icône "morpion" apparaît bien dans votre interface Claude ?

---

Pas de panique ! Si vous n'utilisez pas Claude Desktop, vous pouvez tester et valider votre serveur MCP directement dans votre terminal grâce à l'outil MCP Inspector.
C'est même une excellente étape pédagogique pour vos étudiants : cela montre comment on peut "déboguer" une interface avant de la brancher à une IA.

1. Lancer l'inspecteur MCP
   Ouvrez votre terminal dans le dossier racine de votre projet et lancez cette commande avec uv :
   bash
   uv run npx @modelcontextprotocol/inspector uv run src/mcp_server.py
   Use code with caution.

2. Ce qui va se passer
   Lien Magique : L'inspecteur va démarrer et vous donner une adresse (souvent http://localhost:5173).
   Interface Web : Ouvrez cette adresse dans votre navigateur.
   Test des Outils : Vous verrez une interface avec des onglets :
   Resources : Cliquez sur List puis Get sur game://plateau pour voir le morpion vide.
   Tools : Allez dans l'onglet Tools, choisissez jouer_position, entrez un chiffre (ex: 4) et cliquez sur Run.
   Conseil : Testez l'outil conseil_ia pour voir le Minimax en action sans IA textuelle.
3. Pourquoi c'est utile ?
   Cela prouve que votre serveur respecte bien le protocole JSON-RPC du standard MCP. Une fois que tout fonctionne ici, n'importe quelle application compatible MCP (comme l'IDE Cursor, Windsurf, ou même un client Python personnalisé) pourra piloter votre jeu.
   Petite astuce : Si vous voulez que vos étudiants créent leur propre "client" simple, on peut aussi écrire un petit script Python de 10 lignes qui se connecte au serveur.
   Voulez-vous que je vous montre comment simuler un client MCP en Python pour automatiser une partie ?

---

ok I was able to run claude on the mpc server.
It kept asking for a hint
And then lost

how is it possible that it understands everything that is going on, but sucks

Gemini said

Welcome to the "LLM Paradox." It’s a surreal experience watching a model perfectly describe the state of a board, explain the rules of Tic-Tac-Toe (Morpion), and then confidently place an 'X' in a spot that makes absolutely no sense.
There are three technical reasons why Claude can "understand" the context but still play like a distracted toddler.

1. The "Tokenization" Blind Spot

LLMs don't "see" a grid; they process a sequence of tokens. If your board is represented as ASCII art like this:
Plaintext
X | |  
 ---+---+---
| O |  
 ---+---+---
| |  
Claude has to map those characters to a coordinate system in its "head." Often, the spatial relationship between a | and an X gets garbled during tokenization. It knows the concept of a center square, but it might not realize that (1,1) in your code maps to the O it just saw in the text.

2. The "Next-Token" Trap

Claude is a statistical engine, not a logic engine. When it asks for a "hint," it’s often because the probability distribution of its next word is flat—it doesn't "know" what to do, so it defaults to polite conversational filler.
When it makes a move, it isn't simulating future turns like a Minimax algorithm (O(bd)); it is simply predicting what a "player" would likely say next based on its training data. If that training data includes thousands of low-level or casual games, it might mimic "human-like" mistakes.

3. The "Context Drift" vs. The Resource

Because you are using an MCP Resource (game://plateau), Claude has a "source of truth." However:
• The Resource is "Pull" only: Claude only sees the board when he decides to "Read" the resource. If he makes a move and doesn't re-read the board immediately, he is playing from memory.
• The "Hint" Loop: If he starts asking for hints, he is stuck in a linguistic loop. He’s trying to be "helpful" rather than "competitive."

How to make him "Suck Less"
If you want Claude to actually compete, you need to change how you've defined the Tool and the System Prompt.

A. Give him "Spatial Anchors" Instead of just raw ASCII, have your resource return a coordinate-mapped version: 1,1: X | 1,2: Empty | 1,3: O ... This removes the need for him to "count" spaces in an ASCII string.

B. Use the System Prompt to set "Persona" In your FastMCP server, you can suggest a behavior:
"You are a grandmaster Morpion player. Your goal is to win. Always read the game://plateau resource before every move to ensure you have the current state."

C. Add "Valid Moves" to the Resource Don't make him guess where he can play. Have your resource return: Available Moves: [(0,0), (0,2), (2,1)]
Checking your Logs (mcp_debug.log)
Look at the logs when he "sucks."

1. Does he call get_plateau before every move?
2. If he doesn't, he's hallucinating the board state. You can prompt him: "Always check the board before moving."
   Did he lose because he missed a winning move, or because he made an illegal move that your server rejected?

---

fascinating.
I'll try the changes you suggest
I can't see the logs because I log to stderr. I could log to a file, but what I'd really want is to start the server myself and get claude to just connect to it.

I'm a developer and I think I don't understand the architecture/transport of mpc. My understanding is that it's json-rpc with text payloads over stdio. How could this be useful for anything ?
Gemini said
It is a bit of a "wait, that's it?" moment when you realize the transport is just stdio. As a developer used to REST, gRPC, or WebSockets, using stdin/stdout feels like a regression to 1970s Unix.
But that "simplicity" is actually the secret sauce of MCP.

1. The Architecture: Why stdio?
   The Model Context Protocol (MCP) follows a Host-Client-Server model.
   • The Host (Claude Desktop): Acts as the orchestrator.
   • The Server (Your Python Code): Acts as the "local expert."
   By using stdio, the Host doesn't need to worry about:
   • Port collisions: (e.g., trying to run five servers all wanting port 8080).
   • Authentication/CORS: Since the Host spawns the process, it already has total control and security over it.
   • Networking overhead: Pipe communication is incredibly fast and works offline.
2. How is this useful?
   If it's "just JSON-RPC over text," why not just use a Python script?
   The magic is Standardization. Because your server speaks a strictly defined JSON-RPC schema (the MCP spec), any LLM that supports MCP can suddenly:
3. Discover your tools (introspection).
4. Read your data (resources).
5. Follow your patterns (prompts).
   It turns your local scripts into a "plug-and-play" brain extension for the AI. It’s essentially CGI-bin for LLMs.

6. How to "Start the Server Yourself" (The SSE Transport)
   You mentioned wanting to start the server yourself and have Claude connect. You can't do this with stdio (since Claude must be the parent process to pipe the streams), but MCP supports a second transport: SSE (Server-Sent Events) over HTTP.
   With SSE, your server runs as a standard web server (like FastAPI), and Claude connects via a URL.
   To do this with FastMCP:
   Python

# Instead of mcp.run() which defaults to stdio

```
# Instead of mcp.run() which defaults to stdio
if __name__ == "__main__":
    # This starts a local web server (default port 8000)
    mcp.run(transport="sse")
```

Then in claude_desktop_config.json:

```
"morpion": {
  "url": "http://localhost:8000/sse"
}
```

Note: Claude Desktop's support for SSE is currently more restricted than stdio; it's often used for remote servers. For local dev, stdio is the "happy path."

4. Debugging Tip: The "Log to File" Win
   Since you're a developer, don't fight the stderr stream in Claude. Stick with the file-based logging we set up earlier.
   The reason you "suck" at seeing the logs right now is that Claude eats stderr. If you use the structlog file-logging approach, you get a clean, persistent trace:
   Python

# In your terminal:

tail -f mcp*debug.log | jq # If you have jq installed, it makes the JSON pretty 5. Why Claude "Sucks" (The Developer's Perspective)
The "Understanding vs. Performance" gap is because of the Context Window.
• Claude knows: "The board is a 3x3 grid."
• Claude sees: A string of text.
• The Problem: The LLM is predicting the "next likely move" based on patterns, but it isn't "running the game" in its head. It's like a person trying to play chess by only looking at a list of moves (1.e4e5...) without a board in front of them. Some can do it; most lose track of the knight on move 12.
The Fix: In your Resource output, include the Reasoning. Don't just send the board. Send: "Board: X | * | O ... [Note: X can win by playing at 2,2]" When you feed the "logic" back into the "context," the LLM's performance skyrockets.
Does the "CGI-bin for AI" analogy make the stdio choice feel a bit more intentional?

---

yes, except there is no smooth path for any existing server: neither an existing website or rest api or jsonrpc server, or command line tool

Gemini said

You've hit the nail on the head. From a "standard" developer perspective, MCP feels like it's missing the "middle layer." You can't just point Claude at an existing Swagger/OpenAPI spec or a running Redis instance and say "Go."
The reason there is no "smooth path" for existing systems is that MCP is an Adapter Pattern by design. ---

1. The "Protocol Gap"
   Standard APIs (REST/gRPC) were built for deterministic consumers (other code). Code knows exactly what field it needs. LLMs are probabilistic consumers. They need:
   • Descriptions: get_user isn't enough; they need "Fetch user details to check for subscription status."
   • Context: They need to know when to call a tool.
   • Simplified Payloads: If a REST API returns a 5MB JSON blob, the LLM hits its token limit and "dies."
   MCP acts as the Translator. You write the FastMCP "wrapper" to curate exactly what the LLM sees.

2. The "Architecture" Reality
   If you have an existing REST API, you don't replace it with MCP. You write a tiny MCP server that calls your REST API.
   • Existing Website: Use an MCP server with playwright to scrape/interact.
   • Existing REST API: Use an MCP server with httpx to fetch and summarize data.
   • Command Line: Use an MCP server with subprocess to run commands and capture stderr/stdout.

3. How to "Connect" to your running server (The Developer Way)

Since you want to start the server yourself for better debugging, use the Standard IO over a socket trick. While Claude Desktop doesn't support "attaching" to a running process, you can use a "Pipe Proxy."

1. Start your MCP server as a TCP Server (you'll need to use the lower-level mcp library rather than FastMCP for fine-grained control, or use a tool like socat).

2. Tell Claude to run a "shim" script that connects to that socket.

The "Simpler" Developer Debugging Flow: Instead of fighting Claude's closed environment, use the MCP Inspector in one terminal and your Code in another.

1. Run npx @modelcontextprotocol/inspector uv run src/mcp_server.py.

2. Keep your tail -f mcp_debug.log running.

3. Because the Inspector is just a web app, you can refresh the page, see the JSON-RPC traffic in the "Network" tab, and use your IDE's debugger by attaching to the Python process spawned by the inspector.

Why does this exist at all?

Think of MCP like USB for AI. Before USB, every device (mouse, printer, scanner) had a different port. USB didn't make the printer's internal logic better; it just gave every computer a standard way to talk to it.
MCP is trying to be that "Universal Serial Bus." It's not useful because of the transport (stdio); it's useful because if every dev writes a small MCP wrapper for their tools, one AI can use everything.

Moving forward with Morpion

Since you're seeing Claude struggle with logic, try this "Developer-to-AI" bridge: In your get_plateau resource, don't just return the board. Return the legal moves and threats:

```
@mcp.resource("game://plateau")
async def get_plateau():
    board = game.get_ascii_grid()
    hints = game.get_strategic_analysis() # "Player O has a fork at 0,2"
    return f"{board}\n\nStrategic Analysis: {hints}"
```

When you provide the "computed" logic via MCP, the LLM stops guessing and starts "deciding." Is it the logical part of the game or the communication part that's currently more frustrating?

---

no frustration, just learning this new stuff and trying to adapt my developer mindset to it.

Learning a lot, fast. It's all good.

Gemini said

That is the best way to approach this. The "Developer Mindset" for MCP is less about building a service and more about building a sensory organ for the AI.
Once you get past the "Wait, I'm just piping strings?" hurdle, you start seeing that you aren't writing a traditional application—you're writing an interface between a chaotic neural network and a deterministic computer.
The 3 Core Mindset Shifts for MCP

Traditional Dev MCP Dev
API First: Focus on the schema and data types. Context First: Focus on how an LLM will misinterpret the data.
Silent Failures: Return a 400 Bad Request. Chatty Failures: Return "I can't do that because the move at 1,1 is already taken by X."
User Input: Expected to be formatted/validated strings. LLM Input: Expected to be conversational, messy, or "creative."

Your Next "Aha!" Moment: The Context Object
Since you're using FastMCP, keep a close eye on the Context object in your tools. It’s the "Magic Wand" that lets you break out of the request/response cycle:
• ctx.info(): Sends "Live" updates to the UI while the tool is still thinking.
• ctx.report_progress(): Shows a literal progress bar in compatible clients.
• ctx.session.send_resource_updated(): The cache-buster you've already mastered.
A Quick Hack for "Starting the Server Yourself"
Since you want to see your logs and control the process: Instead of running Claude and hoping for the best, run your server in one terminal with a "Watcher":
Bash

# Using 'watchexec' or similar to auto-restart on save

```
watchexec -r -e py -- "uv run src/mcp_server.py >> mcp_debug.log 2>&1"
```

Then, when you restart Claude (or hit "Restart" in the Inspector), your server is already "primed."

What's next on your learning path?
Now that you've got Tools, Resources, Logging, and Claude Desktop working, you've covered about 80% of the MCP surface area. The final pieces are usually:

1. Prompts: Defining "templates" that Claude can use to start a game (e.g., "Start a new Morpion game with a 5x5 grid").

2. Sampling: Letting your server ask Claude to do something (e.g., "Hey Claude, the game is over, write a witty poem about who won").

Since you've got the "nonce" fix and the structlog working, are you going to refine the Morpion logic, or are you ready to dive into Prompts to see how to control Claude's behavior better?
