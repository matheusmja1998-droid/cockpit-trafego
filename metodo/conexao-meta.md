# Conectar a Meta

Objetivo: o Claude conseguir ler e operar a conta de anúncios do cliente com um token que não depende do perfil pessoal de ninguém.

Quem faz o quê: os cliques no navegador são do gestor (ou do cliente, se o gestor não for administrador). Tu guia um passo por vez, espera ele dizer que fez, e confere.

Os nomes dos menus mudam com frequência. Se o gestor não achar um botão, descreve o objetivo do passo e pede pra ele dizer o que está vendo na tela.

## A regra que define tudo

A Meta separa dois níveis de acesso pra um aplicativo:

- **Acesso padrão:** vem liberado na hora. Serve pra gerenciar contas de anúncio **da mesma empresa (BM) dona do aplicativo**.
- **Acesso avançado:** serve pra gerenciar contas de anúncio **de outras empresas**. Exige análise do aplicativo pela Meta e verificação da empresa. Demora e pode ser negado.

Consequência prática: o aplicativo, o usuário do sistema e a conta de anúncios precisam estar **na mesma BM**. Ou seja, tudo é criado **dentro da BM do cliente**, uma vez por cliente.

Um aplicativo só na BM da agência, recebendo as contas dos clientes por parceria, parece mais simples, mas é justamente o que pede acesso avançado. Sem ele, pode funcionar por um tempo e ser bloqueado depois. Este kit não usa esse caminho: é sempre um aplicativo, um usuário do sistema e um token por BM de cliente.

Explica isso ao gestor em poucas linhas antes de começar.

## Antes de criar qualquer coisa

Pergunta:

1. A conta de anúncios do cliente pertence a qual BM? (Na BM, em contas, contas de anúncios, aparece quem é o dono.)
2. Tu é administrador dessa BM? Se não for, há dois caminhos: o cliente te coloca como administrador, ou o cliente faz os passos com vocês dois em chamada. Escreve pro gestor uma mensagem pronta pra mandar ao cliente explicando o que é e por quê.
3. Quantos administradores humanos essa BM tem? Com um só, se o perfil dele cair, ninguém entra. Recomenda ter pelo menos dois (o cliente e o gestor) e explica o risco.
4. Essa BM já tem algum usuário do sistema ou aplicativo? Com acesso padrão, a BM comporta um usuário do sistema comum e um administrador. Se já existirem, reaproveita em vez de tentar criar outro.

## Passo 1: criar o aplicativo na BM do cliente

1. Entrar em developers.facebook.com com um perfil que seja administrador da BM do cliente.
2. Meus aplicativos, criar aplicativo.
3. Escolher o caso de uso ligado a anúncios e API de Marketing. Se a tela pedir tipo, escolher empresa (business).
4. Nome que identifique o cliente, por exemplo "Cockpit [nome do cliente]".
5. **Vincular à BM do cliente**, a dona da conta de anúncios. Esse é o ponto que não pode errar.

**Confere:** ele vê o painel do aplicativo, e em configurações aparece a BM do cliente como empresa vinculada.

## Passo 2: completar o cadastro do aplicativo

É o passo que mais gente pula. Com o cadastro incompleto, a leitura funciona mas criar conjunto e anúncio é recusado com um erro que parece de permissão.

Em configurações básicas do aplicativo, preencher:

- ícone do aplicativo (imagem quadrada, 1024 por 1024);
- endereço da política de privacidade (pode ser a do site do cliente ou da agência);
- categoria do aplicativo.

**Confere:** os três campos estão salvos, sem aviso de pendência.

## Passo 3: adicionar a API de Marketing

No painel do aplicativo, adicionar produto, API de Marketing, configurar. Se o caso de uso do passo 1 já incluiu, ela já está lá.

**Confere:** "API de Marketing" aparece no menu do aplicativo.

## Passo 4: criar o usuário do sistema

1. Entrar em business.facebook.com/settings e conferir, no topo, que está na **BM do cliente**.
2. Usuários, usuários do sistema, adicionar.
3. Nome "Claude Code". Função: comum (funcionário) já basta, porque ele só precisa enxergar os ativos que tu atribuir. Usa administrador só se a vaga de usuário comum já estiver ocupada.

**Confere:** o usuário do sistema aparece na lista.

## Passo 5: dar os ativos ao usuário do sistema

É o passo esquecido. Sem ele o token nasce válido e não enxerga nada.

No usuário do sistema criado, atribuir ativos:

- **aplicativo** do passo 1, com controle total;
- **conta de anúncios** do cliente, com controle total;
- **página** e **conta do Instagram**, se for subir anúncio por aqui;
- **pixel** (conjunto de dados), se for criar conjunto otimizado pra evento.

**Confere:** os ativos aparecem listados dentro do usuário do sistema.

## Passo 6: gerar o token

1. No usuário do sistema, gerar novo token e escolher o aplicativo do passo 1.
2. Validade: a Meta oferece 60 dias ou nunca expira. Token que não expira é mais prático e exige mais cuidado com o arquivo onde fica. Token de 60 dias é mais seguro e precisa ser renovado. Explica os dois e deixa o gestor escolher. Se escolher 60 dias, anota a data de vencimento na ficha do cliente.
3. Permissões: `ads_management`, `ads_read` e `business_management`. Só essas.
4. Gerar. **O token aparece uma vez só.**

Antes dele clicar em gerar, avisa que o token aparece uma vez e combina que ele vai colar direto no arquivo `.env`.

## Passo 7: guardar o token

O token vai no arquivo `.env`, na raiz do kit. Se o arquivo não existe, copia de `.env.example`.

Como cada cliente tem o próprio token, o nome segue o cliente:

```
META_TOKEN_NOMEDOCLIENTE=...
```

Usa o mesmo nome curto da pasta do cliente, em maiúsculas. Orienta o gestor a abrir o `.env` no editor e colar ele mesmo. Não ecoa o token na conversa.

**Confere:** `python3 scripts/meta.py --cliente nomedocliente testar` responde com `token_ok: true` e lista a conta de anúncios do cliente.

Anota na ficha do cliente qual token ele usa. Todo comando desse cliente leva `--cliente nomedocliente`.

## Limite de chamadas

No acesso padrão o limite é baixo: na casa de algumas centenas de chamadas por hora por conta, crescendo conforme o número de anúncios ativos. Pra rotina normal sobra. Estoura quando alguém roda a mesma consulta em laço ou muitas análises seguidas.

- Puxa o que precisa em poucas chamadas grandes, não em muitas pequenas.
- Erro de limite: para, avisa o gestor e espera. Insistir pode bloquear o token.
- Se bloquear ("acesso à API bloqueado"), o gestor gera um token novo no passo 6.

## Se travar

| O que aparece | Causa provável | O que fazer |
|---|---|---|
| Token ok, mas nenhuma conta na lista | A conta não foi atribuída ao usuário do sistema | Refazer o passo 5 |
| Não consigo escolher o aplicativo ao gerar o token | O aplicativo está em outra BM, ou não foi atribuído ao usuário do sistema | Conferir o vínculo no passo 1 e a atribuição no passo 5 |
| Não deixa criar usuário do sistema | A BM já usou as vagas do acesso padrão | Reaproveitar o usuário do sistema que já existe: atribuir os ativos a ele e gerar o token nele |
| Lê tudo, mas criar conjunto ou anúncio dá "objeto não existe ou falta permissão" | Cadastro do aplicativo incompleto, ou página, Instagram ou pixel não atribuídos | Refazer o passo 2 e conferir o passo 5 |
| "Acesso à API bloqueado" ou erro de limite de chamadas | Muitas chamadas seguidas | Parar. Esperar algumas horas. Se continuar, gerar outro token |
| Token inválido de um dia pro outro | Foi gerado token de usuário comum, que expira, ou o token de 60 dias venceu | Refazer o passo 6 |
| A conta de anúncios não aparece pra atribuir | Ela pertence a outra BM, e esta só tem acesso de parceiro | Fazer o setup na BM que é dona da conta |

## Cliente seguinte

Repete os passos 1 a 7 na BM do próximo cliente, com outro nome de token. Com a prática leva poucos minutos.
