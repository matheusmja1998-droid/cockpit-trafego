# Subir campanha, conjunto e anúncio

Criar é a operação com mais jeito de dar errado. Vai devagar, uma peça por vez, e sempre com o "pode" do gestor.

## Princípios

1. **Copia de algo que funciona.** Em vez de montar a configuração do zero, lê um conjunto e um anúncio da mesma conta que estão rodando bem e usa como base. Muda só o que precisa mudar.
2. **Tudo nasce pausado.** Cria com status pausado, mostra ao gestor no Gerenciador, e só ativa com o "pode".
3. **Poucos por vez.** Sobe dois ou três anúncios e confere antes de subir mais. Criar muitos de uma vez pode acionar bloqueio da conta.
4. **Segue os padrões da ficha.** Janela de atribuição, gênero, idade, região, posicionamentos, página, Instagram, pixel, evento, texto, botão e padrão de link estão em `clientes/<nome>/CLAUDE.md`. Se faltar algum, pergunta e grava.
5. **Nome no padrão do cliente.** Campanha, conjunto e anúncio seguem o formato anotado na ficha.

## Sequência

### 1. Entender o pedido

Confirma com o gestor: qual o objetivo, em qual campanha entra (nova ou existente), qual público, quais criativos, qual orçamento e quando começa.

### 2. Ler a base

```
python3 scripts/meta.py --cliente <nome> api GET <id-do-conjunto-base> --params '{"fields":"name,campaign_id,optimization_goal,billing_event,bid_strategy,promoted_object,attribution_spec,targeting,daily_budget"}'
python3 scripts/meta.py --cliente <nome> api GET <id-do-anuncio-base> --params '{"fields":"name,creative{object_story_spec,url_tags,asset_feed_spec}"}'
```

### 3. Montar e mostrar

Escreve os dados de cada peça num arquivo em `clientes/<nome>/analises/subida-AAAA-MM-DD/` (um JSON por peça). Mostra ao gestor um resumo em português: nome, orçamento, público, criativos, link. Pede o "pode".

### 4. Criar, na ordem

Sempre pelo caminho da conta, informando o ID da peça de cima:

```
python3 scripts/meta.py --cliente <nome> api POST act_<conta>/campaigns   --arquivo campanha.json --confirmar
python3 scripts/meta.py --cliente <nome> api POST act_<conta>/adsets      --arquivo conjunto.json --confirmar
python3 scripts/meta.py --cliente <nome> api POST act_<conta>/adcreatives --arquivo criativo.json --confirmar
python3 scripts/meta.py --cliente <nome> api POST act_<conta>/ads         --arquivo anuncio.json  --confirmar
```

Depois de cada criação, lê a peça de volta e confere se ficou como pedido.

### 5. Conferir e ativar

Pede pro gestor abrir no Gerenciador e olhar a prévia do anúncio. Com o "pode", ativa.

## Cuidados que evitam erro

- **Vídeo certo.** Antes de usar um vídeo da biblioteca, confere o título dele (`api GET <id-do-vídeo> --params '{"fields":"title,length"}'`). Nome parecido já fez subir vídeo errado.
- **Público fechado tem dois campos.** Em remarketing ou público pequeno, a entrega fora do público selecionado só desliga de verdade com os dois ajustes: `targeting_automation.advantage_audience = 0` e `targeting_relaxation_types = {"lookalike": 0, "custom_audience": 0}`. Na criação, manda os dois sempre. Depois lê o conjunto e confere.
- **Público amplo automático muda regras.** Com a segmentação automática ligada, gênero e idade viram sugestão, e a idade máxima tem piso alto. Avisa o gestor quando isso afetar o que ele pediu.
- **Início programado se define na criação.** Se o gestor quer que comece em dia e hora marcados, o horário de início entra ao criar o conjunto.
- **Conjunto precisa de pelo menos 24 horas** entre início e fim, quando tem fim.
- **Mesmo criativo em muitas campanhas** pode fazer uma disputar com a outra. Antes de repetir um criativo, mostra onde ele já roda e pergunta.
- **Erro "objeto não existe ou falta permissão" ao criar** com leitura funcionando: cadastro do aplicativo incompleto. Ver `metodo/conexao-meta.md`.
- **Campos legais ou de transparência** que a plataforma exige em alguns países e setores às vezes não salvam por aqui. Se o Gerenciador reclamar de anunciante ou beneficiário, o gestor preenche na tela.
- **Anúncio reprovado.** Não recria nem edita pra tentar passar. Avisa o gestor, anota o tema na régua como restrição e segue com os outros.

## O que anotar depois

Em `clientes/<nome>/analises/`, registra o que subiu, com IDs, data e quem aprovou. Se descobriu um padrão novo da conta no caminho, grava na ficha.
