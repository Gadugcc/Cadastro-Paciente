# Cadastro de Pacientes — Gradio x Streamlit

Atividade Prática – Aula 1 (Prof. Francisco Fambrini)
Interfaces Web/Mobile para Coleta de Dados.

A mesma aplicação de cadastro de pacientes de um consultório, feita duas vezes:

| Pasta | Biblioteca | Onde roda | Onde ficam os dados |
|---|---|---|---|
| `gradio_app/` | Gradio (`gr.Blocks`) | Localmente | `gradio_app/pacientes.csv` |
| `streamlit_app/` | Streamlit (`st.form`) | Streamlit Community Cloud | `st.session_state` + botão **Baixar CSV** |

Campos: nome, idade, convênio (Particular, Unimed, Bradesco Saúde, SulAmérica, Outro), prioridade (1–5, 5 = urgente) e motivo da consulta. Cada cadastro grava também a data/hora.

## Links da entrega

- App publicado no Streamlit Cloud: `https://SEU-APP.streamlit.app` ← substituir após o deploy
- Print da versão Gradio: [`print_gradio_desktop.png`](print_gradio_desktop.png) e [`print_gradio_celular.png`](print_gradio_celular.png)
- CSV de exemplo: [`gradio_app/pacientes.csv`](gradio_app/pacientes.csv)

## Como rodar a versão Gradio (local)

```bash
cd gradio_app
pip install -r requirements.txt
python app.py
```

Abra http://127.0.0.1:7860. Para testar no celular na mesma rede Wi-Fi, rode `python app.py --rede` e acesse `http://<IP-do-computador>:7860`.

## Como rodar a versão Streamlit (local)

```bash
cd streamlit_app
pip install -r requirements.txt
streamlit run app.py
```

## Deploy no Streamlit Community Cloud

1. Suba este repositório para o GitHub (público).
2. Acesse https://share.streamlit.io e entre com a conta do GitHub.
3. Clique em **Create app** / **New app** → selecione o repositório, a branch `main` e o arquivo **`streamlit_app/app.py`**.
4. Aguarde o build e teste pelo link `*.streamlit.app` — também pelo celular.

> O sistema de arquivos do Streamlit Cloud é efêmero: o CSV gravado no servidor some quando o app reinicia. Por isso a recepção deve exportar os dados pelo botão **Baixar CSV**.

## Gradio x Streamlit — comparação prática

- **Modelo de execução:** o Gradio liga eventos (botão → função → saídas); o Streamlit re-executa o script inteiro a cada interação, por isso precisa de `st.session_state` para guardar os dados entre execuções.
- **Formulário:** no Gradio é preciso devolver valores vazios para limpar os campos; no Streamlit basta `st.form(clear_on_submit=True)`.
- **Layout/celular:** os dois ficam responsivos em coluna única; a tabela do Gradio rola horizontalmente no celular.
- **Publicação:** o Streamlit tem deploy gratuito direto do GitHub (Community Cloud); o Gradio costuma ser publicado no Hugging Face Spaces ou com `share=True` (link temporário de 72 h).
- **Persistência:** localmente ambos gravam o CSV; na nuvem gratuita o disco é temporário, então é necessário exportar (download) ou usar um banco/planilha externa.
