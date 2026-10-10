# Reuniões

Uma ata por reunião com o orientador (ou com o laboratório). Serve para responder, meses
depois, **"o que o professor pediu?"** sem depender de memória — e para não confundir o que ele
disse com o que o aluno pensou na mesma hora.

## Como funciona

- **Um arquivo por reunião**, nomeado `AAAA-MM-DD-assunto.md`, com a data **da reunião** — não a
  data em que a ata foi escrita. Mesma lógica de `docs/registros/` e `docs/apresentacoes/`.
- **Para começar, copiar [`MODELO.md`](MODELO.md).** As seções vêm sempre na mesma ordem, para
  que se saiba onde olhar sem ler tudo.
- **Lida em um minuto.** Tópicos de uma linha, sem narrativa. Se um tópico precisa de um
  parágrafo para ser entendido, ele é um registro (`docs/registros/`), e a ata só aponta para lá.
- **Quem disse fica separado.** O que o professor disse vai numa seção; o que o aluno pensou,
  em outra. Na dúvida sobre quem disse, vai para as ideias do aluno — nunca se atribui ao
  professor uma frase que ele não disse.
- **Decisão é só o que foi fechado.** Sugestão do professor ainda não confirmada fica em "O que o
  professor disse" e reaparece em "Em aberto". Se uma decisão muda escopo ou arquitetura, o
  [`visao-geral.md`](../arquitetura/visao-geral.md) é atualizado **no mesmo commit** da ata.
- **Seção vazia não se apaga:** escreve-se _nenhuma_. Mostra que a pergunta foi feita.
- **As anotações cruas vão no fim**, sem edição, dentro de um bloco recolhível. A ata é a
  leitura organizada; as notas são a fonte, e é com elas que se confere a ata.
- **Ata não se corrige por cima.** Se algo se mostrar errado depois, acrescenta-se uma linha
  datada em "Correções" no fim — a versão original continua visível.

## O que não entra aqui

- **Descobertas e números** — ficam em [`docs/registros/`](../registros/). A ata cita o registro.
- **O que foi feito na semana** — fica em [`docs/diario/`](../diario/).
- **O que se pretende perguntar na próxima reunião** — fica em
  [`perguntas-orientador.md`](../arquitetura/perguntas-orientador.md). Depois da reunião, as
  respostas entram na ata.

---

## As reuniões

Da mais recente para a mais antiga.

| Data | Reunião | Em uma linha |
| --- | --- | --- |
| 30/09/2026 | [Alinhamento](2026-09-30-alinhamento.md) | Reuniões de 7 a 10 min, focadas em resultado; o sistema deve servir a quem recebe o laudo |
