"""
Cadastro de Pacientes — Versão Gradio (execução local)
Atividade Prática Aula 1 — Interfaces Web/Mobile para Coleta de Dados

Executar:
    pip install -r requirements.txt
    python app.py
Abrir no navegador: http://127.0.0.1:7860
(Para testar no celular na mesma rede Wi-Fi: python app.py --rede
 e acessar http://<IP-do-computador>:7860)
"""

import os
import sys
from datetime import datetime

import gradio as gr
import pandas as pd

# CSV salvo na mesma pasta do app, independentemente de onde ele é executado
ARQUIVO_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pacientes.csv")
COLUNAS = ["timestamp", "nome", "idade", "convenio", "prioridade", "motivo"]
CONVENIOS = ["Particular", "Unimed", "Bradesco Saúde", "SulAmérica", "Outro"]


def carregar_ultimos(n: int = 5) -> pd.DataFrame:
    """Lê o CSV e devolve os n últimos cadastros (ou uma tabela vazia)."""
    if os.path.exists(ARQUIVO_CSV):
        return pd.read_csv(ARQUIVO_CSV).tail(n)
    return pd.DataFrame(columns=COLUNAS)


def cadastrar_paciente(nome, idade, convenio, prioridade, motivo):
    """Valida os dados, grava uma nova linha no CSV e devolve status + tabela."""
    nome = (nome or "").strip()

    # --- validações simples ---
    if not nome:
        return "⚠️ Informe o nome do paciente.", carregar_ultimos(), *_manter()
    if idade is None or not (0 <= idade <= 120):
        return "⚠️ Informe uma idade válida (0 a 120).", carregar_ultimos(), *_manter()
    if not convenio:
        return "⚠️ Selecione o convênio.", carregar_ultimos(), *_manter()

    linha = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nome": nome,
        "idade": int(idade),
        "convenio": convenio,
        "prioridade": int(prioridade),
        "motivo": (motivo or "").strip(),
    }
    novo = pd.DataFrame([linha], columns=COLUNAS)

    # Cria o arquivo com cabeçalho na primeira execução; depois só acrescenta
    if os.path.exists(ARQUIVO_CSV):
        novo.to_csv(ARQUIVO_CSV, mode="a", header=False, index=False, encoding="utf-8")
    else:
        novo.to_csv(ARQUIVO_CSV, mode="w", header=True, index=False, encoding="utf-8")

    msg = f"✅ Paciente {nome} cadastrado com sucesso! ({linha['timestamp']})"
    # Limpa o formulário para o próximo paciente
    return msg, carregar_ultimos(), "", None, None, 1, ""


def _manter():
    """Em caso de erro, mantém os valores digitados no formulário."""
    return (gr.update(),) * 5


with gr.Blocks(title="Cadastro de Pacientes") as demo:
    gr.Markdown("## 🏥 Cadastro de Pacientes\nRecepção do consultório — preencha e clique em **Cadastrar**.")

    # Layout em coluna única (amigável para celular)
    with gr.Column():
        nome = gr.Textbox(label="Nome do paciente", placeholder="Ex.: Maria da Silva")
        idade = gr.Number(label="Idade", minimum=0, maximum=120, precision=0)
        convenio = gr.Dropdown(CONVENIOS, label="Convênio", value=None)
        prioridade = gr.Slider(1, 5, step=1, value=1,
                               label="Prioridade do atendimento (5 = urgente)")
        motivo = gr.Textbox(label="Motivo da consulta / observações", lines=3)
        botao = gr.Button("Cadastrar", variant="primary")

        saida_msg = gr.Textbox(label="Status", interactive=False)
        tabela = gr.Dataframe(value=carregar_ultimos(), label="Últimos pacientes cadastrados",
                              interactive=False, wrap=True)

    botao.click(
        cadastrar_paciente,
        inputs=[nome, idade, convenio, prioridade, motivo],
        outputs=[saida_msg, tabela, nome, idade, convenio, prioridade, motivo],
    )
    # Atualiza a tabela sempre que a página é aberta
    demo.load(carregar_ultimos, outputs=tabela)


if __name__ == "__main__":
    # "--rede" libera o acesso por outros dispositivos da mesma rede (ex.: celular)
    host = "0.0.0.0" if "--rede" in sys.argv else "127.0.0.1"
    demo.launch(server_name=host, server_port=7860)
