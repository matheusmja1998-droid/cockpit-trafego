---
name: cockpit-setup
description: Conduz o setup do Cockpit Tráfego do zero, passo a passo, e ensina o gestor a usar. Use quando o gestor disser "começa o setup", "continua o setup", "instala o cockpit", "configura o cockpit", arrastar o PDF do Cockpit Tráfego, ou quando o arquivo .cockpit/progresso.md não existir ou estiver incompleto.
---

# Setup do Cockpit Tráfego

Tu conduz. O gestor acompanha, clica onde só ele pode clicar e aprende no caminho. No fim ele tem a Meta conectada, o primeiro cliente cadastrado com ficha e régua, e o primeiro relatório rodado.

## Como conduzir

- **Uma etapa por vez.** Não adianta a próxima antes do teste da atual passar.
- **Cada etapa tem um teste objetivo.** Só marca como feita depois de rodar o teste e ver o resultado.
- **Salva o progresso.** Depois de cada etapa, atualiza `.cockpit/progresso.md` com a etapa, a data e o resultado do teste. Se o gestor voltar outro dia, lê esse arquivo e continua de onde parou, sem repetir.
- **Ensina no fim de cada etapa.** Duas ou três linhas: o que foi feito e por quê. Depois pede pra ele repetir um pedido simples sozinho.
- **Travou?** Lê a parte "Se travar" do arquivo de método da etapa. Se não resolver, descreve o erro em português simples e diz o que ele precisa conferir. Não inventa solução.
- **Tela da Meta muda.** Os nomes dos menus em `metodo/conexao-meta.md` podem estar diferentes. Descreve o objetivo de cada passo, não só o nome do botão.

## Antes de começar

Confere em silêncio e só fala se algo faltar:

1. `python3 --version` responde (3.8 ou mais novo). No Windows pode ser `python` ou `py`. Se não tiver, orienta a instalar pelo python.org e marcar a opção de adicionar ao PATH.
2. Estamos na raiz do kit (existe `scripts/meta.py` e `metodo/`).
3. Existe `.cockpit/progresso.md`? Se sim, continua da etapa pendente.

Depois abre com uma mensagem curta: o que vai acontecer, quantas etapas são e que ele pode parar e voltar quando quiser.

## Etapas

### 1. Conhecer o gestor

Pergunta, uma de cada vez:

1. Como te chamo? Qual o nome da agência ou operação?
2. Quantos clientes de tráfego tu atende hoje?
3. Que tipos de negócio? (lançamento, perpétuo, negócio local, e-commerce)
4. Qual cliente a gente configura primeiro? De preferência um com campanha rodando agora.
5. A conta de anúncios desse cliente fica em qual BM (portfólio empresarial)? Tu é administrador dela, ou o cliente vai precisar fazer os cliques junto contigo?

Grava as respostas em `.cockpit/gestor.md`.

**Teste:** o arquivo existe com as cinco respostas.

### 2. Conectar a Meta

Segue `metodo/conexao-meta.md` do começo ao fim. É a etapa mais longa e a que mais trava. Avisa isso antes de começar. Ela é feita uma vez por cliente, dentro da BM do cliente, e fica bem mais rápida da segunda vez.

O token vai direto pro `.env`. Não pede pra colar no chat se houver outro jeito: orienta ele a abrir o `.env` e colar lá. Se ele colar no chat mesmo assim, grava no `.env`, não repete o token de volta e avisa que é melhor não fazer isso de novo.

**Teste:** `python3 scripts/meta.py --cliente <nome> testar` lista a conta de anúncios do primeiro cliente.

### 3. Cadastrar o primeiro cliente

Segue `metodo/cliente-novo.md`. Ele cobre: escolher o modelo de negócio, entrevistar pra ficha, conferir nomes de campanha e links, e montar a régua.

A régua sai dos números do próprio gestor e do histórico da conta. Não sugere meta nem teto de cabeça.

**Teste:** existem `clientes/<nome>/CLAUDE.md` e `clientes/<nome>/regua.md` sem campo em branco marcado como obrigatório, e o gestor leu e aprovou os dois.

### 4. Primeiro relatório

Roda o relatório do dia do cliente seguindo `metodo/rotina.md`. Mostra o resultado e explica como ler cada bloco.

Depois pede pra ele mesmo digitar: "como tá o [cliente] hoje?". Mostra que é só isso.

**Teste:** o relatório saiu com dado real da conta e o gestor confirmou que os números batem com o Gerenciador.

Se não baterem, não segue. Descobre a diferença (evento errado na ficha, janela de atribuição, fuso da conta) e corrige a ficha.

### 5. Primeira análise de criativo

Roda a análise de criativo com curva dia a dia, de `metodo/rotina.md`, na campanha principal do cliente. Se a régua indicar alguma ação, mostra a sugestão com a regra e o risco, mas **não executa nesta etapa** a menos que o gestor peça. O objetivo aqui é ele ver como a sugestão chega.

**Teste:** a análise saiu e o gestor disse se concorda ou não com a leitura. Se discordar, pergunta o motivo e oferece salvar como regra.

### 6. Ensinar o Claude

Mostra na prática como funciona o aprendizado: pede pra ele dar uma correção real ("nessa conta eu nunca...", "prefiro ver...") e grava na ficha ou na régua, com data e motivo. Abre o arquivo e mostra a linha.

**Teste:** existe ao menos uma regra salva pelo gestor.

### 7. Fechamento

Entrega um resumo curto:

- o que ficou configurado;
- os cinco pedidos que ele mais vai usar (relatório do dia, análise de criativo, cliente novo, pausar ou mexer em orçamento, subir anúncio);
- como cadastrar o próximo cliente: "cadastra um cliente novo";
- lembrete: nada muda na conta sem o "pode" dele.

Marca o setup como concluído em `.cockpit/progresso.md`.

## Formato do progresso

```markdown
# Progresso do setup

- [x] 1. Conhecer o gestor (AAAA-MM-DD)
- [x] 2. Conectar a Meta (AAAA-MM-DD) · teste: 3 contas visíveis
- [ ] 3. Cadastrar o primeiro cliente
...

## Anotações
(o que travou, o que ficou pendente com o gestor)
```
