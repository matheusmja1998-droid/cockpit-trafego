# Como montar a régua de um cliente

A régua é o conjunto de regras que diz quando pausar, quando esperar e quando mexer em orçamento naquele cliente. Ela existe pra que a decisão de hoje seja igual à de ontem, e pra que o Claude sugira do jeito que o gestor decidiria.

**Regra principal: tu não traz número.** Todo valor da régua vem de uma destas fontes, nesta ordem:

1. o gestor diz;
2. o histórico da conta mostra (tu puxa e apresenta, ele confirma);
3. conta feita junto a partir do preço, da margem ou da verba.

Se nenhuma das três resolve, o campo fica como "a definir" e a regra não é usada até ser preenchida.

## Passo 1: puxar o histórico

Antes de perguntar, puxa os números da conta num período que o gestor considere normal (pergunta qual). Por campanha e por criativo: gasto, resultado no evento da ficha e custo por resultado.

Mostra um resumo: melhor e pior custo por resultado, onde a maior parte ficou, e quanto varia de um dia pro outro. Isso dá chão pra conversa. Gestor que nunca escreveu régua costuma saber os números quando vê o próprio histórico.

## Passo 2: as três faixas

Toda régua começa com três valores do número que manda (ver `metodo/modelos.md`):

- **alvo:** onde ele quer estar;
- **aceitável:** até onde vai sem mexer;
- **teto:** acima disso ele intervém.

Pergunta os três. Se ele só souber um, propõe os outros a partir do histórico e pede confirmação.

## Passo 3: regras de poda (quando pausar um criativo)

Faz as perguntas abaixo. Cada resposta vira uma linha da régua.

1. **Gasto mínimo pra julgar.** Quanto um criativo precisa gastar antes de tu ter opinião sobre ele? Abaixo disso é ruído. Em venda direta, muita gente pensa nisso como parte do preço do produto.
2. **Quantos dias ruins seguidos.** Um dia acima do teto já pausa, ou tu espera mais? Quantos dias fechados?
3. **Sem resultado nenhum.** Gastou quanto sem trazer nada e tu corta?
4. **Caro no acumulado.** Tem criativo que alterna dia bom e dia ruim e nunca cai na regra dos dias seguidos. Tu quer uma regra de média de alguns dias pra pegar esse caso?
5. **Veterano.** Criativo que já foi bom e teve um dia ruim recebe o mesmo tratamento de um novo, ou tem mais paciência?
6. **O que se pausa.** Só o anúncio, ou o conjunto junto? Em teste de público, a unidade é o conjunto e não o criativo.

## Passo 4: regras de orçamento

1. **Quando sobe.** Abaixo de qual custo por resultado tu aumenta a verba?
2. **Quanto sobe por vez** e quanto tempo espera entre um aumento e outro.
3. **Quando reduz** e em quanto.
4. **Em quais campanhas.** Orçamento na campanha ou no conjunto? Tem campanha em que não se mexe?
5. **Horário.** Tu mexe em orçamento em qualquer hora ou só com o dia fechado?
6. **Gasto mínimo do dia pra decidir.** Mexer de manhã cedo, com pouca verba gasta, costuma ser decisão em cima de ruído. Qual a parcela do orçamento do dia que precisa ter saído antes de julgar?

## Passo 5: travas de segurança

Pergunta e grava sempre:

- Qual o mínimo de criativos ativos que uma campanha de escala deve ter? Abaixo disso, tu não pausa: avisa.
- Nunca pausar o último criativo ativo de um conjunto sem avisar.
- Tem campanha, conjunto ou criativo em que ninguém mexe sem ordem dele?
- Tem tema, palavra ou tipo de anúncio que a conta não pode rodar (política da plataforma, regra do cliente, regra do setor)?

## Passo 6: particularidades da conta

Pergunta aberta: "o que tu sabe dessa conta que um gestor novo não saberia?". Exemplos do que costuma aparecer:

- qual número avisa antes do custo subir;
- dias e horários melhores e piores;
- tipo de público que funciona e tipo que nunca funcionou;
- quantos criativos por campanha rendem melhor;
- o que acontece quando o mesmo criativo roda em várias campanhas;
- padrões ao subir campanha (janela de atribuição, gênero, idade, países, posicionamentos).

Grava cada resposta com a data. Isso vale mais que qualquer regra genérica.

## Passo 7: escrever e validar

Escreve `clientes/<nome>/regua.md` a partir de `moldes/regua.md`. Depois lê a régua de volta pro gestor em linguagem simples e pede o "pode".

Em seguida faz a prova: aplica a régua nos últimos dias da conta e mostra o que ela teria feito. Se o resultado for diferente do que o gestor fez de verdade, pergunta o motivo. A diferença quase sempre é uma regra que ele usa e não tinha falado.

## Usando a régua no dia a dia

- Toda sugestão cita a regra que seguiu.
- Se a situação não está coberta pela régua, diz isso e pergunta. Não improvisa regra.
- Quando o gestor decide diferente da régua, pergunta se é exceção ou se a régua muda. Se muda, atualiza o arquivo com data e motivo.
- De tempos em tempos, relê a régua com ele. Régua parada vira regra errada.
