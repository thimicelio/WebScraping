from selenium.webdriver.common.by import By
from time import sleep
import functions
import re

def salesForceScraping():

    url = "https://reg.salesforce.com/flow/plus/df23/sponsors/page/sponsorlisting"
    pathList = '//*[@id="rf-exhibitorcatalog"]/div/main/div[3]/div'
    pathButton = '//*[@id="onetrust-accept-btn-handler"]'
    nameCards = 'h4'
    classCards = 'rf-tile-title'

    # gera o driver do selenim
    driver = functions.firefoxGetDriver(url)

    # espera ate o botão "aceitar cookies" ser carregado
    functions.driverWait(pathButton, driver, 10)

    # clica no botão "aceitar cookies"
    driver.find_element(By.XPATH, pathButton).click()

    # espera ate a lista ser carregada
    functions.driverWait(pathList, driver, 10)

    # faz todos os tratamentos seguintes para encontrar os cards
    cards = functions.preSoupTreatment(driver, nameCards, classCards)

    # obtem os dados dos cards
    functions.postSoupTreatment(cards)

def shmrScraping():

    url = "https://shrm24.mapyourshow.com/8_0/exhview/index.cfm?orsearchtype0=exhibitor&orsearchvalue0=1944437-SH&orsearchdisplay0=Exhibitor"
    pathMap = '//*[@id="mys-floorplan-canvas-div"]/div[1]/canvas'
    nameCards = 'select'
    classCards = 1

    # gera o driver do selenim
    driver = functions.firefoxGetDriver(url)

    # espera pela visibilidade do mapa
    functions.driverWait(pathMap, driver, 20)

    # faz todos os tratamentos seguintes para encontrar os cards
    cards = functions.preSoupTreatment(driver, nameCards, classCards)

    # obtem os dados dos cards
    functions.postSoupTreatment(cards)

def nascsShowScraping():

    url = "https://nacs23.mapyourshow.com/8_0/explore/exhibitor-gallery.cfm?featured=false"
    allExhibittorButtonPath = '//*[@id="exhibitor"]'
    showAllButtonPath = '//*[@id="exhibitor-results"]/div[1]/span/a'
    totalHeight = 130000
    nameCards = 'h3'
    classCards = 'card-Title break-word f2 mb1 mt0'

    # gera o driver do selenim
    driver = functions.firefoxGetDriver(url)

    # Aguarda abrir o site
    functions.driverWait(allExhibittorButtonPath, driver, 10)

    # Encontrar e clicar no botão "All Exhibitors"
    driver.find_element(By.XPATH, allExhibittorButtonPath).click()

    # Encontrar e clicar no botão "See All Results"
    driver.find_element(By.XPATH, showAllButtonPath).click()
    sleep(2)

    # Scrolla a pagina para carregar elementos
    functions.scrollPage(totalHeight, driver)

    # faz todos os tratamentos seguintes para encontrar os cards
    cards = functions.preSoupTreatment(driver, nameCards, classCards)

    # obtem os dados dos cards
    functions.postSoupTreatment(cards)

def infocommShowScraping():
    url = "https://www.infocommshow.org/exhibit/current-exhibitors"
    exhibitsButton = '/html/body/div[2]/main/div/main/div/div[4]/div[2]'
    nameCards = 'div'
    classCards = 'article__body u-text-color-one'

    # gera o driver do selenim
    driver = functions.firefoxGetDriver(url)

    # Aguarda abrir o site
    functions.driverWait(exhibitsButton, driver, 10)
    sleep(2)

    soup = functions.getSoup(driver)

    cards = soup.find_all(nameCards, class_=classCards)

    # Descarta os 5 primeiro elementos de "cards", que são inuteis nesse site
    cards = cards[5:]

    companiesDomain = functions.getNames(cards)

    # Separa os elementos, que estão juntos por um /n
    companiesDomain = companiesDomain[0].splitlines() + companiesDomain[1].splitlines()

    for domain in companiesDomain:
        print(f"{domain}")

def blackHatScraping():
    url = "https://www.blackhat.com/html/sponsors_sustaining.html"
    pathButton = '//*[@id="eucookielawcontainer"]/div/div/div/div[2]/p/a'

    # gera o driver do selenim
    driver = functions.firefoxGetDriver(url)

    # espera ate o botão "aceitar cookies" ser carregado
    functions.driverWait(pathButton, driver, 10)

    # clica no botão "aceitar cookies"
    driver.find_element(By.XPATH, pathButton).click()
    sleep(2)

    soup = functions.getSoup(driver)

    # obtem os nomes atravez de um path
    cards = soup.find_all('a', attrs={'name': True})

    companiesName = []

    # Itera sobre os elementos encontrados
    for elemento in cards:
        # Obtenha o valor do atributo 'name' de cada elemento e imprima
        companiesName.append(elemento['name'])

    companiesDomain = functions.getDomains(len(companiesName), companiesName)

    functions.printToguether(companiesName, companiesDomain)

def fabeTechScraping():
    url = "https://s36.a2zinc.net/clients/sme/FABTECH2024/Public/exhibitors.aspx?ID=6407&sortMenu=103000"
    pathButton = '/html/body/div[1]/div'
    nameCards = 'td'
    classCards = 'companyName'

    # gera o driver do selenim
    driver = functions.firefoxGetDriver(url)

    # espera ate o botão "aceitar cookies" ser carregado
    functions.driverWait(pathButton, driver, 10)

    # clica no botão "aceitar cookies"
    driver.find_element(By.XPATH, pathButton).click()

    # faz todos os tratamentos seguintes para encontrar os cards
    cards = functions.preSoupTreatment(driver, nameCards, classCards)

    # obtem os dados dos cards
    functions.postSoupTreatment(cards)

def CESScraping():
    url = "https://s36.a2zinc.net/clients/sme/FABTECH2024/Public/exhibitors.aspx?ID=6407&sortMenu=103000"
    pathButton = '/html/body/div[1]/div'
    nameCards = 'td'
    classCards = 'companyName'

    # gera o driver do selenim
    driver = functions.firefoxGetDriver(url)

    # espera ate o botão "aceitar cookies" ser carregado
    functions.driverWait(pathButton, driver, 10)

    # clica no botão "aceitar cookies"
    driver.find_element(By.XPATH, pathButton).click()

    # faz todos os tratamentos seguintes para encontrar os cards
    cards = functions.preSoupTreatment(driver, nameCards, classCards)

    # obtem os dados dos cards
    functions.postSoupTreatment(cards)

def shotShowScraping():
    url = "https://n1b.goexposoftware.com/events/ss24/goExpo/exhibitor/listExhibitorProfiles.php"
    pathButton = '//*[@id="1000024"]'
    nameCards = 'tr'
    classCards = 'ffTableSet'

    # gera o driver do selenim
    driver = functions.firefoxGetDriver(url)

    # espera ate a tabela ser carregada
    functions.driverWait(pathButton, driver, 10)
    sleep(2)

    soup = functions.getSoup(driver)

    cards = soup.find_all('a', href=re.compile(r'exhibitor/viewExhibitorProfile.php\?'))

    print(len(cards))

    # obtem os dados dos cards
    functions.postSoupTreatment(cards)

def worldConcrete():

    url = "https://ge24woc.mapyourshow.com/8_0/explore/exhibitor-gallery.cfm?featured=false"
    allExhibittorButtonPath = '//*[@id="exhibitor"]'
    showAllButtonPath = '//*[@id="exhibitor-results"]/div[1]/span/a'
    totalHeight = 130000
    nameCards = 'span'
    classCards = 'b'

    # gera o driver do selenim
    driver = functions.firefoxGetDriver(url)

    # Aguarda abrir o site
    functions.driverWait(allExhibittorButtonPath, driver, 10)

    # Encontrar e clicar no botão "All Exhibitors"
    driver.find_element(By.XPATH, allExhibittorButtonPath).click()

    # Encontrar e clicar no botão "See All Results"
    driver.find_element(By.XPATH, showAllButtonPath).click()
    sleep(2)

    # Scrolla a pagina para carregar elementos
    functions.scrollPage(totalHeight, driver)

    # faz todos os tratamentos seguintes para encontrar os cards
    cards = functions.preSoupTreatment(driver, nameCards, classCards)

    # obtem os dados dos cards
    functions.postSoupTreatment(cards)