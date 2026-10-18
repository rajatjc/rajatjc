"""Community tic-tac-toe, played through GitHub issues.

Each empty square in the README links to a new issue titled "ttt|move|<square>|<game>".
The tictactoe workflow runs this script, which applies the move, redraws the board
between the README's <!--START:ttt--> and <!--END:ttt--> markers, and writes a reply
for the issue.

  python3 scripts/tictactoe.py move     # reads ISSUE_TITLE, ISSUE_USER, COMMENT_FILE
  python3 scripts/tictactoe.py render   # just redraws the README from game/state.json
"""
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "game" / "state.json"
README = ROOT / "README.md"
REPO = os.environ.get("GITHUB_REPOSITORY", "rajatjc/rajatjc")
LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
MARK = {"X": "❌", "O": "⭕"}
SQUARE = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]


def new_state() -> dict:
    return {"game": 1, "board": [""] * 9, "turn": "X", "last_player": None, "last_result": None,
            "moves": [], "players": {}, "totals": {"X": 0, "O": 0, "draw": 0}}


def load() -> dict:
    return json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else new_state()


def save(state: dict) -> None:
    STATE.parent.mkdir(exist_ok=True)
    STATE.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def outcome(board: list) -> str | None:
    for a, b, c in LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    return "draw" if all(board) else None


def play(state: dict, title: str, user: str) -> tuple[bool, str]:
    """Applies a move. Returns (accepted, reply for the issue)."""
    m = re.fullmatch(r"ttt\|move\|([1-9])\|(\d+)", title.strip())
    if not m:
        return False, "That doesn't look like a move. Click one of the numbered squares in my profile README."
    square, game = int(m[1]), int(m[2])
    if game != state["game"]:
        return False, (f"That link was for game #{game}, but game #{state['game']} is being played now. "
                       "Pick a square from the current board.")
    if state["board"][square - 1]:
        return False, f"Square {square} is already taken. Pick an empty one."
    if user == state["last_player"]:
        return False, "You made the last move, so let someone else go next. Come back after their turn!"

    mark = state["turn"]
    state["board"][square - 1] = mark
    state["last_player"] = user
    state["players"][user] = state["players"].get(user, 0) + 1
    state["moves"].insert(0, {"user": user, "mark": mark, "square": square, "game": game,
                              "at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")})
    del state["moves"][8:]

    result = outcome(state["board"])
    if result is None:
        state["turn"] = "O" if mark == "X" else "X"
        return True, f"Thanks @{user}! You played {MARK[mark]} on square {square}. Next up: {MARK[state['turn']]}."
    state["totals"][result] += 1
    state["last_result"] = {"game": game, "result": result, "by": user}
    finished = (f"{MARK[result]} wins game #{game}, and you made the winning move!" if result != "draw"
                else f"Game #{game} ends in a draw.")
    state.update(game=game + 1, board=[""] * 9, turn="X", last_player=None)
    return True, f"Thanks @{user}! {finished} Game #{game + 1} has started."


def move_link(square: int, game: int) -> str:
    title = quote(f"ttt|move|{square}|{game}")
    body = quote("Just press **Create**. The board in the README updates within a minute or two.")
    return f"https://github.com/{REPO}/issues/new?title={title}&body={body}"


def render(state: dict) -> str:
    rows = []
    for r in range(3):
        cells = []
        for c in range(3):
            i = r * 3 + c
            mark = state["board"][i]
            cell = MARK[mark] if mark else f'<a href="{move_link(i + 1, state["game"])}">{SQUARE[i]}</a>'
            cells.append(f'<td align="center" width="64" height="64">{cell}</td>')
        rows.append(f"<tr>{''.join(cells)}</tr>")
    out = [
        f"**Game #{state['game']}** · next move: {MARK[state['turn']]} · "
        "click a numbered square, then press **Create** on the issue that opens.",
        "",
        f'<table>{"".join(rows)}</table>',
        "",
    ]
    if state.get("last_result"):
        lr = state["last_result"]
        out.append(f"Last game (#{lr['game']}): " + (f"{MARK[lr['result']]} won, winning move by @{lr['by']}."
                                                     if lr["result"] != "draw" else "a draw."))
        out.append("")
    t = state["totals"]
    out.append(f"All-time: ❌ {t['X']} wins · ⭕ {t['O']} wins · {t['draw']} draws")
    if state["moves"]:
        out += ["", "**Recent moves**", ""]
        out += [f"- {MARK[m['mark']]} on square {m['square']} by [@{m['user']}](https://github.com/{m['user']}) "
                f"(game #{m['game']}, {m['at']})" for m in state["moves"][:5]]
    if state["players"]:
        top = sorted(state["players"].items(), key=lambda kv: (-kv[1], kv[0]))[:10]
        out += ["", "**Top players**", "", "| Player | Moves |", "| --- | --: |"]
        out += [f"| [@{u}](https://github.com/{u}) | {n} |" for u, n in top]
    return "\n".join(out)


def write_readme(state: dict) -> None:
    text = README.read_text(encoding="utf-8")
    pattern = re.compile(r"(<!--START:ttt-->)(.*?)(<!--END:ttt-->)", re.S)
    if not pattern.search(text):
        sys.exit("README.md has no <!--START:ttt--> / <!--END:ttt--> markers")
    README.write_text(pattern.sub(lambda m: f"{m[1]}\n{render(state)}\n{m[3]}", text), encoding="utf-8")


if __name__ == "__main__":
    state = load()
    if len(sys.argv) > 1 and sys.argv[1] == "move":
        accepted, reply = play(state, os.environ["ISSUE_TITLE"], os.environ["ISSUE_USER"])
        if accepted:
            save(state)
            write_readme(state)
        Path(os.environ.get("COMMENT_FILE", "comment.md")).write_text(reply + "\n", encoding="utf-8")
        print(("accepted: " if accepted else "rejected: ") + reply)
    else:
        save(state)
        write_readme(state)
