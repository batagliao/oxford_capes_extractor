#!usr/bin/env python3

import requests
import areaobject
from cssselect import HTMLTranslator
from lxml import html, etree

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
    firstpage = requests.get("https://sucupira.capes.gov.br/sucupira/public/consultas/coleta/programa/quantitativos/quantitativoAreaAvaliacao.jsf;jsessionid=yoQxmtbSgP9Z8650K1kwdadW.sucupira-203" )
    tree = html.fromstring(firstpage.content)
    anchors = tree.xpath("//table[@class='listagem publico tablesorter']/tbody/tr/td/a")
    
    areas = list()

    for element in anchors:
        text = element.text
        link = element.get("href")
        
        if(text in allowedAreas):
            evArea = areaobject.EvaluationArea()
            evArea.name = text
            evArea.link = link;
            areas.append(evArea)

    return areas


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
    page = requests.get(BASE_URL+evaluationArea.link)
    tree = html.fromstring(page.content)
    anchors = tree.xpath(
        "//table[@class='listagem tablesorter publico']/tbody/tr/td/a")

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
        evaluationArea.areas.append(area)

    return evaluationArea.areas


def getEducationalInstitution(area):
    print("\tObtendo Instituições de {}".format(area.name))
    page = requests.get(BASE_URL + area.link)
    tree = html.fromstring(page.content)
    anchors = tree.xpath("//table[@class='listagem tablesorter publico']/tbody/tr/td/a")

    ies = list()
    for a in anchors:
        text = a.text
        link = a.get("href")
        ei = areaobject.EducationalInstitution()
        ei.name = text
        ei.link = link
        area.eduInstitutions.append(ei)

    return area.eduInstitutions

def getProgram(eduInstitution):
    print("\t\tObtendo programa de {}".format(eduInstitution.name))
    page = requests.get(BASE_URL + eduInstitution.link)
    tree = html.fromstring(page.content)
    anchors = tree.xpath("//table[@class='listagem tablesorter publico']/tbody/tr/td/a")

    programs = list()
    for a in anchors:
        text = a.text
        link = a.get("href")
        p = areaobject.Program()
        p.name = text
        p.link = link
        eduInstitution.programs.append(p)

    return eduInstitution.programs

if(__name__ == "__main__"):
    evaluationAreas = getEvaluationAreas()

    for evArea in evaluationAreas:           
        areas = getArea(evArea)

        for area in areas:
            eis = getEducationalInstitution(area)

            for institution in eis:
                program = getProgram(institution)

