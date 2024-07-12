from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup 
import time
import csv

service = Service()
options = webdriver.FirefoxOptions()

navegador = webdriver.Firefox(service=service, options=options)

url = 'https://precodahora.ba.gov.br/'

navegador.get(url)
time.sleep(2)

input1 = navegador.find_element(by=By.ID, value="fake-sbar")
input1.click()

input2 = navegador.find_element(by=By.ID, value="top-sbar")
input2.send_keys("etanol")

button = navegador.find_element(By.CLASS_NAME, "btn-top-sbar")
button.click()

time.sleep(2)
listaItens = []

for i in range(0, 25):
    nomeItem = 'card_list_1-' + str(i)
    
    try:
        item = navegador.find_element(By.ID, nomeItem)
        item_html = item.get_attribute('outerHTML')

        soup = BeautifulSoup(item_html, 'html.parser')
        
        # Extrai do HTML os dados do produto
        nome_produto = soup.find('div', style="font-size:18px;").strong.text
        valor_produto = soup.find('div', style="font-size:42px;font-weight:bold; color: #000;").text.strip()
        codigo_barras = soup.find('i', class_='fa fa-barcode codbarra').next_sibling.strip()
        estabelecimento = soup.find('i', class_='fa fa-building').next_sibling.strip()
        endereco = soup.find('i', class_='fa fa-map-signs').next_sibling.strip()
        
        
        listaItens.append([nome_produto, valor_produto, codigo_barras, estabelecimento, endereco])
        
    except Exception as e:
        print(f"Erro ao processar item {nomeItem}: {e}")

# Nome do arquivo CSV
nome_arquivo = 'dados.csv'

# Escrevendo os dados no arquivo CSV
with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as arquivo_csv:
    escritor_csv = csv.writer(arquivo_csv)
    escritor_csv.writerow(['Nome do Produto', 'Valor', 'Código de Barras', 'Estabelecimento', 'Endereço'])
    escritor_csv.writerows(listaItens)
