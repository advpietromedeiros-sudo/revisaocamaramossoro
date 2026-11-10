# CLAUDE.md — Revisão Câmara de Mossoró (Kit de Estudos)

> ANTES DE QUALQUER AÇÃO, leia o `0 Readme First/FAROL.md`, o `docs/DECISOES.md` e o `docs/PROCEDENCIA.md`.
> As regras gerais estão em `C:\Users\advpi\Repositório\CLAUDE.md` e no HARNESS da pasta-mãe.

- **O que é:** app de estudo de página única (`index.html`) com a Lei Orgânica do Município de Mossoró e o
  Regimento Interno da Câmara Municipal de Mossoró: lei seca, questões (múltipla escolha e certo/errado),
  cartões de revisão, desempenho e ativação por chave de licença.
- **Pilha:** HTML/CSS/JS num arquivo só, dados embutidos (`window.__DATA__`), progresso no `localStorage` do
  navegador. Sem servidor, sem dependência. ⚠️ **Fora da pilha do roteiro (§P4)** — divergência declarada.
- **Portas e containers:** nenhum. Abre com duplo clique.
- **Remoto:** `advpietromedeiros-sudo/revisaocamaramossoro`, **privado** (D-001).
- 🔴 **O `index.html` traz embutido o segredo que gera as chaves de licença** (`window.__CFG__`, ofuscado por XOR,
  reversível). Publicar o arquivo (repositório público, GitHub Pages) permite a qualquer um gerar chaves válidas.
  Ver D-002.
