"""
Cadastro de Pacientes — Versão Streamlit (deploy no Streamlit Community Cloud)
Atividade Prática Aula 1 — Interfaces Web/Mobile para Coleta de Dados

Executar localmente:
    pip install -r requirements.txt
    streamlit run app.py

Observação: no Streamlit Community Cloud o sistema de arquivos é efêmero —
o pacientes.csv gravado no servidor some quando o app reinicia. Por isso os
dados da sessão ficam em st.session_state e podem ser exportados pelo botão
"Baixar CSV".
"""

import os
from datetime import datetime

import pandas as pd
import streamlit as st

ARQUIVO_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pacientes.csv")
COLUNAS = ["timestamp", "nome", "idade", "convenio", "prioridade", "motivo"]
CONVENIOS = ["Particular", "Unimed", "Bradesco Saúde", "SulAmérica", "Outro"]

st.set_page_config(page_title="Cadastro de Pacientes", page_icon="🏥", layout="centered")
st.title("🏥 Cadastro de Pacientes")
st.caption("Recepção do consultório — preencha e clique em **Cadastrar**.")

# Pacientes acumulados durante a sessão
if "pacientes" not in st.session_state:
    st.session_state.pacientes = pd.DataFrame(columns=COLUNAS)


def gravar_csv(linha: dict) -> None:
    """Mesma lógica da versão Gradio: cria com cabeçalho ou acrescenta."""
    novo = pd.DataFrame([linha], columns=COLUNAS)
    existe = os.path.exists(ARQUIVO_CSV)
    novo.to_csv(ARQUIVO_CSV, mode="a" if existe else "w", header=not existe,
                index=False, encoding="utf-8")


with st.form("cadastro", clear_on_submit=True):
    nome = st.text_input("Nome do paciente", placeholder="Ex.: Maria da Silva")
    idade = st.number_input("Idade", min_value=0, max_value=120, step=1)
    convenio = st.selectbox("Convênio", CONVENIOS, index=None,
                            placeholder="Selecione o convênio")
    prioridade = st.slider("Prioridade do atendimento (5 = urgente)", 1, 5, 1)
    motivo = st.text_area("Motivo da consulta / observações")
    enviado = st.form_submit_button("Cadastrar", type="primary", width="stretch")

if enviado:
    if not nome.strip():
        st.warning("⚠️ Informe o nome do paciente.")
    elif convenio is None:
        st.warning("⚠️ Selecione o convênio.")
    else:
        nova_linha = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "nome": nome.strip(),
            "idade": int(idade),
            "convenio": convenio,
            "prioridade": int(prioridade),
            "motivo": motivo.strip(),
        }
        st.session_state.pacientes = pd.concat(
            [st.session_state.pacientes, pd.DataFrame([nova_linha])],
            ignore_index=True,
        )
        try:
            gravar_csv(nova_linha)  # cópia local (efêmera no Cloud)
        except OSError:
            pass
        st.success(f"✅ Paciente {nova_linha['nome']} cadastrado!")

st.subheader("Últimos pacientes cadastrados")
total = len(st.session_state.pacientes)
if total == 0:
    st.info("Nenhum paciente cadastrado nesta sessão ainda.")
else:
    st.dataframe(st.session_state.pacientes.tail(5), hide_index=True, width="stretch")
    st.caption(f"Total nesta sessão: {total}")

csv = st.session_state.pacientes.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Baixar CSV", csv, "pacientes.csv", "text/csv",
                   disabled=(total == 0), width="stretch")
