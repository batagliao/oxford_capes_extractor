import requests
from lxml import html
import areaobject

BASE_URL = "https://sucupira.capes.gov.br/"


def getArea(evaluationArea):
    # engenharias e zootecnia tem especificidades

    allowedEngineeringI = [
        "ENGENHARIA SANITÁRIA"
    ]

    allowedEngineeringIV = [
        "ENGENHARIA BIOMÉDICA"
    ]

    allowedZootecn = [
        "ZOOTECNIA"
    ]

    print("Obtendo áreas de {}".format(evaluationArea.name))
    page = requests.get(BASE_URL + evaluationArea.link)
    tree = html.fromstring(page.content)
    anchors = tree.xpath(
        "//table[@class='listagem tablesorter publico']/tbody/tr/td/a")

    resultareas = list()

    for a in anchors:
        text = a.text
        link = a.get("href")

        if(evaluationArea.name == "ENGENHARIAS I"):
            if(text not in allowedEngineeringI):
                continue

        if(evaluationArea.name == "ENGENHARIAS IV"):
            if(text not in allowedEngineeringIV):
                continue

        if(evaluationArea.name == "ZOOTECNIA / RECURSOS PESQUEIROS"):
            if(text not in allowedZootecn):
                continue

        area = areaobject.Area()
        area.name = text
        area.link = link
        resultareas.append(area)

    return resultareas
