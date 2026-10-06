# Cockpit Tráfego

Kit pra gerir tráfego pago com o Claude Code. O Claude lê as contas de anúncio, monta o relatório do dia, analisa criativo, sugere otimização pela régua de cada cliente e executa o que tu aprovar.

## Como começar

1. Abre esta pasta no Claude Code.
2. Escreve: **começa o setup**.

O Claude conduz o resto: conecta a Meta, cadastra teu primeiro cliente, monta a régua contigo e roda o primeiro relatório. Dá pra parar e voltar depois; ele continua de onde parou.

## O que tu precisa

- Claude Code com plano pago.
- Python 3 instalado.
- Ser administrador da BM (portfólio empresarial) dona da conta de anúncios do cliente, ou ter o cliente junto pra fazer os cliques. A conexão é feita dentro da BM de cada cliente.

## O que tem aqui

| Pasta | Pra que serve |
|---|---|
| `CLAUDE.md` | As regras que o Claude segue sempre |
| `metodo/` | Como fazer cada coisa: conexão, cliente novo, régua, rotina, subir anúncio |
| `moldes/` | Modelos em branco de ficha e régua |
| `scripts/meta.py` | A ponte com a Meta |
| `clientes/` | Uma pasta por cliente (criada no setup, fica só na tua máquina) |

## Segurança

- O token fica só no arquivo `.env`, que não vai pro Git.
- Nada muda na tua conta sem tu dizer "pode".
- O kit não exclui campanha, conjunto nem anúncio. Só pausa.
- Tu é responsável pelo que acontece na conta. Confere a prévia no Gerenciador antes de ativar qualquer coisa e respeita as políticas da Meta.

## Pedidos do dia a dia

- "como tá o [cliente] hoje?"
- "analisa os criativos do [cliente]"
- "o que a régua manda fazer no [cliente]?"
- "cadastra um cliente novo"
- "sobe esses criativos na campanha de teste do [cliente]"
