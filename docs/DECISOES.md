# DECISÕES — Revisão Câmara de Mossoró

> Registro de decisões do titular. Cada uma traz data, autor e o que trava enquanto estiver aberta.

## Em aberto

Nenhuma em 10/11/2026, 20h49.

## Tomadas

### D-002 — Repositório PÚBLICO, app no GitHub Pages (10/11/2026, 20h49, titular)

- **Decisão do titular, textual:** opção *"Publicar no GitHub Pages"* (pergunta das 20h41) e *"pode deixar publico"*.
- **Risco aceito, com o fato medido em 10/11/2026:** o `index.html` carrega em `window.__CFG__.s` o segredo da
  geração de chaves (`keyFor` = SHA-256 do segredo + e-mail), ofuscado só por XOR com uma constante do mesmo arquivo.
  Publicado, quem ler o código consegue gerar chaves válidas para qualquer e-mail. O titular foi avisado antes de
  decidir. Substitui a D-001 quanto à visibilidade.
- **Caminho para fechar o risco depois, se quiser:** validar a chave fora do arquivo (servidor) ou trocar o segredo
  e distribuir chaves novas.

### D-001 — Repositório privado (10/11/2026, regra canônica de 31/10/2026)

Pedido do titular, 10/11/2026, textual: *"em paralelo coloque essa aplição no guithub com o nome
revisaocamaramossoro"*. O pedido não diz público; vale a regra da pasta-mãe (*"o repositorio é privado mesmo"*,
31/10/2026): nasce **privado**.
