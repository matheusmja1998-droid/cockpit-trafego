# Rotina: relatório, análise e otimização

Antes de qualquer coisa aqui, lê a ficha (`clientes/<nome>/CLAUDE.md`) e a régua (`clientes/<nome>/regua.md`) do cliente. O evento que conta, a fonte da verdade, o filtro de nome e todos os limites vêm de lá.

## Relatório do dia

Pedidos que disparam: "como tá o cliente X", "relatório de hoje", "faz a análise do dia".

**O que puxar:**

```
python3 scripts/meta.py --cliente <nome> insights --conta <conta> --nivel campaign --tag "<filtro da ficha>" --desde ontem
python3 scripts/meta.py --cliente <nome> insights --conta <conta> --nivel campaign --tag "<filtro da ficha>" --desde hoje
python3 scripts/meta.py --cliente <nome> campanhas --conta <conta> --tag "<filtro da ficha>" --ativas
```

**Como montar:**

1. Tabela por campanha ativa: orçamento atual, depois ontem (gasto, resultado, custo por resultado) e hoje parcial (os mesmos três). Linha de total no fim.
2. Uma linha de leitura: o total está no alvo, no aceitável ou acima do teto da régua.
3. Se a ficha tem fonte da verdade fora do Gerenciador, traz o número real ao lado e aponta a diferença.
4. Se o modelo tem funil depois do clique (grupo, pesquisa, agendamento, carrinho), acrescenta as etapas que tu consegue ler. As que dependem do gestor, pergunta.
5. Em lançamento: ritmo contra a meta (acumulado, meta, dias que faltam, quanto precisa por dia).

**Regras de leitura:**

- Ontem é dia fechado. Hoje é sempre parcial, e isso vai escrito.
- Não tira conclusão de hoje com pouco gasto.
- Dia ruim pra conta inteira (todo mundo piorou junto) é diferente de uma campanha ruim. Olha o conjunto antes de apontar culpado.
- Termina respondendo três coisas: está no ritmo? onde está o gargalo? qual a próxima ação?

Salva o relatório em `clientes/<nome>/analises/AAAA-MM-DD.md` quando o gestor pedir registro.

## Análise de criativo

Pedidos que disparam: "analisa os criativos", "qual criativo tá ruim", "o que eu pauso".

**O que puxar:** nível de anúncio, por dia, cobrindo os últimos dias.

```
python3 scripts/meta.py --cliente <nome> insights --conta <conta> --nivel ad --tag "<filtro>" --desde <6 dias atrás> --ate hoje --por-dia
```

**Como montar:** uma linha por criativo, com o custo por resultado em colunas: hoje, ontem, anteontem, últimos 3 dias, 3 dias anteriores e total. Junto, o gasto de cada janela.

**Como ler:**

- **A curva vale mais que a média.** Pra cada criativo, diz com uma palavra: subindo, caindo, parado, ou sem leitura (pouco resultado pra dizer). O acumulado esconde criativo que começou bem e está encarecendo.
- **De onde vem a mudança.** Se o custo subiu, olha se foi o custo do clique (leilão ou criativo cansando) ou a conversão depois do clique (página, oferta, público).
- **Criativo cruzado com público.** O mesmo criativo pode ir bem num público e mal em outro. Se ele roda em mais de uma campanha, mostra separado e junto. Antes de chamar um criativo de ruim, confere se o problema é o público onde ele está.
- **Pouco dado é pouco dado.** Abaixo do gasto mínimo da régua, não há veredito.
- **Em venda:** a venda real da fonte da verdade vem primeiro. Os números do Gerenciador entram como sinais que avisam antes (custo por visita na página, início de compra).

Depois aplica a régua e lista o que ela indica. Tudo como sugestão.

## Otimizar

Toda sugestão de mudança segue este formato:

```
Sugestão: pausar o anúncio "X" na campanha "Y"
Dado: [números, com período e fonte]
Regra: [qual linha da régua]
Risco: [o que pode dar errado se fizer; o que pode dar errado se não fizer]
```

- Separa o que é dado do que é interpretação tua.
- Uma recomendação principal. Se houver outras, vêm depois, em ordem de importância.
- Se a régua não cobre o caso, diz que não cobre e pergunta.
- Confere as travas da régua antes de sugerir (mínimo de criativos ativos, último criativo do conjunto, o que não se mexe).

**Executar, só depois do "pode":**

```
python3 scripts/meta.py --cliente <nome> pausar --id <id>              # mostra o que faria
python3 scripts/meta.py --cliente <nome> pausar --id <id> --confirmar  # executa
python3 scripts/meta.py --cliente <nome> orcamento --id <id> --diario <valor> --confirmar
```

Roda primeiro sem `--confirmar`, mostra o nome do objeto que voltou e confirma com o gestor que é aquele mesmo. Depois de executar, lê o objeto de novo pra confirmar que a mudança entrou, e registra em `clientes/<nome>/analises/` o que foi feito, quando e por qual regra.

Se o gestor recusar a sugestão, pergunta o motivo e oferece salvar como regra.

## Checagem semanal

Uma vez por semana, ou quando o gestor pedir "revisão da conta":

- criativos: quais carregam o resultado, quais estão cansando, o que falta testar;
- funil: onde se perde mais gente entre o clique e o resultado final;
- comparação com o melhor período do próprio cliente;
- parte técnica: página no ar, evento disparando, link com os parâmetros certos;
- régua: alguma regra foi contrariada várias vezes? Pode estar errada.
