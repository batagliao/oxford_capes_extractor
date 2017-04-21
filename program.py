import requests
from lxml import html
import areaobject

BASE_URL = "https://sucupira.capes.gov.br/"


def getPrograms(eduAssociation):
    print("\t\tObtendo programa de {}".format(eduAssociation.name))
    page = requests.get(BASE_URL + eduAssociation.link)
    tree = html.fromstring(page.content)
    anchors = tree.xpath(
        "//table[@class='listagem tablesorter publico']/tbody/tr/td/a")

    programs = list()
    for a in anchors:
        text = a.text
        link = a.get("href")

        #remover o parenteses
        lastindex = text.rfind('(')
        if(lastindex > -1):
            text = text[:lastindex - 1]

        p = areaobject.Program()
        p.name = text
        p.link = link
        programs.append(p)

    return programs
