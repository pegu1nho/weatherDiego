import requests
import sqlite3
import datetime
import config

banco = sqlite3.connect('weather.db')
cursor = banco.cursor()

#cursor.execute("CREATE TABLE previsao (id_previsao integer PRIMARY KEY AUTOINCREMENT, temperatura text, umidade text, descricao text, velocidade text, data text, hora text)")

def retorna_url(cidade, estado):

    fields = 'only_results,city_name,temp,date,time,description,currently,humidity,wind_speedy,sunrise,sunset,condition_slug,forecast,max,min,date'
    city = cidade
    state = estado
    key = config.api_key

    URL = (f'https://api.hgbrasil.com/weather?array_limit=2&format=json&fields={fields}&city_name={city},{state}&key={key}')

    return URL

def inserir_banco(temperatura, umidade, descricao, velocidade, data, hora):

    cursor.execute("INSERT INTO previsao (temperatura, umidade, descricao, velocidade, data, hora) VALUES ('"+temperatura+"', '"+umidade+"', '"+descricao+"', '"+velocidade+"', '"+data+"', '"+hora+"')")
    banco.commit()

def consultar_banco():
    cursor.execute("SELECT * FROM previsao")
    print(cursor.fetchall())

def imprime_previsao(data_, max, min):
    for i in range(len(data_)):
        print("Data: ", data_[i])
        print("Média: ", (max[i] + min[i]) / 2)

def imprime_dados():
    print(f"\n{cidade}")
    print(
        f"\nTemperatura atual: {temperatura}° C \nData/hora: {data} {hora} \nDescrição: {descricao} \nReferencia: {referencia} \nUmidade: {umidade}% \nVelocidade do vento: {velocidade}"
        f"\nNascer do sol: {nascer} \nPor do sol: {por} \nCondição climática: {condicao} \n\nPrevisão: ")
    imprime_previsao(data_, max, min)

def retorna_data():
    d = datetime.datetime.now()
    data = (f"{d.day}/{d.month}/{d.year}")
    return data

def retorna_hora():
    d = datetime.datetime.now()
    hora = (f"{d.hour}:{d.minute}:{d.second}")
    return hora


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    city = input("Digite a cidade: ")
    state = input("Digite o estado (sigla): ")

    URL = retorna_url(city, state)

    resposta = requests.get(URL)

    if resposta:

        r = resposta.json()

        temperatura = r['temp']
        data = r['date']
        hora = r['time']
        descricao = r['description']
        referencia = r['currently']
        umidade = r['humidity']
        velocidade = r['wind_speedy']
        nascer = r['sunrise']
        por = r['sunset']
        condicao = r['condition_slug']
        cidade = r['city_name']
        previsao = r['forecast']

        data_ = []
        max = []
        min = []

        for i in range(len(previsao)):
            data_.append(previsao[i]['date'])
            max.append(previsao[i]['max'])
            min.append(previsao[i]['min'])

        imprime_dados()

        inserir_banco(str(temperatura), str(umidade), descricao, velocidade, retorna_data(), retorna_hora())

        print("\nSelect banco: ")
        consultar_banco()

    else:
        print('Not ok')