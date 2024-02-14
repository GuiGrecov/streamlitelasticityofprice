import pandas as pd
import datetime as dt
import streamlit as st

df_order_elasticity = pd.read_csv("order.csv")
x_price = pd.read_csv("x_price.csv")
y_demand = pd.read_csv("y_demand.csv")
df_cross = pd.read_csv("teste.csv")

st.set_page_config( page_title="ELASTICIDADE DE PREÇO", layout="wide")

st.title("ELASTICIDADE DE PREÇO")
st.caption("Esse site foi gerado como o projeto final de uma aplicação que tem como estudo analisar a elasticidade de preço. Razão em que variamos o preço e a demanda de um produto")

tab1, tab2, tab3 = st.tabs(["SIMULADOR DE DESCONTO","ELASTICIDADE CRUZADA", "BUSSINES PERFORMANCE" ])

def tratamento(percentual, df_order_elasticity ):
    percentual = percentual/100

    resultado_faturamento = {
        'name': [],
        'faturamento_atual': [],
        'faturamento_redução': [],
        'perda_faturamento': [],
        'faturamento_novo': [],
        'variacao_faturamento': [],
        'variacao_percentual': []
    }

    for i in range(len(df_order_elasticity)):
        preco_atual_medio = x_price[df_order_elasticity['name'][i]].mean()
        demanda_atual = y_demand[df_order_elasticity['name'][i]].sum()

        reducao_preco = preco_atual_medio * (1-percentual)
        aumento_demanda = -percentual * df_order_elasticity['price_elasticity'][i]  # negativo para sumir com o valor da elasticidade negativa

        demanda_nova = aumento_demanda * demanda_atual

        faturamento_atual = round(preco_atual_medio * demanda_atual, 2)
        faturamento_novo = round(reducao_preco * demanda_nova, 2)

        faturamento_reducao = round(faturamento_atual * (1-percentual), 2)

        perda_faturamento = round(faturamento_atual - faturamento_reducao, 2)

        variacao_faturamento = round(faturamento_novo - faturamento_atual, 2)

        variacao_percentual = round(((faturamento_novo - faturamento_atual) / faturamento_atual), 2)

        resultado_faturamento['name'].append(df_order_elasticity['name'][i])
        resultado_faturamento['faturamento_atual'].append(faturamento_atual)
        resultado_faturamento['faturamento_redução'].append(faturamento_reducao)
        resultado_faturamento['perda_faturamento'].append(perda_faturamento)
        resultado_faturamento['faturamento_novo'].append(faturamento_novo)
        resultado_faturamento['variacao_faturamento'].append(variacao_faturamento)
        resultado_faturamento['variacao_percentual'].append(variacao_percentual)

    resultado = pd.DataFrame(resultado_faturamento)
    return resultado

with tab1:
    with st.container():
        st.markdown('## SIMULADOR DOS PRODUTOS SELECIONADOS (DIGITE UMA PORCETAGEM)')
        percentual = st.number_input("Digite um Desconto:", min_value=0.0, max_value=11.0, step=0.1)
        st.text(f"Tabela seguindos o desconto informado de {percentual}")
        df = tratamento(percentual, df_order_elasticity )
        st.dataframe(df)
        total =  df["variacao_faturamento"].sum()


        st.text(f"Somatória do novo faturamento seguindo o desconto projetado é de R$ {total}")

        negativo = df[df["variacao_percentual"] < 0]

        #SOMATÓRIA NEGATIVA
        if len(negativo) > 0:
            st.markdown('## VALORES NEGATIVOS (PERCENTUAIS NEGATIVOS)')
            st.text(f"Esses foram os produtos que não existe compensação financeiro")

            deficit =  negativo["variacao_faturamento"].sum()

            st.dataframe(negativo)

            st.text(f"Somatória do prejuízo é de R$ {deficit}")
            st.text(f"Recomendado não executar o descontos nesses produtos")

        else:
            print("")

        #SOMATÓRIA POSITIVA
        positivo = df[df["variacao_percentual"] > 0]

        if len(positivo) > 0:
            st.markdown('## VALORES POSITIVOS (PERCENTUAIS POSITIVOS)')
            st.text(
                f"Esses foram os produtos que não existe compensação financeira aplicando os desconto selecionado.")

            saving = positivo["variacao_faturamento"].sum()

            st.dataframe(positivo)

            st.text(f"Somatória do lucro (variação do faturamento) é de R$ {saving}")


        else:
            print("")

with tab2:
    #ELASTICIDADE CRUZADA
    st.header("ELASTICIDADE CRUZADA")

    st.text("Nessa parte vamos analisar a performance do código.")

    st.text("""
            1. Elasticidade de preço cruzada positiva: \n Isso ocorre quando a quantidade demandada de um produto aumenta em resposta a um aumento \n no preço de um produto relacionado. Indica que os dois produtos são substitutos, e um aumento no preço \n de um produto leva os consumidores a buscar o produto alternativo, aumentando sua demanda.
            
2. Elasticidade de preço cruzada negativa: \n Isso ocorre quando a quantidade demandada de um produto diminui em resposta a um aumento no preço \n de um produto relacionado. Indica que os dois produtos são complementares, e um aumento no preço \n de um produto reduz a demanda pelo outro produto.
            
3. Elasticidade de preço cruzada nula (ou próxima de zero): \n Isso ocorre quando não há uma relação significativa entre a variação no preço de um produto e a \n quantidade demandada do outro produto. Indica que não há substitutos ou complementares próximos \n entre os dois produtos""")

    st.dataframe(df_cross)

    st.text("CONCLUSÃO")
    st.text("""Os produtos selecionados e mostrado no Business Peformance não são concorrentes. \nA maioria dos produtos são complementares.  \nSomente no caso do 12 MacBook e Apple MacBook Pro MLUQ2LL/A 13.3. são concorrentes porém aqui\npossivelmente há uma variação do melhor preço para os consumidores  se o modelo normal do Macbook \nestiver mais barato que a versão PRO possivelmente os usuários prefiram comprar o mais barato""")

with tab3:
    #Performance de Negócio
    st.header("BUSINESS PERFORMANCE")

    st.text("Nessa parte vamos analisar a performance dos produtos selecionados")
    df_order_elasticity = df_order_elasticity[["name", "price_elasticity"]]
    st.dataframe(df_order_elasticity)

    st.text("Elasticidade negativa devida a inclinação da reta... Não é alguma proporção de preço inversa")
    st.text("Todos os produtos mostrados acima tem um P valor menor do que 0.05. \nFiltramos durante o estudo de Machine Learning a fim de aumentarmos a assertividade ")
