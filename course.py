import requests
from lxml import html
import areaobject

BASE_URL = "https://sucupira.capes.gov.br/"


def getCourses(program: areaobject.Program):
   print("\t\t\t Obtendo informações cursos do programa {}".format(program.name))
   page = requests.get(BASE_URL + program.link)
   tree = html.fromstring(page.content)

   sections = tree.xpath(
       "//div[@class='conteudo-painel']/div[@class='titulo']")

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

       #verifica se o nome já foi adicionado
       if(any(rc.name == iename for rc in resultcourses)):
           continue

       if(any(rc.intituition == iename for rc in resultcourses)):
           continue

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
       resultcourses.append(c)

   return resultcourses

def getcontainervalue(container):
    valcontainer = container.getchildren()[1]
    children = valcontainer.getchildren()
    if(len(children) > 0):
        return children[0].text
    else:
        return ""
