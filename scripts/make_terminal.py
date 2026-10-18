"""Generates the animated terminal header: assets/terminal-dark.svg and terminal-light.svg.

Edit SESSION below and run:  python3 scripts/make_terminal.py
Commands "type" out, then their output appears. Pure SVG + SMIL animation, so it
works inside a GitHub README (no JavaScript, no external service).
"""
from pathlib import Path
from xml.sax.saxutils import escape

# (command, [output lines]). Output segments are (text, color-role) pairs.
SESSION = [
    ("whoami", [[("Rajat Sharma", "name"), (" · Software Developer @ IBM · Toronto, ON", "text")]]),
    ("cat now.txt", [[("Building Maximo's multi-tenant SaaS on Kubernetes + OpenShift", "text")],
                     [("Go · Python · Helm · Tekton · Argo CD · Terraform · AWS", "dim")]]),
    ("kubectl get projects", [
        [("NAME            STATUS    STACK", "dim")],
        [("loonie-ledger   ", "name"), ("Running", "ok"), ("   Java · Python · Node.js · Redis Streams", "text")],
        [("lsm-kv          ", "name"), ("Running", "ok"), ("   Java 21 · WAL · SSTables · Bloom filters", "text")],
    ]),
    ("echo $CONTACT", [[("rajatjc.github.io · linkedin.com/in/rajatjc · rajat.jc@gmail.com", "link")]]),
]

THEMES = {
    "dark": {"bg": "#0d1117", "border": "#30363d", "bar": "#161b22", "title": "#8b949e", "prompt": "#3fb950",
             "cmd": "#e6edf3", "text": "#c9d1d9", "dim": "#8b949e", "name": "#79c0ff", "ok": "#3fb950", "link": "#d2a8ff"},
    "light": {"bg": "#ffffff", "border": "#d0d7de", "bar": "#f6f8fa", "title": "#57606a", "prompt": "#1a7f37",
              "cmd": "#1f2328", "text": "#1f2328", "dim": "#6e7781", "name": "#0969da", "ok": "#1a7f37", "link": "#8250df"},
}

WIDTH, LINE_H, TOP, LEFT, CHAR_W = 860, 22, 58, 22, 8.45
TYPE_SECONDS_PER_CHAR, PAUSE = 0.055, 0.45


def build(theme: dict) -> str:
    rows, t, y = [], 0.6, TOP
    clip_defs = []
    for i, (command, output) in enumerate(SESSION):
        # Prompt appears, then the command types out by widening a clip rectangle.
        type_time = len(command) * TYPE_SECONDS_PER_CHAR
        clip_id = f"c{i}"
        clip_defs.append(
            f'<clipPath id="{clip_id}"><rect x="{LEFT + 2 * CHAR_W}" y="{y - 16}" height="{LINE_H}" width="0">'
            f'<animate attributeName="width" from="0" to="{len(command) * CHAR_W + 6:.0f}" begin="{t:.2f}s" '
            f'dur="{type_time:.2f}s" fill="freeze"/></rect></clipPath>')
        rows.append(f'<g opacity="0"><set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/>'
                    f'<text x="{LEFT}" y="{y}" fill="{theme["prompt"]}">$</text>'
                    f'<text x="{LEFT + 2 * CHAR_W}" y="{y}" fill="{theme["cmd"]}" clip-path="url(#{clip_id})">{escape(command)}</text></g>')
        t += type_time + PAUSE
        y += LINE_H
        for line in output:
            spans = "".join(f'<tspan fill="{theme[role]}">{escape(text)}</tspan>' for text, role in line)
            rows.append(f'<text x="{LEFT}" y="{y}" opacity="0" xml:space="preserve">{spans}'
                        f'<set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/></text>')
            t += 0.12
            y += LINE_H
        t += PAUSE
        y += 6
    # Final prompt with a blinking cursor.
    rows.append(f'<g opacity="0"><set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/>'
                f'<text x="{LEFT}" y="{y}" fill="{theme["prompt"]}">$</text>'
                f'<rect x="{LEFT + 2 * CHAR_W}" y="{y - 14}" width="9" height="17" fill="{theme["prompt"]}">'
                f'<animate attributeName="opacity" values="1;0;1" dur="1.1s" begin="{t:.2f}s" repeatCount="indefinite"/></rect></g>')
    height = y + 22
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" viewBox="0 0 {WIDTH} {height}" role="img" aria-label="Terminal: Rajat Sharma, software developer at IBM in Toronto. Projects: loonie-ledger and lsm-kv.">
<defs>{"".join(clip_defs)}</defs>
<rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{height - 1}" rx="10" fill="{theme["bg"]}" stroke="{theme["border"]}"/>
<path d="M0.5 10.5 a10 10 0 0 1 10-10 h{WIDTH - 21} a10 10 0 0 1 10 10 v20 h-{WIDTH - 1} z" fill="{theme["bar"]}"/>
<line x1="0.5" y1="30.5" x2="{WIDTH - 0.5}" y2="30.5" stroke="{theme["border"]}"/>
<circle cx="20" cy="16" r="6" fill="#ff5f57"/><circle cx="40" cy="16" r="6" fill="#febc2e"/><circle cx="60" cy="16" r="6" fill="#28c840"/>
<text x="{WIDTH / 2}" y="20" text-anchor="middle" fill="{theme["title"]}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="12">rajat@toronto: ~</text>
<g font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace" font-size="14">
{chr(10).join(rows)}
</g>
</svg>
'''


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "assets"
    out.mkdir(exist_ok=True)
    for name, theme in THEMES.items():
        (out / f"terminal-{name}.svg").write_text(build(theme), encoding="utf-8")
        print(f"wrote assets/terminal-{name}.svg")
