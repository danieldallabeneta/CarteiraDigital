import pandas as pd
import statsmodels.api as sm
import requests

class Services():

    def get_dados_historico(self, user):
        # URL do microserviço que fornece o histórico de gastos
        url = "http://api-gateway/app1/movement/get_all?usuario="+user
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Could not fetch expense data"}

    def generate_projections(self, user):
        history = self.get_dados_historico(user)
        
        if "error" in history:
            return history
        
        if not isinstance(history, list) or len(history) == 0:
            return {"error": "No data available"}
        
        df = pd.DataFrame(history)

        df['valor'] = pd.to_numeric(df['valor'], errors='coerce')  
        df['tipo'] = pd.to_numeric(df['tipo'], errors='coerce')

        df = df.dropna(subset=['valor', 'tipo'])

        df['data'] = pd.to_datetime(df['data'], errors='coerce')
        df = df.dropna(subset=['data'])

        df['valor'] = df.apply(lambda row: row['valor'] if row['tipo'] == 1 else -row['valor'], axis=1)
        
        df['year_month'] = df['data'].dt.to_period('M')
        result = df.groupby('year_month')['valor'].sum().reset_index()
        result.columns = ['date', 'amount']
        result['date'] = result['date'].dt.to_timestamp()
        monthly_expenses = result.set_index('date')['amount']
        
        model = sm.tsa.ARIMA(monthly_expenses, order=(12, 1, 1))  
        model_fit = model.fit()
        
        forecast = model_fit.forecast(steps=12)

        return {
            "monthly_average": monthly_expenses.mean(),
            "projections": forecast.tolist()
        }
