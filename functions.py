from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import requests
import difflib

# define a variavel global APIFinder, que é uma api para encontrar os domínios das compainhas
APIFinder = 'https://autocomplete.clearbit.com/v1/companies/suggest?query='

# define a variavel global APIFinder, que é uma api para encontrar os domínios das compainhas
auth_token = "pathOHh4mC5YAsTqI.3eddc964e3328f89fe1ae483983666ce703cb1038f5d45d1e64b7efb207e2381"

def firefoxGetDriver(url):
    # Configura as opções do Firefox para o modo headless
    options = Options()
    options.headless = True

    # Inicializa o driver do Firefox
    driver = webdriver.Firefox(options)

    # Carrega a página usando o Selenium
    driver.get(url)

    return driver

# aguarda a visibilidade de algum elemento da pagina
def driverWait(element, driver, time):
    try:
        # Aguarda disponibilidade do botão
        WebDriverWait(driver, time).until(EC.visibility_of_element_located((By.XPATH, element)))
    except TimeoutException:
        print("Timeout excedido. Tentando recarregar a página...")
        driver.refresh()
        # Aguarda disponibilidade do botão novamente após recarregar a página
        WebDriverWait(driver, time).until(EC.visibility_of_element_located((By.XPATH, element)))

# formata o texto para url
def formatar_para_url(texto):
    substituicoes = {
        ' ': '%20',
        '!': '%21',
        '"': '%22',
        '#': '%23',
        '$': '%24',
        '&': '%26',
        "'": '%27',
        '(': '%28',
        ')': '%29',
        '*': '%2A',
        '+': '%2B',
        ',': '%2C',
        '/': '%2F',
        ':': '%3A',
        ';': '%3B',
        '<': '%3C',
        '=': '%3D',
        '>': '%3E',
        '?': '%3F',
        '@': '%40',
        '[': '%5B',
        ']': '%5D',
        '^': '%5E',
        '`': '%60',
        '{': '%7B',
        '|': '%7C',
        '}': '%7D',
        '~': '%7E'
    }
    for caractere, substituicao in substituicoes.items():
        texto = texto.replace(caractere, substituicao)
    return texto

# Obtem o soup da pagina
def getSoup(driver):
    # Obtém o HTML da página depois que o JavaScript foi executado
    page = driver.page_source

    # Fecha o navegador
    driver.quit()

    # Use BeautifulSoup para analisar o HTML
    return BeautifulSoup(page, 'html.parser')

# obtem o nome das empresas a partir dos cards
def getNames(cards):
    # Cria uma lista vazia para armazenar os nomes das opções
    companyNames = []

    i = 0

    for option in cards:
        # Adiciona o texto da opção à lista se não for vazio
        cardText = option.text.strip()
        if cardText:
            '''i += 1'''
            companyNames.append(cardText)
        '''if i == 20:
            break'''

    # Filtra a lista para remover valores vazios e cria um JSON
    return list(filter(None, companyNames))

# obtém os domínios das empresas
def getDomains(quantasEmpresas, companyNames):

    urlComplete = []

    # Inicializa a lista com None para todos os índices
    domains = [None] * quantasEmpresas

    # Loop para juntar as strings
    for i in range(quantasEmpresas):

        maxSimilarity = 0

        # Formata o nome da empresa para HTML, visto que muitas tem caracteres especiais no nome
        nameUrl = formatar_para_url(companyNames[i]).lower()

        # Montando o URL completo da página que precisamos acessar
        urlComplete.append(APIFinder + nameUrl)

        # Faz a solicitação HTTP para a API
        response = requests.get(urlComplete[i])

        # Analisa o JSON retornado pela API
        data = response.json()

        for empresa in data:
            if empresa['name'].lower() == companyNames[i].lower():
                domains[i] = empresa['domain']
                break

        if domains[i] == None:
            companyNames[i] = None

    return domains

# uploada os dados no airtable
def airtableUpdate(companiesData):
    # Coloca na Airtable
    urlAirtable = "https://api.airtable.com/v0/apposMEtwpLIKroDf/CSVScraping"

    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }

    payload = {"records": [{"fields": company} for company in companiesData]}

    response = requests.post(urlAirtable, headers=headers, json=payload)
    response.json()

def printToguether(companiesName, companiesDomain):
    # printa no terminal
    for name, domain in zip(list(filter(None, companiesName)), list(filter(None, companiesDomain))):
        print(f"{name}; {domain}")

# usa a biblioteca Pandas para converter o arquivo para CSV
def convertoToCSV(companiesName, companiesDomain, nameOfScraping):
    companiesData = {}

    # Iterar sobre os nomes das empresas e seus respectivos domínios
    for Name, Domain in zip(companiesName, companiesDomain):
        # Adicionar o par chave-valor ao dicionário
        companiesData[Name] = Domain

# faz o tratamento antes de transformar em soup
def preSoupTreatment(driver, nameCards, classCards):
    soup = getSoup(driver)

    # busca o elemento que contem as cards na pagina
    if isinstance(classCards, (int, float, complex)):
        cards = soup.find_all(nameCards)[classCards]
    else:
        cards = soup.find_all(nameCards, class_=classCards)

    print(len(cards))

    return cards

# faz o enriquecimento dos dados depois de transformar em soup
def postSoupTreatment(cards):
    # obtem o nome das companhias
    companiesName = getNames(cards)

    # obtem o domínio das companhias
    # companiesDomain = getDomains(10, companiesName)
    companiesDomain = getDomains(len(companiesName), companiesName)

    # combina os dados para enviar ao airtable
    combinedData = list(zip(companiesName, companiesDomain))

    # printa no terminal
    printToguether(companiesName, companiesDomain)

    '''for name in companiesName:
        print(f"{name}")'''

    """for pair in combinedData:
        print(f" {pair},")

    # upa os dados pro airtable
    airtableUpdate(combinedData)"""

# scrolla a página
def scrollPage(totalHeight, driver):
    for i in range(1, totalHeight, 100):
        driver.execute_script("window.scrollTo(0, {});".format(i))