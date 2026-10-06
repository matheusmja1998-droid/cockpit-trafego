#!/usr/bin/env python3
"""
Cockpit Tráfego: acesso à Meta Marketing API.

Sem dependências (só Python 3). Lê o token do arquivo .env na raiz do kit.
Leitura é livre. Qualquer comando que muda algo na conta só executa com --confirmar;
sem a flag ele só mostra o que faria. Excluir não existe aqui de propósito.

Uso rápido:
  python3 scripts/meta.py testar
  python3 scripts/meta.py contas
  python3 scripts/meta.py campanhas --conta act_123 --tag "[BLACK]" --ativas
  python3 scripts/meta.py insights --conta act_123 --nivel ad --desde 2026-01-10 --ate 2026-01-12 --por-dia
  python3 scripts/meta.py pausar --id 1234567890 --confirmar
  python3 scripts/meta.py orcamento --id 1234567890 --diario 250 --confirmar
  python3 scripts/meta.py api GET act_123/customaudiences --params '{"fields":"name,delivery_status"}'
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, timedelta
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BASE = "https://graph.facebook.com"
# A Meta aposenta versões antigas da API. Se esta ficar velha, o script lê a versão nova
# na mensagem de erro e segue. Pra fixar outra, use META_API_VERSION no .env.
VERSAO_PADRAO = "v25.0"
CODIGO_VERSAO_ANTIGA = 2635
# Códigos de limite de chamadas da Meta. Nesses casos espera e tenta de novo, poucas vezes.
CODIGOS_LIMITE = {4, 17, 32, 613, 80000, 80004}
ESPERA_LIMITE = 60
MAX_PAGINAS = 20

CAMPOS_CAMPANHA = "name,status,effective_status,objective,daily_budget,lifetime_budget,bid_strategy"
CAMPOS_INSIGHTS = (
    "campaign_id,campaign_name,adset_id,adset_name,ad_id,ad_name,"
    "spend,impressions,cpm,frequency,inline_link_clicks,inline_link_click_ctr,"
    "cost_per_inline_link_click,actions"
)


def carregar_env():
    env = RAIZ / ".env"
    if not env.exists():
        return
    for linha in env.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#") or "=" not in linha:
            continue
        chave, valor = linha.split("=", 1)
        os.environ.setdefault(chave.strip(), valor.strip().strip('"').strip("'"))


def sair(mensagem, detalhe=None):
    saida = {"erro": mensagem}
    if detalhe:
        saida["detalhe"] = detalhe
    print(json.dumps(saida, ensure_ascii=False, indent=2), file=sys.stderr)
    sys.exit(1)


def pegar_token(cliente=None):
    """Token do cliente (META_TOKEN_<CLIENTE>) se existir, senão o geral (META_TOKEN)."""
    chaves = []
    if cliente:
        chaves.append("META_TOKEN_" + re.sub(r"[^A-Z0-9]+", "_", cliente.upper()).strip("_"))
    chaves.append("META_TOKEN")
    for chave in chaves:
        valor = os.environ.get(chave, "").strip()
        if valor:
            return valor
    sair(
        "Token da Meta não encontrado.",
        f"Esperava {' ou '.join(chaves)} no arquivo .env da raiz do kit. Veja metodo/conexao-meta.md.",
    )


def normalizar_conta(conta):
    conta = conta.strip()
    return conta if conta.startswith("act_") else f"act_{conta}"


def montar_url(caminho):
    versao = os.environ.get("META_API_VERSION", "").strip().strip("/") or VERSAO_PADRAO
    return "/".join([BASE, versao, caminho.strip("/")])


def codificar(params):
    limpo = {}
    for chave, valor in (params or {}).items():
        if valor is None:
            continue
        limpo[chave] = json.dumps(valor, ensure_ascii=False) if isinstance(valor, (dict, list)) else valor
    return urllib.parse.urlencode(limpo)


def requisitar(metodo, url, token, corpo=None):
    """Uma chamada HTTP com repetição só em erro de limite. O token vai no cabeçalho, nunca na URL."""
    for tentativa in range(3):
        req = urllib.request.Request(url, data=corpo, method=metodo)
        req.add_header("Authorization", f"Bearer {token}")
        try:
            with urllib.request.urlopen(req, timeout=90) as resposta:
                return json.loads(resposta.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            bruto = e.read().decode("utf-8", "replace")
            try:
                erro = json.loads(bruto).get("error", {})
            except ValueError:
                erro = {"message": bruto[:500]}
            nova = re.search(r"latest version: (v\d+\.\d+)", erro.get("message", ""))
            if erro.get("code") == CODIGO_VERSAO_ANTIGA and nova and tentativa < 2:
                print(f"A Meta aposentou a versão em uso. Seguindo com {nova.group(1)}. "
                      f"Grave META_API_VERSION={nova.group(1)} no .env.", file=sys.stderr)
                os.environ["META_API_VERSION"] = nova.group(1)
                url = re.sub(r"graph\.facebook\.com/v\d+\.\d+", f"graph.facebook.com/{nova.group(1)}", url)
                continue
            if erro.get("code") in CODIGOS_LIMITE and tentativa < 2:
                print(
                    f"Limite de chamadas da Meta (código {erro.get('code')}). "
                    f"Esperando {ESPERA_LIMITE}s antes de tentar de novo.",
                    file=sys.stderr,
                )
                time.sleep(ESPERA_LIMITE)
                continue
            sair("A Meta recusou a chamada.", erro)
        except urllib.error.URLError as e:
            sair("Sem conexão com a Meta.", str(e.reason))


def ler(caminho, params, token):
    """GET com paginação. Devolve a lista completa quando a resposta tem 'data'."""
    url = montar_url(caminho) + "?" + codificar(params)
    resposta = requisitar("GET", url, token)
    if not isinstance(resposta.get("data"), list):
        return resposta
    itens = list(resposta["data"])
    paginas = 1
    while resposta.get("paging", {}).get("next") and paginas < MAX_PAGINAS:
        # O link de próxima página vem com o token na URL; tira antes de usar.
        proxima = re.sub(r"([?&])access_token=[^&]*&?", r"\1", resposta["paging"]["next"]).rstrip("?&")
        resposta = requisitar("GET", proxima, token)
        itens.extend(resposta.get("data", []))
        paginas += 1
    return itens


def escrever(caminho, params, token, confirmar):
    """POST. Sem --confirmar só mostra o que seria enviado."""
    if not confirmar:
        return {
            "simulacao": True,
            "o_que_faria": {"metodo": "POST", "caminho": caminho, "dados": params},
            "como_executar": "Mostre isso ao gestor. Com o 'pode' dele, rode de novo com --confirmar.",
        }
    resposta = requisitar("POST", montar_url(caminho), token, corpo=codificar(params).encode("utf-8"))
    return {"executado": True, "caminho": caminho, "dados": params, "resposta": resposta}


def imprimir(dados):
    print(json.dumps(dados, ensure_ascii=False, indent=2))


def dia(texto):
    if texto in (None, "ontem"):
        return (date.today() - timedelta(days=1)).isoformat()
    if texto == "hoje":
        return date.today().isoformat()
    try:
        return date.fromisoformat(texto).isoformat()
    except ValueError:
        sair(f"Data inválida: {texto}", "Use AAAA-MM-DD, 'hoje' ou 'ontem'.")


def numero(valor):
    try:
        return float(valor)
    except (TypeError, ValueError):
        return 0.0


# ---------- comandos ----------

def cmd_testar(args, token):
    quem = ler("me", {"fields": "id,name"}, token)
    contas = ler("me/adaccounts", {"fields": "name,account_id,account_status,currency", "limit": 200}, token)
    imprimir({
        "token_ok": True,
        "identidade": quem,
        "contas_visiveis": len(contas),
        "contas": contas,
        "leitura": "Se a conta do cliente não está na lista, a conta de anúncios não foi atribuída "
                   "ao usuário do sistema. Veja 'Se travar' em metodo/conexao-meta.md.",
    })


def cmd_contas(args, token):
    imprimir(ler("me/adaccounts", {
        "fields": "name,account_id,account_status,currency,timezone_name,amount_spent",
        "limit": 200,
    }, token))


def cmd_campanhas(args, token):
    params = {"fields": CAMPOS_CAMPANHA, "limit": 200}
    filtros = []
    if args.tag:
        filtros.append({"field": "name", "operator": "CONTAIN", "value": args.tag})
    if args.ativas:
        filtros.append({"field": "effective_status", "operator": "IN", "value": ["ACTIVE"]})
    if filtros:
        params["filtering"] = filtros
    campanhas = ler(f"{normalizar_conta(args.conta)}/campaigns", params, token)
    for c in campanhas:
        for campo in ("daily_budget", "lifetime_budget"):
            if c.get(campo):
                c[campo.replace("_budget", "_orcamento")] = numero(c[campo]) / 100
    imprimir(campanhas)


def cmd_insights(args, token):
    desde, ate = dia(args.desde), dia(args.ate or args.desde)
    params = {
        "level": args.nivel,
        "fields": CAMPOS_INSIGHTS,
        "time_range": {"since": desde, "until": ate},
        "limit": 500,
    }
    if args.por_dia:
        params["time_increment"] = 1
    if args.tag:
        params["filtering"] = [{"field": "campaign.name", "operator": "CONTAIN", "value": args.tag}]
    linhas = ler(f"{normalizar_conta(args.conta)}/insights", params, token)
    saida = []
    for l in linhas:
        resultados = {a["action_type"]: numero(a["value"]) for a in l.get("actions", [])}
        saida.append({
            "dia": l.get("date_start") if args.por_dia else f"{l.get('date_start')} a {l.get('date_stop')}",
            "campanha": l.get("campaign_name"),
            "conjunto": l.get("adset_name") if args.nivel in ("adset", "ad") else None,
            "anuncio": l.get("ad_name") if args.nivel == "ad" else None,
            "id": l.get({"campaign": "campaign_id", "adset": "adset_id", "ad": "ad_id"}[args.nivel]),
            "gasto": numero(l.get("spend")),
            "impressoes": int(numero(l.get("impressions"))),
            "cpm": round(numero(l.get("cpm")), 2),
            "frequencia": round(numero(l.get("frequency")), 2),
            "cliques_link": int(numero(l.get("inline_link_clicks"))),
            "ctr_link": round(numero(l.get("inline_link_click_ctr")), 2),
            "custo_clique_link": round(numero(l.get("cost_per_inline_link_click")), 2),
            "visitas_pagina": int(resultados.get("landing_page_view", 0)),
            "resultados": resultados,
        })
    imprimir({
        "periodo": {"desde": desde, "ate": ate, "por_dia": bool(args.por_dia)},
        "nivel": args.nivel,
        "linhas": saida,
        "leitura": "Em 'resultados' use UM tipo de evento só, o que está na ficha do cliente. "
                   "Somar dois eventos parecidos conta o mesmo resultado duas vezes.",
    })


def cmd_status(args, token, novo):
    atual = ler(args.id, {"fields": "name,status,effective_status"}, token)
    resultado = escrever(args.id, {"status": novo}, token, args.confirmar)
    resultado["objeto"] = atual
    imprimir(resultado)


def cmd_orcamento(args, token):
    if args.diario <= 0:
        sair("Orçamento precisa ser maior que zero.")
    atual = ler(args.id, {"fields": "name,daily_budget,effective_status"}, token)
    antes = numero(atual.get("daily_budget")) / 100
    resultado = escrever(args.id, {"daily_budget": int(round(args.diario * 100))}, token, args.confirmar)
    resultado["objeto"] = atual.get("name")
    resultado["orcamento_diario_antes"] = antes
    resultado["orcamento_diario_depois"] = args.diario
    if antes:
        resultado["variacao_pct"] = round((args.diario / antes - 1) * 100, 1)
    imprimir(resultado)


def cmd_api(args, token):
    params = {}
    if args.arquivo:
        params = json.loads(Path(args.arquivo).read_text(encoding="utf-8"))
    elif args.params:
        try:
            params = json.loads(args.params)
        except ValueError:
            sair("--params precisa ser um JSON válido.")
    metodo = args.metodo.upper()
    if metodo == "GET":
        imprimir(ler(args.caminho, params, token))
    elif metodo == "POST":
        imprimir(escrever(args.caminho, params, token, args.confirmar))
    else:
        sair("Só GET e POST. Excluir fica de fora de propósito: pausar resolve e dá pra desfazer.")


def main():
    carregar_env()
    p = argparse.ArgumentParser(description="Cockpit Tráfego: Meta Marketing API")
    p.add_argument("--cliente", help="Usa META_TOKEN_<CLIENTE> do .env em vez do token geral")
    sub = p.add_subparsers(dest="comando", required=True)

    sub.add_parser("testar", help="Confere o token e lista as contas que ele enxerga")
    sub.add_parser("contas", help="Lista as contas de anúncio")

    c = sub.add_parser("campanhas", help="Lista campanhas de uma conta")
    c.add_argument("--conta", required=True)
    c.add_argument("--tag", help="Só campanhas com esse texto no nome")
    c.add_argument("--ativas", action="store_true")

    i = sub.add_parser("insights", help="Números por campanha, conjunto ou anúncio")
    i.add_argument("--conta", required=True)
    i.add_argument("--nivel", choices=["campaign", "adset", "ad"], default="campaign")
    i.add_argument("--desde", default="ontem", help="AAAA-MM-DD, 'hoje' ou 'ontem'")
    i.add_argument("--ate", help="Padrão: igual a --desde")
    i.add_argument("--por-dia", action="store_true", help="Uma linha por dia, pra ver a curva")
    i.add_argument("--tag", help="Só campanhas com esse texto no nome")

    for nome, ajuda in (("pausar", "Pausa campanha, conjunto ou anúncio"),
                        ("ativar", "Ativa campanha, conjunto ou anúncio")):
        s = sub.add_parser(nome, help=ajuda)
        s.add_argument("--id", required=True)
        s.add_argument("--confirmar", action="store_true")

    o = sub.add_parser("orcamento", help="Muda o orçamento diário de campanha ou conjunto")
    o.add_argument("--id", required=True)
    o.add_argument("--diario", type=float, required=True, help="Valor em moeda da conta, ex: 250 ou 250.50")
    o.add_argument("--confirmar", action="store_true")

    a = sub.add_parser("api", help="Chamada direta pra qualquer ponto da API (GET livre, POST com --confirmar)")
    a.add_argument("metodo")
    a.add_argument("caminho")
    a.add_argument("--params", help="JSON com os parâmetros")
    a.add_argument("--arquivo", help="Arquivo JSON com os parâmetros")
    a.add_argument("--confirmar", action="store_true")

    args = p.parse_args()
    token = pegar_token(args.cliente)
    {
        "testar": cmd_testar,
        "contas": cmd_contas,
        "campanhas": cmd_campanhas,
        "insights": cmd_insights,
        "pausar": lambda a, t: cmd_status(a, t, "PAUSED"),
        "ativar": lambda a, t: cmd_status(a, t, "ACTIVE"),
        "orcamento": cmd_orcamento,
        "api": cmd_api,
    }[args.comando](args, token)


if __name__ == "__main__":
    main()
