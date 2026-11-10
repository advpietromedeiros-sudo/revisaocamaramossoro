"""Portão do Kit Câmara de Mossoró: roda todas as portas e só abre com todas verdes (HARNESS §P6, REGRA CINCO).

Cada porta tem nome, o que faz e o erro que impede. Porta pulada sai 2 e se diz.

Uso: python docs/verificar_antes_de_subir.py              roda as portas sobre o index.html
     python docs/verificar_antes_de_subir.py --autoteste  planta 4 defeitos e só sai 0 se CADA um for acusado
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
APP = RAIZ / "index.html"
RX_SCRIPT = re.compile(r"<script>(.*?)</script>", re.S)

# lê os dados embutidos e devolve o que a integridade precisa conferir
SONDA = r"""
const fs = require('fs'); const window = {};
eval(fs.readFileSync(process.argv[2], 'utf8'));
const D = window.__DATA__ || {}, C = window.__CFG__ || {};
const ids = new Set(); for (const l of ['lom','ri']) for (const a of ((D.laws||{})[l]||[])) ids.add(a.id);
const qs = D.q || [], fc = D.fc || [];
const ruins = [];
for (const q of qs) {
  for (const id of (q.a||[])) if (!ids.has(id)) ruins.push(q.id + ' cita ' + id);
  if (q.tp === 'mc' && !(Array.isArray(q.o) && q.o.length === 5 && q.c >= 0 && q.c < 5)) ruins.push(q.id + ' sem 5 alternativas ou gabarito');
  if (q.tp === 'ce' && typeof q.g !== 'boolean') ruins.push(q.id + ' sem gabarito C/E');
}
for (const c of fc) if (!ids.has(c.a)) ruins.push(c.id + ' cita ' + c.a);
console.log(JSON.stringify({lom: ((D.laws||{}).lom||[]).length, ri: ((D.laws||{}).ri||[]).length,
  q: qs.length, fc: fc.length, cfg: Array.isArray(C.s) && C.s.length > 0, ruins}));
"""


def portas(html: str) -> list[tuple[str, str | None]]:
    """Devolve (nome, erro ou None) de cada porta."""
    out: list[tuple[str, str | None]] = []
    scripts = RX_SCRIPT.findall(html)
    if len(scripts) < 2:
        return [("o app tem o script de dados e o de lógica", f"achei {len(scripts)} bloco(s) <script>")]
    with tempfile.TemporaryDirectory() as d:
        erros = []
        for i, s in enumerate(scripts):
            arq = Path(d) / f"s{i}.js"
            arq.write_text(s, encoding="utf-8")
            r = subprocess.run(["node", "--check", str(arq)], capture_output=True, text=True, encoding="utf-8")
            if r.returncode:
                erros.append(f"bloco {i + 1}: " + (r.stderr.strip().splitlines() or ["?"])[-1])
        out.append(("JavaScript do app sem erro de sintaxe", "; ".join(erros) or None))
        dados = Path(d) / "dados.js"
        dados.write_text(scripts[0], encoding="utf-8")
        sonda = Path(d) / "sonda.js"
        sonda.write_text(SONDA, encoding="utf-8")
        r = subprocess.run(["node", str(sonda), str(dados)], capture_output=True, text=True, encoding="utf-8")
        if r.returncode:
            out.append(("dados embutidos legíveis", (r.stderr.strip().splitlines() or ["?"])[-1]))
            return out
        m = json.loads(r.stdout)
    vazio = [k for k in ("lom", "ri", "q", "fc") if not m[k]]
    out.append(("dados embutidos completos (LOM, Regimento, questões, cartões)",
                f"vazio: {', '.join(vazio)}" if vazio else None))
    out.append(("toda questão e todo cartão citam artigo que existe; gabaritos válidos",
                f"{len(m['ruins'])} defeito(s), ex.: {m['ruins'][:3]}" if m["ruins"] else None))
    out.append(("configuração da licença presente", None if m["cfg"] else "window.__CFG__.s ausente"))
    out.append(("contagem", f"__info__ LOM {m['lom']} · Regimento {m['ri']} · questões {m['q']} · cartões {m['fc']}"))
    return out


def rodar(html: str, falar: bool = True) -> int:
    falhou = False
    for nome, erro in portas(html):
        if erro and erro.startswith("__info__"):
            if falar:
                print(f"  [ i ] {erro[9:]}")
            continue
        falhou |= bool(erro)
        if falar:
            print(f"  [{' X ' if erro else 'OK '}] {nome}" + (f" — {erro}" if erro else ""))
    return 1 if falhou else 0


def autoteste() -> int:
    html = APP.read_text(encoding="utf-8")
    alvo = re.search(r'"a":\["(lom:[^"]+)"\]', html)
    sabotagens = [
        ("JavaScript quebrado", lambda h: h.replace("function $(id){", "function $(id){{", 1)),
        ("questão citando artigo inexistente", lambda h: h.replace(alvo.group(0), '"a":["lom:9999"]', 1) if alvo else h),
        ("questões apagadas", lambda h: re.sub(r'"q":\[.*?\],"fc":', '"q":[],"fc":', h, count=1, flags=re.S)),
        ("gabarito fora das alternativas", lambda h: h.replace('"c":0,', '"c":7,', 1)),
    ]
    ok = True
    for nome, f in sabotagens:
        h2 = f(html)
        if h2 == html:
            print(f"  ❌ não plantou: {nome}")
            ok = False
            continue
        acusou = rodar(h2, falar=False) == 1
        print(f"  {'✅ acusou' if acusou else '❌ NÃO acusou'}: {nome}")
        ok &= acusou
    print("AUTOTESTE " + ("OK: os 4 defeitos plantados foram acusados" if ok else "FALHOU"))
    return 0 if ok else 1


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if shutil.which("node") is None:
        print("⚠️ node não encontrado: portão PULADO (sai 2)")
        sys.exit(2)
    if "--autoteste" in sys.argv:
        sys.exit(autoteste())
    rc = rodar(APP.read_text(encoding="utf-8"))
    print("  ✅ portão aberto" if rc == 0 else "  ❌ portão fechado")
    sys.exit(rc)
