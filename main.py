import xml.etree.ElementTree as Element
from zipfile import ZipFile
from Classes.poligono import *


def abrir_projeto(arq_name):
    if '.kmz' in arq_name:
        with ZipFile(arq_name, 'r') as f:
            f.extract('doc.kml', 'TEMP')
            arq_name = 'TEMP/doc.kml'
    return Element.parse(arq_name)


def percorrer_e_manter(root_arq, poligono_arq):
    np = root_arq.tag.split('}')[0] + '}'
    for root2 in root_arq.findall("*"):
        if root2.tag == np + "Placemark":
            for root3 in root2.findall(np + "Point"):
                for root4 in root3.findall(np + "coordinates"):
                    coordenada = [float(root4.text.strip().split(',')[1]),
                                  float(root4.text.strip().split(',')[0])]
                    if poligono_arq.esta_dentro(coordenada):
                        root_arq.remove(root2)
                        break
            for root3 in root2.findall(np + "LineString"):
                for root4 in root3.findall(np + "coordinates"):
                    coordenada = [float(root4.text.strip().split()[0].split(',')[1]),
                                  float(root4.text.strip().split()[0].split(',')[0])]
                    if poligono_arq.esta_dentro(coordenada):
                        root_arq.remove(root2)
                        break
            for root3 in root2.findall(np + "Polygon"):
                coordenada = [float(root3[1][0][0].text.strip().split()[0].split(',')[1]),
                              float(root3[1][0][0].text.strip().split()[0].split(',')[0])]
                if poligono_arq.esta_dentro(coordenada):
                    root_arq.remove(root2)
                    break
        else:
            percorrer_e_manter(root2, poligono_arq)


if __name__ == '__main__':
    doc = abrir_projeto("projeto.kmz")
    root = doc.getroot()
    poligonos = Poligono.extrair_poligonos("poligonos.kmz")
    for poligono in poligonos:
        percorrer_e_manter(root, poligono)
    doc.write('projeto_fora_do_poligono.kmz')
