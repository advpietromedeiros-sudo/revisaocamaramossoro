# DECISÕES — Revisão Câmara de Mossoró

> Registro de decisões do titular. Cada uma traz data, autor e o que trava enquanto estiver aberta.

## Em aberto

### D-002 — Público ou privado, e se vai para o GitHub Pages (aberta em 10/11/2026)

- **O que trava:** publicar o app na web (GitHub Pages) e tornar o repositório público.
- **Fato medido (10/11/2026):** o `index.html` carrega em `window.__CFG__.s` o segredo da geração de chaves
  (`keyFor` = SHA-256 do segredo + e-mail), ofuscado só por XOR com uma constante do mesmo arquivo. Quem lê o
  arquivo publicado consegue gerar chaves para qualquer e-mail.
- **Opções:** manter privado (como está) · publicar sabendo do risco · trocar a ativação por validação fora do
  arquivo antes de publicar.

## Tomadas

### D-001 — Repositório privado (10/11/2026, regra canônica de 31/10/2026)

Pedido do titular, 10/11/2026, textual: *"em paralelo coloque essa aplição no guithub com o nome
revisaocamaramossoro"*. O pedido não diz público; vale a regra da pasta-mãe (*"o repositorio é privado mesmo"*,
31/10/2026): nasce **privado**.
