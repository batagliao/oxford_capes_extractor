class EvaluationArea(object):
    name : str = ""
    link : str = ""
    areas = list()

class Area(object):
    name : str = ""
    link : str = ""
    eduInstitutions = list()


class EducationalInstitution(object):
    programs = list()
    name: str = ""
    link: str = ""

class Program(object):
    name: str = ""
    link: str = ""