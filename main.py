#!usr/bin/env python3

import sys
import areaobject
import evaluationarea
import area
import educationalassociation
import program
import course
import csv
from openpyxl import Workbook

def writetofile(evarea, a, association, program, c):
    filename = "{}_{}.csv".format(FILTER_AREA.lower(), FILTER_EVALUATIONAREA.lower())
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([evarea.name.strip(), "CIÊNCIAS DA SAÚDE",
                         a.name.strip(), c.intituition.strip(), c.adminDependency, program.name.strip(),
                        c.name.strip(), c.code.strip(), c.level.strip(),
                        a.name.strip(), c.logradouro.strip(), c.bairro.strip(), 
                        c.city.strip(), c.zipcode.strip(), c.caixapostal.strip(),
                        c.phone.strip(), c.email.strip(), c.url.strip()])

def writeheader():
    filename = "{}_{}.csv".format(FILTER_AREA.lower(),
                                         FILTER_EVALUATIONAREA.lower())
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Área de avaliação", "Grande área",
                        "Área", "IES", "Dependência administrativa", "Programa", 
                        "Cursos", "Código do curso", "Nível", "Área básica",
                        "Logradouro", "Bairro", "Cidade/UF", "Cep", "Caixa postal",
                        "Telefone", "E-mail", "URL"])


def writetofile_excel(evarea, a, association, program, c, ws):
    ws.append([evarea.name.strip(), "CIÊNCIAS DA SAÚDE",
                     a.name.strip(), c.intituition.strip(), None, program.name.strip(),
                     c.name.strip(), c.code.strip(), c.level.strip(),
                     a.name.strip(), c.logradouro.strip(), c.bairro.strip(),
                     c.city.strip(), c.zipcode.strip(), c.caixapostal.strip(),
                     c.phone.strip(), c.email.strip(), c.url.strip()])

def writeheader_excel(ws):                                     
    ws.append(["Área de avaliação", "Grande área",
              "Área", "IES", "Dependência administrativa", "Programa",
              "Cursos", "Código do curso", "Nível", "Área básica",
                        "Logradouro", "Bairro", "Cidade/UF", "Cep", "Caixa postal",
                        "Telefone", "E-mail", "URL"])   

def save_excel(wb):
    filename= "{}_{}.xlsx".format(FILTER_AREA.lower(),
                                  FILTER_EVALUATIONAREA.lower())
    wb.save(filename)

if(__name__ == "__main__"):

    if(len(sys.argv) < 3):
        print("Necessário passar parâmetros de filtro de área e subárea")
        exit(1)

    FILTER_EVALUATIONAREA = sys.argv[1].upper()
    FILTER_AREA = sys.argv[2].upper()

    #excel
    wb=Workbook(write_only = True)
    ws=wb.create_sheet()

    writeheader_excel(ws)
    writeheader()

    evaluationAreas = evaluationarea.getEvaluationAreas()

    for evArea in [a for a in evaluationAreas if a.name == FILTER_EVALUATIONAREA ]:
        areas = area.getArea(evArea)

        for area in [a for a in areas if a.name == FILTER_AREA]:
            associations = educationalassociation.getEducationalAssociation(area)

            for assoc in associations:
                programs = program.getPrograms(assoc)

                for prog in programs:
                    #for course
                    courses = course.getCourses(prog)

                    for c in courses:
                        writetofile(evArea, area, assoc, prog, c)
                        writetofile_excel(evArea, area, assoc, prog, c, ws)
                    
    save_excel(wb)

