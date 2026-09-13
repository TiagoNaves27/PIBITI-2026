# Registros

Um arquivo por momento que vale contar: uma descoberta, uma decisão com alternativa
descartada, um número que vai ter que ser defendido.

Serve para três coisas, nesta ordem de importância:

1. **Guardar o porquê.** Daqui a seis meses, na hora de escrever o artigo ou de responder a
   um professor, o "o que foi feito" está no código e o "por que foi feito assim" não está
   em lugar nenhum — a menos que alguém escreva.
2. **Virar apresentação.** Cada registro tem uma frase, uma figura e um punhado de
   consequências. Um slide sai quase por recorte.
3. **Deixar o número conferível.** Todo número citado num registro vem de um script
   versionado em `scripts/`, que qualquer pessoa pode rodar de novo.

## Como funciona

- **Um arquivo por episódio**, nomeado `AAAA-MM-DD-assunto.md`, com a data em que a coisa
  aconteceu. Assim a pasta se ordena sozinha e vira a linha do tempo do projeto.
- **O título é uma afirmação**, não um assunto. "O acervo tem 914 ensaios utilizáveis", não
  "Análise do acervo".
- **Escrito para quem não estava lá** — inclusive para você mesmo daqui a seis meses. Sem
  "como vimos ontem", sem depender de conversa anterior.
- **Separar o que o dado mostra do que é interpretação.** São dois parágrafos rotulados, não
  um texto só. "125 arquivos não têm etapa de cisalhamento, e 108 deles têm um arquivo de
  mesmo ID e mesma data que tem" é dado. "O laboratório salva o ensaio em duas partes" é
  interpretação, e vai marcada como tal até alguém do laboratório confirmar.
- **Nada de contexto inventado.** Não afirmar o que ninguém disse — como o acervo era usado
  antes, o que o operador pensava, por que alguém fez o que fez. Se não veio de uma pessoa
  ou de um arquivo, ou é dedução declarada, ou não entra. Um registro existe para ser
  defendido na frente de um professor; uma frase plausível e sem fonte é o que derruba o
  resto.
- **Figura gerada por script**, nunca print de tela, guardada em `figuras/` e usando a
  paleta do `CLAUDE.md`.
- **Registro não se corrige por cima.** Se o número mudar depois, o registro antigo fica
  como está e nasce um novo explicando a mudança. A pasta é um histórico, não uma
  enciclopédia — mostrar que o projeto errou e corrigiu é parte do que se quer mostrar.

O gabarito de cada arquivo: a frase · o que aconteceu · a evidência · por que importa · o
que eu decidi · como conferir · ligações · o que ficou em aberto.

## O que não entra aqui

- **`docs/diario/`** — o que foi feito em cada semana, cronológico, para o orientador.
- **`visao-geral.md` §9** — índice de decisões, uma linha por decisão, sem narrativa.
- **`docs/artigo/`** — escrito mais tarde, a partir destes registros.
- Trabalho de rotina. "Escrevi o parser" não é registro; "descobri que ler um ODC como DS
  não dá erro nenhum" é.

---

## Os registros

| Data | Registro |
| --- | --- |
| 12/09/2026 | [O acervo tem 914 ensaios utilizáveis — e a maior parte do descarte não é ensaio perdido](2026-09-12-triagem-do-acervo.md) |
