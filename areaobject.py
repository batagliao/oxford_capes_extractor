class EvaluationArea(object):
    name : str = ""
    link : str = ""
    areas = list()

class Area(object):
    name : str = ""
    link : str = ""
    eduAssociations = list()


class EducationalAssociation(object):
    programs = list()
    name: str = ""
    link: str = ""

class Program(object):
    name: str = ""
    link: str = ""

class Course(object):
    name: str = ""
    intituition: str = ""
    adminDependency: str = ""
    code: str = ""
    level: str = ""
    logradouro: str = ""
    bairro: str = ""
    city: str = ""
    zipcode: str = ""
    caixapostal: str = ""
    phone: str = ""
    email: str = ""
    url: str = ""
    
