import pandas as pd
import statsmodels.api as sm
from wallet.walletServices import WalletServices

wallet_services = WalletServices()

class Services():

    def generate_projections(self, user):
        history = wallet_services.get_dados_historico_user(user)
        
        if "error" in history:
            return history
        
        if not isinstance(history, list) or len(history) == 0:
            return {"error": "Sem histórico de movimentações"}
        
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
    
    def get_data_graph(self, wallet):
        data = wallet_services.get_dados_historico_wallet(wallet)
        if "error" in data:
            return data

        if not isinstance(data, list) or len(data) == 0:
            return {"error": "Sem histórico de movimentações"}
        
        df = pd.DataFrame(data)

        df['data'] = pd.to_datetime(df['data'])
        df['month'] = df['data'].dt.to_period('M')
        df['tipo'] = df['tipo'].map({1: 'entrada', 2: 'saida'})
        grouped = df.groupby(['month', 'tipo']).agg({'valor': 'sum'}).reset_index()

        result = {}
        for _, row in grouped.iterrows():
            month = row['month'].strftime('%Y-%m')
            if month not in result:
                result[month] = {'entrada': 0, 'saida': 0}
            result[month][row['tipo']] = row['valor']
        
        return result