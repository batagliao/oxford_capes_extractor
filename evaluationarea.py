import requests
from lxml import html
import areaobject

BASE_URL = "https://sucupira.capes.gov.br/"

def getEvaluationAreas():
    allowedAreas = [
        "BIODIVERSIDADE",
        "BIOTECNOLOGIA",
        "CIÊNCIAS AMBIENTAIS",
        "CIÊNCIAS BIOLÓGICAS I",
        "CIÊNCIAS BIOLÓGICAS II",
        "CIÊNCIAS BIOLÓGICAS III",
        "ENFERMAGEM",
        "ENGENHARIAS I",
        "ENGENHARIAS IV",
        "FARMÁCIA",
        "MEDICINA VETERINÁRIA",
        "NUTRIÇÃO",
        "ODONTOLOGIA",
        "PSICOLOGIA",
        "SAÚDE COLETIVA",
        "SERVIÇO SOCIAL",
        "ZOOTECNIA / RECURSOS PESQUEIROS"
    ]
    print("Obtendo primeira página")
    firstpage = requests.get(
        "https://sucupira.capes.gov.br/sucupira/public/consultas/coleta/programa/quantitativos/quantitativoAreaAvaliacao.jsf;jsessionid=yoQxmtbSgP9Z8650K1kwdadW.sucupira-203")
    tree = html.fromstring(firstpage.content)
    anchors = tree.xpath(
        "//table[@class='listagem publico tablesorter']/tbody/tr/td/a")

    areas = list()

    for element in anchors:
        text = element.text
        link = element.get("href")

        if(text in allowedAreas):
            evArea = areaobject.EvaluationArea()
            evArea.name = text
            evArea.link = link
            areas.append(evArea)

    return areas
