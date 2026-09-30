# Registros

Um arquivo por momento que vale contar: uma descoberta, uma decisão com alternativa
descartada, um número que vai ter que ser defendido.

Serve para três coisas, nesta ordem de importância:

1. **Guardar o porquê.** Daqui a seis meses, na hora de escrever o artigo ou de responder a
   um professor, o "o que foi feito" está no código e o "por que foi feito assim" não está
   em lugar nenhum — a menos que alguém escreva.
2. **Virar apresentação.** Cada registro tem uma frase e um punhado de consequências — e uma
   figura, quando houver número que se enxergue melhor desenhado. Um slide sai quase por
   recorte.
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

O gabarito de cada arquivo, nesta ordem:

> **a frase** · **o que aconteceu** · **a evidência** · **como conferir** · **por que
> importa** · **o que eu decidi** · **ligações** · **o que ficou em aberto**

"Como conferir" vem logo depois da evidência, não no fim: é ele que sustenta a evidência, e
quem duvidar do número vai querer o comando antes de ler as conclusões tiradas dele.

## O que não entra aqui

- **`docs/diario/`** — o que foi feito em cada semana, cronológico, para o orientador.
- **`visao-geral.md` §9** — índice de decisões, uma linha por decisão, sem narrativa.
- **`docs/artigo/`** — escrito mais tarde, a partir destes registros.
- Trabalho de rotina. "Escrevi o parser" não é registro; "descobri que ler um ODC como DS
  não dá erro nenhum" é.

---

## Os registros

Do mais recente para o mais antigo.

| Data | Registro |
| --- | --- |
| 29/09/2026 | [O laboratório lê τ a 10 mm, não no máximo da curva — e a envoltória D1N passa a ser c = 22,6 kPa, φ = 32,2°](2026-09-29-ruptura-a-10mm.md) |
| 29/09/2026 | [A série D1N fecha uma envoltória com R² = 0,987 — mas só depois dos dois filtros](2026-09-29-envoltoria-d1n.md) |
| 13/09/2026 | [As máquinas gravam dois layouts com a mesma extensão, e nenhuma forma de ler avisa quando você erra o tipo](2026-09-13-dois-layouts.md) |
| 12/09/2026 | [O ensaio com a maior razão τ/σ do acervo é um dos bons — a magnitude não separa nada](2026-09-12-forma-da-curva.md) |
| 12/09/2026 | [Três ensaios registraram resistência altíssima sem nunca romper — e a conferência manual não teria como perceber](2026-09-12-ensaios-travados.md) |
| 12/09/2026 | [O identificador do ensaio parece dizer a tensão normal — e em seis casos ele mente](2026-09-12-id-nao-e-dado.md) |
| 12/09/2026 | [O acervo tem 914 ensaios utilizáveis — e a maior parte do descarte não é ensaio perdido](2026-09-12-triagem-do-acervo.md) |
| 12/09/2026 | [O projeto deixou de ser instrumentação e virou engenharia de dados](2026-09-12-mudanca-de-escopo.md) |

## Os scripts por trás dos números

| Script | O que calcula |
| --- | --- |
| `scripts/triagem_acervo.py` | as quatro situações do acervo: 914, 108, 17, 4 |
| `scripts/ensaios_nao_rompidos.py` | os ensaios que não romperam: 13, 421, 9, 3 |
| `scripts/razao_tau_sigma.py` | a razão τ/σ de cada ensaio: 211, 106, 105 |
| `scripts/id_versus_sigma.py` | identificadores repetidos com σ divergente: 748, 96, 6 |
| `scripts/comparar_layouts.py` | os dois layouts e os três modos de falha |
| `scripts/figura_*.py` | as figuras, a partir dos scripts acima |
| `scripts/apoio_apresentacao.py` | a envoltória D1N e suas variantes com τ a 10 mm (`variantes`: 22,6 kPa, 32,2°, 0,980) e pelo máximo (`variantes-maximo`: 24,0 kPa, 32,6°, 0,987); as curvas D1N (`curvas-d1n`); o acervo a 10 mm (`acervo-10mm`: 914, 116, 798); as figuras `envoltoria-d1n-10mm.png`, `envoltoria-d1n.png` e `forma-da-curva-268.png` |
