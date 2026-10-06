# Cadastrar um cliente

Objetivo: sair com a pasta do cliente pronta, com ficha e régua, e o primeiro relatório batendo com o Gerenciador.

Pergunta uma coisa por vez. O gestor já roda tráfego pra esse cliente e sabe as respostas; teu papel é tirar isso da cabeça dele e colocar no arquivo.

## 1. Pasta

Cria `clientes/<nome-curto>/` com a subpasta `analises/`. Nome curto em minúsculas, sem acento e sem espaço.

## 2. Conta de anúncios

Cada cliente tem o próprio token, criado na BM dele. Se este cliente ainda não foi conectado, segue `metodo/conexao-meta.md` antes de continuar.

Com o token gravado, roda `python3 scripts/meta.py --cliente <nome> contas` e mostra a lista. O gestor aponta qual é a conta. Se não aparecer, a conta não foi atribuída ao usuário do sistema: passo 5 de `metodo/conexao-meta.md`.

Anota na ficha: ID da conta, moeda, fuso horário e o nome do token (`META_TOKEN_<NOME>`). Todo comando deste cliente leva `--cliente <nome>`.

## 3. Modelo de negócio

Segue as quatro perguntas de `metodo/modelos.md` e registra o modelo.

## 4. Entrevista da ficha

Pergunta e grava em `clientes/<nome>/CLAUDE.md`, a partir de `moldes/ficha-cliente.md`:

- quem é o cliente e o que vende;
- produto principal e preço;
- o que está rodando agora (campanha, lançamento, promoção) e as datas;
- pra onde o anúncio leva (página, WhatsApp, formulário, loja);
- **qual evento conta como resultado** nessa conta (lead, cadastro concluído, compra, conversa iniciada). Roda um `insights` de ontem e mostra os tipos de resultado que a conta registra, pra ele apontar qual é. Anota o nome exato do evento. Só um;
- **qual a fonte da verdade** do resultado: Gerenciador, planilha, plataforma de vendas, loja, CRM. Se for fora do Gerenciador, pergunta como tu consegue ler (arquivo exportado, planilha compartilhada) e anota o caminho;
- com quem o gestor fala no cliente e o que o cliente cobra ver.

## 5. Conferir o número

Antes de seguir, valida a ficha: puxa ontem pelo script, com o evento escolhido, e pede pro gestor comparar com o que ele vê no Gerenciador no mesmo dia.

Se não bater, as causas mais comuns são:

- evento errado, ou dois eventos parecidos sendo somados;
- janela de atribuição diferente da que ele usa na tela;
- fuso horário da conta diferente do dele.

Corrige a ficha e testa de novo. Não avança com número divergente.

## 6. Nomes de campanha

Lista as campanhas ativas e olha o padrão de nomes com o gestor.

O que um bom padrão de nome permite: achar todas as campanhas de uma ação por um trecho do nome, e saber pelo nome qual o objetivo e o tipo (teste, escala, remarketing).

- Se ele já tem padrão: anota na ficha exatamente como é, com um exemplo, e qual trecho identifica cada tipo.
- Se não tem: propõe um formato simples, com um identificador da ação, o objetivo, o tipo e um número de ordem. Ele ajusta. **Não renomeia nada que já está rodando** sem ele pedir; o padrão vale pras próximas.

Anota na ficha qual texto usar no filtro `--tag` pra pegar as campanhas da ação atual.

## 7. Links e rastreamento

Pergunta se os anúncios usam parâmetros de origem no link (UTM) e qual o padrão. Isso é o que permite cruzar a venda ou o lead real com a campanha, o conjunto e o criativo.

- Se usa: anota o padrão e o que cada parâmetro carrega.
- Se não usa: explica o que ele perde sem isso e propõe um padrão que preencha sozinho o nome da campanha, do conjunto e do anúncio. Aplicar nos anúncios é decisão dele.

## 8. Padrões ao subir campanha

Pergunta o que é sempre igual nessa conta ao criar campanha: janela de atribuição, gênero, idade, países ou região, posicionamentos, página e perfil do Instagram, pixel e evento de otimização, texto e botão padrão.

O jeito mais seguro de descobrir é ler um conjunto que funciona e mostrar a configuração dele: `python3 scripts/meta.py --cliente <nome> api GET <id-do-conjunto> --params '{"fields":"name,optimization_goal,billing_event,promoted_object,attribution_spec,targeting"}'`.

## 9. Régua

Segue `metodo/regua.md` do começo ao fim.

## 10. Fechar

Lê a ficha e a régua de volta pro gestor, em resumo, e pede o "pode". Depois roda o relatório do dia (`metodo/rotina.md`) pra mostrar tudo funcionando.
