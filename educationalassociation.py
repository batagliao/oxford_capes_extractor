import requests
from lxml import html
import areaobject

BASE_URL = "https://sucupira.capes.gov.br/"


def getEducationalAssociation(area):
    print("\tObtendo Instituições de {}".format(area.name))
    page = requests.get(BASE_URL + area.link)
    tree = html.fromstring(page.content)
    anchors = tree.xpath(
        "//table[@class='listagem tablesorter publico']/tbody/tr/td/a")

    ies = list()
    for a in anchors:
        text = a.text
        link = a.get("href")
        ea = areaobject.EducationalAssociation()
        ea.name = text
        ea.link = link
        area.eduAssociations.append(ea)

    return area.eduAssociations
