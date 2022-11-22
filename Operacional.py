import openpyxl

import Banco_de_dados
import tkinter
import tkinter.messagebox
import numpy as np
import matplotlib as plt
from PIL import Image, ImageDraw


class funcoes_geral():
    def __init__(self):
        self.criar_imagens()
    def criar_imagens(self, foto='C:\\Users\\Samuel\\Downloads\\senhor.jpg', tamanho= (100,100)):
        if foto == '': return
        img0 = Image.open(foto).convert("RGB")
        width, height = img0.size
        tamx = 0
        tamy = 0
        diferx = 0
        difery = 0
        if height < width:
            tamy = height
            tamx = height
            diferx = (width-height)/2
        else:
            tamy = width
            tamx = width
            difery = (height - width)/2
        img = img0.crop((diferx,difery,tamx+diferx,tamy+difery)).resize(tamanho) #cortando em quadrado centralizado e redimencionando
        img.save(foto[:len(foto)-4] + '_Retangulo.gif')
        # passando desenho para lista (só funciona caso a img esta em convert('RGB')
        npImage = np.array(img)
        lista = []
        for i in range(0,100):
            linha = []
            for x in range(0,100):
                linha.append([x,x,x])
            lista.append(linha)
        print(npImage)
        print(lista)

        h, w = img.size
        #desenhar o circulo
        alpha = Image.new('L', img.size,'black').convert("RGBA") #o 255 é definindo a cor em preto toda a tela
        fundo = Image.new('RGB', img.size,(255,255,255))
        draw = ImageDraw.Draw(alpha)
        draw.pieslice([0, 0, h, w], 0, 360, fill='white', outline='black') #desenhando circulo branco na tela
        #precisamos passar o circulo para array também
        npAlpha = np.array(alpha)
        # aqui faz a magia do corte circular na imagem principal. A ordem faz toda a diferença
        npImage = np.dstack((npImage,npAlpha))
        # depois preciso mudar o fundo para a cor da tela
        Ifinal = Image.fromarray(npImage)
        Ifinal.save(foto[:len(foto) - 4] + '_circulo.png')
class funcoes_login(Banco_de_dados.BD):
    def verificar_login(self,event):
        BD = self.abrir_BD()
        ws = BD['logins']

        for lin in range(2,1_000_000,1):
            if ws.cell(row=lin,column=1).value == None:
                tkinter.messagebox.showinfo('Login', 'Matricula não existe!')
                self.usuario.entry.delete(0, tkinter.END)
                self.senha.entry.delete(0, len(self.senha.entry.get()))
                break
            if ws.cell(row=lin,column=1).value == self.usuario.entry.get():
                if ws.cell(row=lin,column=2).value == self.senha.entry.get():
                    tkinter.messagebox.showinfo('Login','Login correto')
                    self.tela_login.destroy()
                    if str(ws.cell(row=lin,column=1).value).find('adm') > -1:
                        self.abrir_appAdm()
                    else:
                        self.abrir_appCli()
                else:
                    tkinter.messagebox.showinfo('Login','Senha errada!')
                    self.senha.entry.delete(0, len(self.senha.entry.get()))
                break
        self.fechar_BD(BD)
class funcoes_adm(Banco_de_dados.BD):
    def deletar_frames(self):
        for item in self.tela.winfo_children():
            if str(item.widgetName) != 'Frame': continue
            if item.winfo_name() == self.frame_abas.winfo_name(): continue
            for filho in item.winfo_children():
                try:
                    filho.destroy()
                except:
                    print(f'{filho.winfo_name()} é None!')
            try:
                item.destroy()
            except:
                print(f'{item.winfo_name()} é None!')
    def clicar_menu(self,event):
        lista = [self.bt_notificacoes, self.bt_acao_estoque, self.bt_dash, self.bt_compra_descarte,
                 self.bt_cadastro]
        #self.tela.winfo_pointerx()-self.tela.winfo_rootx() - encontra a posição do cursor na tela em pixels
        contador  = 0
        posicao = 0
        for item in self.frame_abas.winfo_children():
            if item.winfo_x()-(self.tela.winfo_pointerx()-self.tela.winfo_rootx()) <= 0 and item.winfo_x()-(self.tela.winfo_pointerx()-self.tela.winfo_rootx()) > -205:
                for itemLista in lista:
                    if itemLista.lbBase.winfo_name() == item.winfo_name():
                        if itemLista.selecionado == True: return
                        itemLista.selecionou('')
                        posicao = contador
                        break
                    contador +=1
                for itemLista in lista:
                    if itemLista.lbBase.winfo_name() != item.winfo_name():
                        itemLista.retira_selecao()
                break
        self.deletar_frames()
        self.gerar_aba_treeview()

        funcoes={
            '0': self.gerar_obj_notificacoes,
            '1': self.gerar_obj_acao_estoque,
            '2': self.gerar_obj_dash,
            '3': self.gerar_obj_compra_descarte,
            '4': self.gerar_obj_cadastro
        }
        funcoes[str(posicao)]()
    def carregar_cabecalho_treeview(self, nome_aba, colunas: list):
        ''' as colunas é uma lista com o numero das colunas a serem adicionadas
        ex.: [0,1,5,7]'''
        wb = self.abrir_BD()
        ws = wb[nome_aba]
        #a variavel cabecalho vem com self porque queremos usar na classe app_Adm!
        self.cabecalho = []
        for col in colunas:
            if ws.cell(row=1,column=col).value == None: break
            self.cabecalho.append(ws.cell(row=1,column=col).value)
        self.fechar_BD(wb)
    def filtro_geral(self, colunas=[], lin=0):
        self.filtro = True
    def tags_personalizadas(self,linha: int, coluna_e_codigo: list, ws: openpyxl.Workbook):
        '''como deve ser escrito a lista colunas: colunas = [[numero coluna,texto-tag,texto-tag]...]
        exemplo: [[2,pendente-perigo,espera-alerta]] (esse caso irá usar a tag perigo para o texto pendente)'''
        tag = 'normal'
        if len(coluna_e_codigo) == 1:
            print(f'coluna {coluna_e_codigo[0]} sem informações para tags')
            return tag
        for i in range(1,len(coluna_e_codigo),1):
            if ws.cell(row=linha,column=coluna_e_codigo[0]).value == coluna_e_codigo[i][:str(coluna_e_codigo[i]).find('-')]:
                tag =  coluna_e_codigo[i][str(coluna_e_codigo[i]).find('-')+1:]
                return tag
        return tag

    def carregar_tabela_com_codigo(self, nome_aba, caso_pai,colunas='', treeview='', filtro=False, tags=False):
        '''
        --caso_pai:
        o caso pai é uma lista com dois termos: [numero coluna, texto da condicional]
        ex: [6,'pedido']
        na coluna 6, toda linha que tiver escrito pedido

        --tags:
        as tags são confusas. para usar as tags, precisa escrever uma lista assim:
        ex: tags = [[2,pendente-perigo,espera-alerta..],[4,pendente-perigo,espera-alerta..]].
        sempre com duas listas internas, uma é pra escolher a tag do item pai, outra dos filhos.
        dentro dessas listas estão os parametros: [numero coluna,texto-tag,texto-tag...]
        '''
        if tags != False:
            if len(tags) != 2:
                print('as tags desta função precisam de 2 listas no formato [num col, texto-tag,texto-tag..]')
                return
        if treeview == '': treeview = self.treev_principal
        if colunas == False: colunas = self.cabecalho
        wb = self.abrir_BD()
        ws = wb[nome_aba]
        linha = []
        #trazendo codigos unicos[coluna de codigos] para o loop
        lista_pai=[]
        item_adicionado = False #variavel de controle
        for lin in range(2,1_000_000,1):
            item_adicionado = False
            if ws.cell(row=lin,column=1).value == None: break
            if filtro == True: #esse filtro ainda precisa ser elaborado!
                self.filtro_geral()
                if self.filtro == False: continue
            for item in lista_pai:
                if ws.cell(row=lin, column=1).value == item:
                    item_adicionado = True
                    break
            if item_adicionado == True: continue
            lista_pai.append(ws.cell(row=lin, column=1).value)
        #precisamos de dois indices diferentes para criar o parentesco
        indice = 0
        indice_Pai = 0
        #vamos carregar a treeview toda!
        for pathern in lista_pai: #esse for controla a dependencia dos itens
            for lin in range(2,1_000_000,1):
                if ws.cell(row=lin, column=1).value == None: break
                if ws.cell(row=lin, column=1).value == pathern:
                    if ws.cell(row=lin, column=caso_pai[0]).value == caso_pai[1]:
                        minha_tag = self.tags_personalizadas(linha=lin,coluna_e_codigo=tags[0],ws=ws)
                        for x in colunas:
                            if x == 1: continue
                            linha.append(ws.cell(row=lin,column=x).value)
                        treeview.treeview.insert('',index=indice,iid=str(indice_Pai) + 'p',text=ws.cell(row=lin,column=1).value,values=linha, tags=minha_tag)
                        indice +=1
            for lin in range(2,1_000_000,1): #vamos adicionar os itens filhos!
                if ws.cell(row=lin, column=1).value == None: break
                if ws.cell(row=lin,column=1).value == pathern:
                    if ws.cell(row=lin, column=caso_pai[0]).value == caso_pai[1]: continue
                    minha_tag = self.tags_personalizadas(linha=lin, coluna_e_codigo=tags[1], ws=ws)
                    linha = [ws.cell(row=lin, column=x).value for x in colunas if x != 1]
                    treeview.treeview.insert(str(indice_Pai) + 'p',index=indice,iid=str(indice)+'_'+str(indice_Pai)+'p',values=linha, tags=minha_tag)
                    indice += 1
            indice_Pai +=1
        self.fechar_BD(wb)






#rodar = funcoes_geral()
