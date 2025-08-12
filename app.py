import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title='Dashboard de Salários na Área de Dados',
    page_icon='📊',
    layout='wide',
)

df = pd.read_csv("dados-imersao-final.csv")

# Barra lateral de filtros
st.sidebar.header('Filtros 🔎')

# Filtro de Ano
anos_disponiveis = sorted(df['ano'].unique())
anos_selecionados = st.sidebar.multiselect('Ano 📅', anos_disponiveis)

# Filtro de Senioridade
senioridades_disponiveis = sorted(df['senioridade'].unique())
senioridades_selecionadas = st.sidebar.multiselect("Senioridade 🧠", senioridades_disponiveis)

# Filtro por Tipo de Contrato
contratos_disponiveis = sorted(df['contrato'].unique())
contratos_selecionados = st.sidebar.multiselect("Tipo de Contrato 📝", contratos_disponiveis)

# Filtro por Tamanho da Empresa
tamanhos_disponiveis = sorted(df['tamanho_empresa'].unique())
tamanhos_selecionados = st.sidebar.multiselect("Tamanho da Empresa 🏭", tamanhos_disponiveis)

# Filtro por País
paises_disponiveis = sorted(df['residencia'].unique())
paises_selecionados = st.sidebar.multiselect('Localização 🗺️', paises_disponiveis)

# Filtro por Cargo
cargos_disponiveis = sorted(df['cargo'].unique())
cargos_selecionados = st.sidebar.multiselect('Cargo 💼', cargos_disponiveis)

# Filtragem aplicada
df_filtrado = df.copy()

if anos_selecionados:
    df_filtrado = df_filtrado[df_filtrado['ano'].isin(anos_selecionados)]

if senioridades_selecionadas:
    df_filtrado = df_filtrado[df_filtrado['senioridade'].isin(senioridades_selecionadas)]

if contratos_selecionados:
    df_filtrado = df_filtrado[df_filtrado['contrato'].isin(contratos_selecionados)]

if tamanhos_selecionados:
    df_filtrado = df_filtrado[df_filtrado['tamanho_empresa'].isin(tamanhos_selecionados)]

if paises_selecionados:
    df_filtrado = df_filtrado[df_filtrado['residencia'].isin(paises_selecionados)]

if cargos_selecionados:
    df_filtrado = df_filtrado[df_filtrado['cargo'].isin(cargos_selecionados)]

# ---
st.title("Dashboard para Análise de Salários na Área de Dados 📑")
st.subheader("Explore os dados salariais na área de dados nos últimos anos.")
st.markdown("Utilize os filtros à esquerda para facilitar sua procura.")

# Métricas
st.subheader("Métricas gerais (Salário anual em USD)")

if not df_filtrado.empty:
    salario_medio = df_filtrado['usd'].mean()
    salario_maximo = df_filtrado['usd'].max()
    total_registros = df_filtrado.shape[0]
    cargo_mais_frequente = df_filtrado["cargo"].mode()[0]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Salário médio", f"${salario_medio:,.0f}")
    col2.metric("Salário máximo", f"${salario_maximo:,.0f}")
    col3.metric("Total de registros", f"{total_registros:,}")
    col4.metric("Cargo mais comum", cargo_mais_frequente)
else:
    st.warning('Nenhum dado para exibir as métricas')

st.markdown("---")

# --- Análises Visuais com Plotly ---
st.subheader("Gráficos")

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    if not df_filtrado.empty:
        top_cargos_salario = df_filtrado.groupby('cargo')['usd'].mean().nlargest(10).sort_values(ascending=True).reset_index()
        grafico_cargos_salario = px.bar(
            top_cargos_salario,
            x='usd',
            y='cargo',
            orientation='h',
            title="Top 10 cargos por salário médio",
            labels={'usd': 'Média salarial anual (USD)', 'cargo': ''}
        )
        grafico_cargos_salario.update_layout(title_x=0.1, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(grafico_cargos_salario, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de cargos.")

with col_graf2:
    if not df_filtrado.empty:
        top_cargos_qntd = df_filtrado['cargo'].value_counts().nlargest(10).sort_values(ascending=True).reset_index()
        top_cargos_qntd.columns = ['cargo', 'quantidade']
        grafico_cargos_qntd = px.bar(
            top_cargos_qntd,
            x='quantidade',
            y='cargo',
            orientation='h',
            title="Top 10 cargos mais populares",
            labels={'quantidade': 'Quantidade', 'cargo': ''}
        )
        grafico_cargos_qntd.update_layout(title_x=0.1, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(grafico_cargos_qntd, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de cargos.")

col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    if not df_filtrado.empty:
        remoto_contagem = df_filtrado['remoto'].value_counts().reset_index()
        remoto_contagem.columns = ['tipo_trabalho', 'quantidade']
        grafico_remoto = px.pie(
            remoto_contagem,
            names='tipo_trabalho',
            values='quantidade',
            title='Proporção dos tipos de trabalho',
            hole=0.5
        )
        grafico_remoto.update_traces(textinfo='percent+label')
        grafico_remoto.update_layout(title_x=0.1)
        st.plotly_chart(grafico_remoto, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico dos tipos de trabalho.")

with col_graf4:
    if not df_filtrado.empty:
        grafico_hist = px.histogram(
            df_filtrado,
            x='usd',
            nbins=30,
            title="Distribuição de salários anuais",
            labels={'usd': 'Faixa salarial (USD)', 'count': ''}
        )
        grafico_hist.update_layout(title_x=0.1)
        st.plotly_chart(grafico_hist, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de distribuição.")

col_graf5, col_graf6 = st.columns(2)

with col_graf5:
    if not df_filtrado.empty:
        media_ds_pais = df_filtrado.groupby('residencia_iso3')['usd'].mean().reset_index()

        grafico_paises_ds = px.choropleth(media_ds_pais,
            locations='residencia_iso3',
            color='usd',
            color_continuous_scale='rdylgn',
            title='Salário médio de cargos por país',
            labels={'usd': 'Salário médio (USD)', 'residencia_iso3': 'País'})
        grafico_paises_ds.update_layout(title_x=0.1)
        st.plotly_chart(grafico_paises_ds, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de países.")

with col_graf6:
    if not df_filtrado.empty:
        qntd_cargo_pais = df_filtrado.groupby(['residencia_iso3', 'cargo']).size().reset_index(name='quantidade')
        top_cargo_por_pais = (
            qntd_cargo_pais.loc[
                qntd_cargo_pais.groupby('residencia_iso3')['quantidade'].idxmax()
            ]
            .reset_index(drop=True)
        )

        grafico_paises_qntd = px.choropleth(top_cargo_por_pais,
            locations='residencia_iso3',
            color='quantidade',
            color_continuous_scale='rdylgn',
            title='Quantidade de cargos por país',
            labels={'quantidade': 'Quantidade', 'cargo': 'Cargo', 'residencia_iso3': 'País'},
            hover_name='cargo')
        grafico_paises_qntd.update_layout(title_x=0.1)
        st.plotly_chart(grafico_paises_qntd, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de países.")


# --- Tabela de Dados Detalhados ---
st.subheader("Dados Detalhados")
st.dataframe(df_filtrado)

st.markdown("---")

st.markdown('Dataset from Kaggle - Usado para fins educativos.')
st.markdown('Desenvolvido por Marcos V C Zanola')