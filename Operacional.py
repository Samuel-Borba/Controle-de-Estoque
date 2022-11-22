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
    def carregar_cabecalho_treeview(self, nome_aba):
        wb = self.abrir_BD()
        ws = wb[nome_aba]
        #a variavel cabecalho vem com self porque queremos usar na classe app_Adm!
        self.cabecalho = []
        for col in range(1,1_000_000,1):
            if ws.cell(row=1,column=col).value == None: break
            self.cabecalho.append(ws.cell(row=1,column=col).value)
        self.fechar_BD(wb)
    def filtro_geral(self, colunas=[], lin=0):
        self.filtro = True
    def tags_personalizadas(self, n_colunas: list, lista_nome_tags):
        '''preciso de ajuda pra criar uma função melhor. por enquanto esta assim:
        n_colunas escolhe a coluna pra verificar o texto
        lista '''
    def carregar_tabela_com_codigo(self, nome_aba, filtro=False,tags=[]):
        '''as tags sempre são 4 e na ordem: [normal,alerta,pedido,ok]'''
        wb = self.abrir_BD()
        ws = wb[nome_aba]
        linha = []
        #descobrindo ultima coluna preenchida
        ultima_Col = 0
        for col in range(2,1_000,1):
            if ws.cell(row=1,column=col+1).value == None:
                ultima_Col=col
                break
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
        #essas tags vao ser correlacionadas as ordens das tags informadas na função
        minhatag = ['normal', 'alerta', 'perigo', 'ok']
        pd_tab = ['codigo']

        #vamos carregar a treeview toda!
        for pathern in lista_pai: #esse for controla a dependencia dos itens
            for lin in range(2,1_000_000,1):
                if ws.cell(row=lin, column=1).value == None: break
                if ws.cell(row=lin, column=1).value == pathern:
                    #precisamos criar depois uma função pra adicionar tags fora desta!
                    if ws.cell(row=lin, column=3).value == 'pedido': #precisamos colocar uma variavel flex aqui!
                        minha_tag = 'normal'
                        if ws.cell(row=lin, column=6).value == 'espera':
                            minha_tag = 'alerta'
                        for x in range(2,ultima_Col+1):
                            linha.append(ws.cell(row=lin,column=x).value)
                        self.treev_principal.treeview.insert('',index=indice,iid=str(indice_Pai) + 'p',text=ws.cell(row=lin,column=1).value,values=linha, tags=minha_tag)
                        indice +=1
            for lin in range(2,1_000_000,1): #vamos adicionar os itens filhos!
                if ws.cell(row=lin, column=1).value == None: break
                if ws.cell(row=lin,column=1).value == pathern:
                    if ws.cell(row=lin, column=3).value == 'pedido': continue #precisamos colocar uma variavel flex aqui!
                    minha_tag = 'normal'
                    if ws.cell(row=lin, column=7).value == 'pendente':
                        minha_tag = 'alerta'
                    elif ws.cell(row=lin, column=7).value == 'negado':
                        minha_tag = 'perigo'
                    elif ws.cell(row=lin, column=7).value == 'aceito':
                        minha_tag = 'ok'
                    linha = [ws.cell(row=lin, column=x).value for x in range(2, ultima_Col + 1)]
                    self.treev_principal.treeview.insert(str(indice_Pai) + 'p',index=indice,iid=str(indice)+'_'+str(indice_Pai)+'p',values=linha, tags=minha_tag)
                    indice += 1
            indice_Pai +=1
        self.fechar_BD(wb)






#rodar = funcoes_geral()
