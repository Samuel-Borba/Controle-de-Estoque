import openpyxl
_caminho = 'banco_de_dados\\BD.xlsx'
class BD():
    def abrir_BD(self) -> openpyxl.Workbook:
        BD = openpyxl.load_workbook(_caminho)
        return BD
    def fechar_BD(self,BD: openpyxl.Workbook):
        BD.save(_caminho)
        BD.close()
