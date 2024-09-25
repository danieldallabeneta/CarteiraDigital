import pandas as pd
import statsmodels.api as sm
import requests

def get_dados_historico(user):
    # URL do microserviço que fornece o histórico de gastos
    url = "http://localhost/api2/movements/"+user
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json().get('dados', [])
    else:
        return {"error": "Could not fetch expense data"}

def generate_projections(user):
    history = get_dados_historico(user)

    if "error" in history:
        return history
    
    # Transformar o histórico em um DataFrame
    df = pd.DataFrame(history)
    
    # Assumir que o histórico tem uma coluna 'amount' para os gastos
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')

    # Resumir os gastos mensais
    monthly_expenses = df['amount'].resample('M').sum()

    # Treinamento do modelo ARIMA
    model = sm.tsa.ARIMA(monthly_expenses, order=(1, 1, 1))  # ARIMA(1,1,1) como exemplo, pode ser ajustado
    model_fit = model.fit()

    # Fazer a projeção para os próximos 12 meses
    forecast = model_fit.forecast(steps=12)

    return {
        "monthly_average": monthly_expenses.mean(),
        "projections": forecast.tolist()
    }
