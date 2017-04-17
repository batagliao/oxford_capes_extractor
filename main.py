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


def getEducationalAssociation(area):
    print("\tObtendo Instituições de {}".format(area.name))
    page = requests.get(BASE_URL + area.link)
    tree = html.fromstring(page.content)
    anchors = tree.xpath("//table[@class='listagem tablesorter publico']/tbody/tr/td/a")

    ies = list()
    for a in anchors:
        text = a.text
        link = a.get("href")
        ea = areaobject.EducationalAssociation()
        ea.name = text
        ea.link = link
        area.eduAssociations.append(ea)

    return area.eduAssociations

def getPrograms(eduAssociation):
    print("\t\tObtendo programa de {}".format(eduAssociation.name))
    page = requests.get(BASE_URL + eduAssociation.link)
    tree = html.fromstring(page.content)
    anchors = tree.xpath("//table[@class='listagem tablesorter publico']/tbody/tr/td/a")

    programs = list()
    for a in anchors:
        text = a.text
        link = a.get("href")
        p = areaobject.Program()
        p.name = text
        p.link = link
        eduAssociation.programs.append(p)

    return eduAssociation.programs


def getCourses(program: areaobject.Program):
   print("\t\t\t Obtendo informações cursos do programa {}".format(program.name))
   page = requests.get(BASE_URL + program.link)
   tree = html.fromstring(page.content)

   sections = tree.xpath("//div[@class='conteudo-painel']/div[@class='titulo']")
      
   # primeira seção é sobre o programa > ignore
   # segunda seção são as universidades
   # terceira seção os cursos

   resultcourses = list()

   course = sections[2].getnext()
   coursename = course.getchildren()[0].text

   coursecodcontainer = course.getnext()
   coursecod = getcontainervalue(coursecodcontainer)

   levelcontainer = coursecodcontainer.getnext()
   level = getcontainervalue(levelcontainer)

   ies = sections[1].getparent().xpath("//h2")
   for ie in ies[:-1]:
       iename = ie.getchildren()[0].text
       cepcontainer = ie.getnext()
       cep = getcontainervalue(cepcontainer)
       
       logradourocontainer = cepcontainer.getnext()
       logradouro = getcontainervalue(logradourocontainer)

       numerocontainer = logradourocontainer.getnext()
       numero = getcontainervalue(numerocontainer)

       complementocontainer = numerocontainer.getnext()
       complemento = getcontainervalue(complementocontainer)

       bairrocontainer = complementocontainer.getnext()
       bairro = getcontainervalue(bairrocontainer)

       municipiocontainer = bairrocontainer.getnext()
       municipio = getcontainervalue(municipiocontainer)

       faxcontainer = municipiocontainer.getnext()
       fax = getcontainervalue(faxcontainer)

       telcontainer = faxcontainer.getnext()
       tel = getcontainervalue(telcontainer)

       emailprogramacontainer = telcontainer.getnext()
       emailprogram = getcontainervalue(emailprogramacontainer)

       urlcontainer = emailprogramacontainer.getnext()
       url = getcontainervalue(urlcontainer)
       
       c = areaobject.Course()
       c.name = coursename
       c.intituition = iename
       c.adminDependency = ""
       c.code = coursecod
       c.level = level
       c.logradouro = logradouro
       c.bairro = bairro
       c.city = municipio
       c.zipcode: cep
       c.caixapostal = ""
       c.phone = tel
       c.email = emailprogram
       c.url = url

   
    


def getcontainervalue(container):
    valcontainer = container.getchildren()[1]
    children = valcontainer.getchildren()
    if(len(children) > 0):
        return children[0].text
    else:
        return ""


if(__name__ == "__main__"):
    evaluationAreas = getEvaluationAreas()

    for evArea in evaluationAreas:           
        areas = getArea(evArea)

        for area in areas:
            associations = getEducationalAssociation(area)

            for assoc in associations:
                programs = getPrograms(assoc)

                for program in programs:
                    program = getCourses(program)

