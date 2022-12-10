import tkinter
import tkinter.font as tkFont
from tkinter import ttk
import matplotlib.image as img
import matplotlib.pyplot as plt
from PIL import ImageTk
from ttkthemes import ThemedStyle
import Operacional
import os
import tkinter.messagebox

class my_Treeview():
    def __init__(self, master, x, y, width, height, colunas: list, pathern: bool):
        self.master = master
        #cores para personalizar sua tabela - variaveis livres
        self.bg = self.master['background']
        self.fg = 'black'
        self.selectBg = '#FFFFCD'
        self.select_fg = '#71007A'
        self.fieldBg = self.master['background']
        self.tag_normal_bg = self.bg
        self.tag_normal_fg =self.fg
        self.tag_alerta_bg = 'white'
        self.tag_alerta_fg = '#C48C00'
        self.tag_perigo_bg = 'white'
        self.tag_perigo_fg = '#8A0000'
        self.tag_ok_bg = 'white'
        self.tag_ok_fg = '#006405'
        #variaveis fixas -  não mexer nestas.
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colunas: list = colunas
        self.pathern = pathern
        self.my_tv()
        self.my_scrolls()
        self.my_style()
        self.my_tags()
    def my_tv(self):
        self.treeview = tkinter.ttk.Treeview(self.master)
        self.treeview.place(x=self.x, y=self.y, width=self.width, height=self.height)

        if self.pathern == True:
            self.treeview['columns'] = self.colunas[1:]

            self.treeview.column("#0", anchor='center')
            self.treeview.heading('#0', text= self.colunas[0])
            for item in self.colunas[1:]:
                self.treeview.column(str(item), anchor='center')
                self.treeview.heading(str(item),text=str(item).replace('_',' '))
        else:
            self.treeview['columns'] = self.colunas
            self.treeview.column("#0", width=0, stretch=0)
            for item in self.colunas:
                self.treeview.column(str(item), anchor='center')
                self.treeview.heading(str(item),text=str(item).replace('_',' '))
    def my_scrolls(self):
        self.scroll_vertical = tkinter.ttk.Scrollbar(self.master, orient='vertical')
        self.scroll_vertical.place(x=self.x+self.width, y=self.y,width=20,height=self.height)
        self.treeview['yscrollcommand'] = self.scroll_vertical.set
        self.scroll_vertical['command'] = self.treeview.yview
        self.scroll_horizontal = tkinter.ttk.Scrollbar(self.master, orient='horizontal')
        self.scroll_horizontal.place(x=self.x, y=self.y + self.height-20, width=self.width, height=20)
        self.treeview['xscrollcommand'] = self.scroll_horizontal.set
        self.scroll_horizontal['command'] = self.treeview.xview
    def my_style(self):
        self.style = tkinter.ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('Treeview',
                             background=self.bg,
                             fieldbackground=self.fieldBg,
                             foreground = self.fg,
                             rowheight=25)
        self.style.map('Treeview', background=[('selected', self.selectBg)], foreground=[('selected',self.select_fg)])
    def my_tags(self):
        self.treeview.tag_configure('normal', background=self.tag_normal_bg, foreground=self.tag_normal_fg)
        self.treeview.tag_configure('alerta', background=self.tag_alerta_bg, foreground=self.tag_alerta_fg)
        self.treeview.tag_configure('perigo', background=self.tag_perigo_bg, foreground=self.tag_perigo_fg)
        self.treeview.tag_configure('ok', background=self.tag_ok_bg, foreground=self.tag_ok_fg)
        self.treeview.tag_configure('normal2', background='#DADBEE', foreground=self.tag_normal_fg)
        self.treeview.tag_configure('alerta2', background='#DADBEE', foreground=self.tag_alerta_fg)
        self.treeview.tag_configure('perigo2', background='#DADBEE', foreground=self.tag_perigo_fg)
        self.treeview.tag_configure('ok2', background='#DADBEE', foreground=self.tag_ok_fg)
class entry_personalizado():
    def __init__(self, master: tkinter.Tk, xPixel: int, yPixel: int, width: int, height: int, nome: str, tam_Letra: int,
                 password: bool= False, tipo_de_texto: str='texto',quant_carac=20):
        #Configure cores na classe
        self.corLetra = 'black'
        self.corLinha1 = '#909090'
        self.corLinha2 = '#5100BC'       #'#21599D'
        self.string = tkinter.StringVar(master)
        self.corFundo = master['background']
        self.master = master
        self.xPixel = xPixel
        self.yPixel = yPixel
        self.widthPixel = width
        self.heightPixel = height
        self.password = password
        self.nome_Entry = nome
        self.tam_Letra = tam_Letra
        self.fonte_Class = tkFont.Font(family="Lucida Grande", size=tam_Letra)
        self.criar_Linha()
        self.criar_entry()
        self.criar_label()
        self.tipo_de_texto = tipo_de_texto
        if self.tipo_de_texto == 'senha':
            self.txt_forca = 'Escolha uma senha'
            self.lb_forca = tkinter.Label(master, text=self.txt_forca, background=master['bg'],
                                        font=self.fonte_Class)
            self.lb_forca.place(x=xPixel, y=yPixel+25, height=height)
        self.casas_decimais = 2
        self.quant_carac = quant_carac
        self.chamada_tipo_de_texto()
    def limpar_entry(self):
        self.entry.delete(0, tkinter.END)
    def bloquear_entry(self):
        self.entry.configure(state='disable')
    def liberar_entry(self):
        self.entry.configure(state='normal')
    #eventos
    def focus_entry(self,event):
        self.entry.focus()
    def escreve_entry(self,event):
            self.label_Class.place(y=self.yPixel-self.heightPixel)
            self.label_Class.configure(foreground=self.corLinha2)
            self.canvas_entry.itemconfig(self.linhaCanvas, fill=self.corLinha2,width=2)
    def verificaTexto(self,event):
        if self.tipo_de_texto == 'cpf':
            ver = True
            if len(self.string.get()) < 14:
                self.limpar_entry()
                ver = False
            if ver == True:
                listaNum = []
                resultado = ''
                for i in self.string.get():
                    if str(i) == '.': continue
                    if str(i) == '-': break
                    listaNum.append(int(i))
                digito = 0
                for i in range(len(listaNum)):
                    digito += listaNum[i] * (i + 1)
                digito = digito % 11
                if digito == 10: digito = 0
                listaNum.append(digito)
                resultado += str(digito)
                digito = 0
                for i in range(len(listaNum)):
                    digito += listaNum[i] * i
                digito = digito % 11
                if digito == 10: digito = 0
                resultado += str(digito)
                if resultado != str(self.string.get()[12:]):
                    tkinter.messagebox.showinfo('Team-29','CPF inválido!')
                    self.focus_entry('')
                    self.limpar_entry()
                    return
        if str(self.entry.get()) == '':
            self.label_Class.place(y=self.yPixel)
            self.label_Class.configure(foreground=self.corLinha1)
            self.canvas_entry.itemconfig(self.linhaCanvas, fill=self.corLinha1,width=1)
        else:
            self.label_Class.place(y=self.yPixel - self.heightPixel)
            self.label_Class.configure(foreground=self.corLinha2)
            self.canvas_entry.itemconfig(self.linhaCanvas, fill=self.corLinha2, width=2)

    def forca_senha(self, *args):
        senha = self.string.get()
        numeros = [str(x) for x in range(10)]
        letras_min = 'qwertyuiopasdfghjklçzxcvbnm'
        letras_M = letras_min.upper()
        carac_Esp = 'áàèìòùéíóúãõ!@#$%¨&*()-_+=-;:/ÁÉÍÓÚÀÈÌÒÙÃÕâêîôûÂÊÎÔÛ'
        pontos = 0
        if len(senha) == 0:
            self.txt_forca = 'Escolha uma senha'
            self.lb_forca['text'] = self.txt_forca
            return
        if len(senha) < 5:
            self.txt_forca = 'Senha muito fraca!'
            self.lb_forca['text']=self.txt_forca
            return
        if len(senha) > 8:
            pontos = 2
        elif len(senha) > 5:
            pontos = 1
        for i in numeros:
            if senha.find(str(i)) > -1:
                pontos += 1
                break
        for i in letras_min:
            if senha.find(str(i)) > -1:
                pontos += 1
                break
        for i in letras_M:
            if senha.find(str(i)) > -1:
                pontos += 1
                break
        for i in carac_Esp:
            if senha.find(str(i)) > -1:
                pontos += 3
                break
        if pontos <=2:
            self.txt_forca = 'Senha muito fraca!'
            self.lb_forca['text'] = self.txt_forca
            return
        if pontos <=3:
            self.txt_forca = 'Senha fraca'
            self.lb_forca['text'] = self.txt_forca
            return
        if pontos <=4:
            self.txt_forca = 'Senha boa'
            self.lb_forca['text'] = self.txt_forca
            return
        if pontos <= 5:
            self.txt_forca = 'Senha forte'
            self.lb_forca['text'] = self.txt_forca
            return
        if pontos <= 7:
            self.txt_forca = 'Senha muito forte!'
            self.lb_forca['text'] = self.txt_forca
            return
        if pontos >7:
            self.txt_forca = 'É uma senha, ou chave de Criptografia?'
            self.lb_forca['text'] = self.txt_forca
            return
    def val_texto(self, *args):
        if len(self.string.get()) == 0: return
        if len(self.string.get()) > self.quant_carac:
            self.entry.delete(len(self.entry.get()) - 1, tkinter.END)
            return
    def val_numero(self, *args):
        if len(self.string.get()) == 0: return
        if len(self.string.get()) > self.quant_carac:
            self.entry.delete(len(self.entry.get()) - 1, tkinter.END)
            return
        entradas = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ',']
        if self.casas_decimais == 0: entradas = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        for i in range(len(self.string.get())):
            if self.string.get()[i] not in entradas:
                self.entry.delete(i,i+1)
                return
        if self.string.get()[len(self.string.get())-1] not in entradas:
            self.entry.delete(len(self.entry.get())-1,tkinter.END)
            return
        if self.string.get()[len(self.string.get()) - 1] == ',':
            if len(self.string.get()) == 1:
                novo_texto = '0' + ','
                self.entry.delete(0, tkinter.END)
                self.entry.insert(0, novo_texto)
                return
            if self.string.get()[:len(self.string.get())-1].find(',') >-1:
                self.entry.delete(len(self.entry.get()) - 1, tkinter.END)
                return
        if self.string.get().find(',') >-1:
            if len(self.string.get()) - (self.string.get().find(',')+1) == self.casas_decimais+1:
                self.entry.delete(len(self.entry.get()) - 1, tkinter.END)
    def val_cpf(self, *args):
        if len(self.string.get()) == 0: return
        entradas = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.','-']
        if self.string.get()[len(self.string.get())-1] not in entradas:
            self.entry.delete(len(self.entry.get())-1,tkinter.END)
            return
        for i in range(len(self.string.get())): #13..25
            if self.string.get()[i] not in entradas:
                self.entry.delete(i,i+1)
                return
        if len(self.string.get()) == 15:
            self.entry.delete(len(self.entry.get()) - 1, tkinter.END)
            return
        if self.string.get()[len(self.string.get()) - 1] == '.':
            if len(self.string.get()) in [4, 8]: return
            self.entry.delete(len(self.entry.get()) - 1, tkinter.END)
            return
        if self.string.get()[len(self.string.get()) - 1] == '-':
            if len(self.string.get()) == 12: return
            self.entry.delete(len(self.entry.get()) - 1, tkinter.END)
            return
        if len(self.string.get()) in [4,8]:
            if self.string.get()[len(self.string.get()) - 1] not in ['.']:
                separador = '.'
                novo_texto = self.string.get()[:len(self.string.get()) - 1] +\
                             separador + self.string.get()[len(self.string.get())-1]
                self.entry.delete(0, tkinter.END)
                self.entry.insert(0, novo_texto)
        if len(self.string.get()) ==12:
            if self.string.get()[len(self.string.get()) - 1] not in ['-']:
                separador = '-'
                novo_texto = self.string.get()[:len(self.string.get()) - 1] + \
                             separador + self.string.get()[len(self.string.get()) - 1]
                self.entry.delete(0, tkinter.END)
                self.entry.insert(0, novo_texto)
    def val_telefone(self, *args):
        #(xx)xxxxx-xxxx
        if len(self.string.get()) == 0: return
        if len(self.string.get()) == 15:
            self.entry.delete(len(self.entry.get()) - 1, tkinter.END)
            return
        entradas = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '(',')','-']
        if self.string.get()[len(self.string.get()) - 1] not in entradas:
            self.entry.delete(len(self.entry.get()) - 1, tkinter.END)
            return
        for i in range(len(self.string.get())):
            if self.string.get()[i] not in entradas:
                self.entry.delete(i,i+1)
                return
        if  self.string.get()[len(self.string.get()) - 1] == '(':
            if len(self.string.get()) == 1: return
            self.entry.delete(len(self.entry.get()) - 1, tkinter.END)
            return
        if self.string.get()[len(self.string.get()) - 1] == ')':
            if len(self.string.get()) == 4: return
            self.entry.delete(len(self.entry.get()) - 1, tkinter.END)
            return
        if self.string.get()[len(self.string.get()) - 1] == '-':
            if len(self.string.get()) == 10: return
            self.entry.delete(len(self.entry.get()) - 1, tkinter.END)
            return
        if len(self.string.get()) in [1,4,10]:
            if self.string.get()[len(self.string.get()) - 1] not in ['(',')','-']:
                if len(self.string.get()) == 1: separador = '('
                if len(self.string.get()) == 4: separador = ')'
                if len(self.string.get()) == 10: separador = '-'
                novo_texto = self.string.get()[:len(self.string.get()) - 1] + \
                             separador + self.string.get()[len(self.string.get()) - 1]
                self.entry.delete(0, tkinter.END)
                self.entry.insert(0, novo_texto)
    def val_data(self, *args):
        if len(self.string.get()) == 0: return
        if len(self.string.get()) == 11:
            self.entry.delete(len(self.entry.get()) - 1, tkinter.END)
            return
        entradas = ['0','1','2','3','4','5','6','7','8','9','/']
        if self.string.get()[len(self.string.get())-1] not in entradas:
            self.entry.delete(len(self.entry.get())-1,tkinter.END)
            return
        for i in range(len(self.string.get())):
            if self.string.get()[i] not in entradas:
                self.entry.delete(i,i+1)
                return
        if self.string.get()[len(self.string.get())-1] ==  '/':
            if len(self.string.get()) in [3, 6]: return
            if len( self.string.get()) ==2:
                digito = self.string.get()[len(self.string.get())-2]
                novo_texto = '0'+digito + '/'
                self.entry.delete(0, tkinter.END)
                self.entry.insert(0, novo_texto)
                return
            if len( self.string.get()) ==5:
                digito = self.string.get()[len(self.string.get()) - 2]
                novo_texto = self.string.get()[:len(self.string.get()) - 2] +\
                    '0' + digito + '/'
                self.entry.delete(0,tkinter.END)
                self.entry.insert(0,novo_texto)
                return
            self.entry.delete(len(self.entry.get())-1,tkinter.END)
            return
        if len(self.string.get()) in [3,6]:
            novo_texto = self.string.get()[:len(self.string.get())-1]
            novo_texto += '/'
            novo_texto += self.string.get()[len(self.string.get())-1]
            self.entry.delete(0,tkinter.END)
            self.entry.insert(0,novo_texto)
    #funções criação de obj ou chamada de evento
    def chamada_tipo_de_texto(self):
        self.string = tkinter.StringVar(self.master) #precisa sempre resetar pra não acumular o evento trace.
        self.entry['textvariable']=self.string #redefinindo nova informação na string(acredito que a antiga limpa da memoria)
        if self.tipo_de_texto == 'data': self.string.trace('w',self.val_data)
        if self.tipo_de_texto == 'numero': self.string.trace('w',self.val_numero)
        if self.tipo_de_texto == 'texto': self.string.trace('w',self.val_texto)
        if self.tipo_de_texto == 'cpf': self.string.trace('w', self.val_cpf)
        if self.tipo_de_texto == 'telefone': self.string.trace('w', self.val_telefone)
        if self.tipo_de_texto == 'senha': self.string.trace('w', self.forca_senha)
    def criar_Linha(self):
        self.canvas_entry = tkinter.Canvas(self.master,background=self.corFundo,bd=0,highlightthickness=0,
                                    width=self.widthPixel,height=self.heightPixel)
        self.canvas_entry.place(x=self.xPixel,y=self.yPixel+15)
        self.linhaCanvas = self.canvas_entry.create_line(0, 0, self.widthPixel, 0, fill=self.corLinha1)
    def criar_entry(self):
        self.entry = tkinter.Entry(self.master,background=self.corFundo,foreground=self.corLetra,
                              width=self.widthPixel,font=self.fonte_Class, bd=0, textvariable=self.string)
        if self.password == True:
            self.entry.configure(show='●')
        self.entry.place(anchor='w',x=self.xPixel,y=self.yPixel,width=self.widthPixel,height=self.heightPixel)
        self.entry.bind('<FocusIn>',self.escreve_entry)
        self.entry.bind('<FocusOut>',self.verificaTexto)
    def criar_label(self):
        self.label_Class= tkinter.Label(self.master,background=self.corFundo,foreground=self.corLinha1,
                             font=self.fonte_Class,bd=0, text=self.nome_Entry, cursor=self.entry['cursor'])
        self.label_Class.place(anchor= 'w', x=self.xPixel,y=self.yPixel,height=self.heightPixel)
        self.label_Class.bind('<Button-1>',self.focus_entry)
class botao_de_imagens():
    def __init__(self, master: tkinter.Tk,xPixel: int, yPixel: int,imgBase: str, imgMouse: str, selecionar: bool= False, selecionado: bool=False, img_clique: str= '' ):
        self.master = master
        self.xPixel = xPixel
        self.yPixel = yPixel
        self.corFundo = master['background']
        self.selecionar = selecionar
        self.selecionado = selecionado
        self.img_clique = img_clique
        self.imgBase = imgBase
        self.imgMouse = imgMouse
        self.botao_clicado = False
        self.criar_bt()
    def mouseEntrou(self,event):
        if self.selecionado == True: return
        self.lbBase['image']=self.imgm
        self.lbBase['cursor']='hand2'
        self.lbBase.update()
    def mouseSaiu(self,event):
        if self.selecionado == True: return
        self.lbBase['image']=self.imgb
        self.lbBase['cursor'] = 'hand2'
        self.lbBase.update()
    def selecionou(self, event):
        if self.selecionar == False: return
        if self.selecionado == True: return
        self.lbBase['image']=self.imgs
        self.lbBase['cursor']='arrow'
        self.selecionado = True
    def retira_selecao(self):
        self.selecionado = False
        self.mouseSaiu('')
    def criar_bt(self):
        self.imgb = ImageTk.PhotoImage(file=self.imgBase)
        self.imgm = ImageTk.PhotoImage(file=self.imgMouse)
        if self.selecionar == True: self.imgs = ImageTk.PhotoImage(file=self.img_clique)
        self.lbBase = tkinter.Label(self.master,image=self.imgb, bd=0)
        self.cursorBase = self.lbBase['cursor']
        self.lbBase['cursor']='hand2'
        self.lbBase.place(x=self.xPixel,y=self.yPixel)
        self.lbBase.bind('<Enter>',self.mouseEntrou)
        self.lbBase.bind('<Leave>', self.mouseSaiu)
        self.lbBase.bind('<ButtonRelease-1>', self.mouseEntrou)
        self.lbBase.bind('<Button-1>', self.selecionou)
class lb_exit():
    def __init__(self,frame,x,y, tamanho=14):
        self.frame=frame
        self.x=x
        self.y=y
        self.tamanho = tamanho
        self.font = tkFont.Font(family='Lucida Grande', size=self.tamanho)
        self.criar_lb()
    def mudar_texto(self, texto):
        self.label['text'] = texto
    def mouseEntrou(self, event):
        self.label['fg']='#d60a07'
    def mouseSaiu(self,event):
        self.label['fg'] = 'black'
    def criar_lb(self):
        self.label = tkinter.Label(self.frame,background='white',fg='black',bd=0,text='Sair',
                                   font=self.font, cursor='hand2')
        self.label.place(x=self.x,y=self.y)
        self.label.bind('<Enter>', self.mouseEntrou)
        self.label.bind('<Leave>', self.mouseSaiu)
class lb_img(Operacional.funcoes_geral):
    def __init__(self, frame, id, x, y):
        self.frame = frame
        self.id = str(id)
        self.x = x
        self.y = y
        self.criar_lb()
    def bind_lb(self, event):
        img = plt.imread(f'imagens\\banco-de-imagens\\{self.id}-original.png')
        img = plt.imshow(img)
        img.axes.get_xaxis().set_visible(False)
        img.axes.get_yaxis().set_visible(False)
        plt.show()
    def criar_lb(self):
        if os.path.isfile(f'imagens\\banco-de-imagens\\{self.id}-circular.png') == False:
            self.id = 'no_image'
        self.imagem = ImageTk.PhotoImage(file=f'imagens\\banco-de-imagens\\{self.id}-circular.png')
        self.label = tkinter.Label(self.frame,bg='white',image=self.imagem, cursor='hand2')
        self.label.place(x=self.x,y=self.y)
        self.label.bind('<Button-1>', self.bind_lb)
class app_login(Operacional.funcoes_login):
    def __init__(self):
        self.Criar_tela()
        self.Criar_entrys()
        self.Criar_logo()
        self.Criar_botao()
        self.criar_Titulo()
        self.gerar_bt_inf()
        self.tela_login.mainloop()
    def Criar_tela(self):
        self.tela_login = tkinter.Tk()
        self.tela_login.geometry('800x600')
        self.tela_login.resizable(False, False)
        self.tela_login.title('Login Estoque - Team 29 Estacio')
        self.tela_login.configure(background='white')
        self.tela_login.iconbitmap('imagens\\estacio_sem_nome.ico')
    def Criar_entrys(self):
        self.usuario = entry_personalizado(master=self.tela_login, xPixel=400, yPixel=220, width=300, height=25,
                                           nome='Matricula', password=False, tam_Letra=12)

        self.senha = entry_personalizado(master=self.tela_login, xPixel=400, yPixel=285, width=300, height=25,
                                         nome='Senha', password=True, tam_Letra=12)
    def Criar_logo(self):
        self.img = ImageTk.PhotoImage(file='imagens\\logo_time.gif')
        self.logo = tkinter.Label(self.tela_login, bd=0, background=self.tela_login['background'], image=self.img)
        self.logo.place(x=-20,y=130)
    def Criar_botao(self):
        self.bt = botao_de_imagens(master=self.tela_login, xPixel=435, yPixel=350,
                                   imgBase='imagens\\login\\btBase_login.gif', imgMouse='imagens\\login\\btMouse_login.gif')
        self.bt.lbBase.bind('<Button-1>',self.verificar_login)
    def criar_Titulo(self):
        self.titulo = tkinter.Label(self.tela_login, bd=0, background=self.tela_login['background'],
                                    text='Login Central de Ferramentaria', fg='black',
                                    font=tkFont.Font(family='Lucida Grande',size=20))
        self.titulo.place(x=360,y=70)
    def bt_inf_bind(self, event):
        tkinter.messagebox.showinfo('Team-29', '''Este login é o adm padrão do projeto.
        
        Matricula: adm001
        Senha: adm123''')
    def gerar_bt_inf(self):
        self.bt_inf = botao_de_imagens(master=self.tela_login, xPixel=705, yPixel=310,
                                   imgBase='imagens\\login\\inf_base.gif',
                                   imgMouse='imagens\\login\\inf_mouse.gif')
        self.bt_inf.lbBase.bind('<Button-1>',self.bt_inf_bind)
    def abrir_appAdm(self,matricula, nome, numero, turno, equipe):
        app_Adm(matricula, nome, numero, turno, equipe)
    def abrir_appCli(self):
        app_Cli()
class app_Adm(Operacional.funcoes_adm):
    def __init__(self, matricula, nome, numero, turno, equipe):
        self.nGerar = False
        self.id =''
        self.matricula=matricula
        self.nome=nome
        self.numero=numero
        self.turno=turno
        self.equipe=equipe
        self.criar_tela()
        self.criar_controle_abas()
        self.criar_frame_login()
    def criar_tela(self):
        self.tela = tkinter.Tk()
        self.width = 1100 # cuidado com esse tamanho. Caso queira mudar, muitos codigos precisam ser recalculados.
        self.height = 700 # pode mudar livremente
        self.tela.iconbitmap('imagens\\estacio_sem_nome.ico')
        self.tela.geometry(f'{self.width}x{self.height}')
        self.tela.resizable(False,False)
        self.tela.title('Central de Ferramentaria - ADM')
        self.tela['background']='white'
    def criar_frame_filtro(self, quantos_filtros, nome_aba, tela, treeview, width, height, x, y, tamLetra, caso_pai='',
                           colunas='', tags=''):
        self.quant_f = quantos_filtros
        self.nome_aba_f = nome_aba
        self.frame_fitro = tkinter.Frame(tela,bd=0,bg=tela['bg'], highlightthickness=1)
        self.frame_fitro.place( width=width, height=height,x=x,y=y)
        self.caso_pai_f = caso_pai
        self.colunas_f = colunas
        self.tags_f = tags
        self.treev_filtro = treeview
        fonte = tkFont.Font(family="Lucida Grande", size=tamLetra)
        tam_total = width - 20
        tam_peça = int((tam_total-((quantos_filtros*30)*2))/(quantos_filtros*2))
        informacoes = treeview.treeview['columns']
        for i in range(quantos_filtros):
            if i == 0:
                self.cbb_1 = tkinter.ttk.Combobox(self.frame_fitro,background='white',font=fonte,state='readonly',
                                                  values=informacoes)
                self.cbb_1.place(width=tam_peça, height=25, x=10 + ((2 * i) * (tam_peça + 30)), y=(height / 3) + 12.5)
                self.label_1 = tkinter.Label(self.frame_fitro,background=tela['bg'],font=fonte,bd=0,
                                             text='Coluna a filtrar')
                self.label_1.place(width=tam_peça, height=25, x=10 + ((2 * i) * (tam_peça + 30)), y=(height / 3) - 12.5)
                self.cbb_1.bind('<<ComboboxSelected>>', self.bind_cbb_filtro)
                self.entry_1 = entry_personalizado(master=self.frame_fitro, xPixel=10+(((i*2)+1)*(tam_peça+30)),
                                                 yPixel=(height / 3) + 20,width= tam_peça,
                                                 height=25,nome=f'Cbb {i+1} vazia', tam_Letra=tamLetra,
                                                   password= False)
                self.esc_1_1 = tkinter.Label(self.frame_fitro,background=tela['bg'], fg='white',font=fonte,bd=0,
                                             text='>=')
                self.esc_1_1.bind('<Button-1>',self.escolha_sinal_filtro)
                self.esc_1_1.place(x=10+(((i*2)+2)*(tam_peça+30))-22.5,y=(height/3)-20, height=20)
                self.esc_1_2 = tkinter.Label(self.frame_fitro, background=tela['bg'], fg='white', font=fonte, bd=0,
                                             text='==')
                self.esc_1_2.bind('<Button-1>', self.escolha_sinal_filtro)
                self.esc_1_2.place(x=10 + (((i * 2) + 2) * (tam_peça + 30)) - 22.5, y=(height / 3), height=20)
                self.esc_1_3 = tkinter.Label(self.frame_fitro, background=tela['bg'], fg='white', font=fonte, bd=0,
                                             text='<=')
                self.esc_1_3.bind('<Button-1>', self.escolha_sinal_filtro)
                self.esc_1_3.place(x=10 + (((i * 2) + 2) * (tam_peça + 30)) - 22.5, y=(height / 3)+20, height=20)
                continue
            if i == 1:
                self.cbb_2 = tkinter.ttk.Combobox(self.frame_fitro, background='white', font=fonte,state='readonly',
                                                  values=informacoes)
                self.cbb_2.place(width=tam_peça, height=25, x=10 + ((2 * i) * (tam_peça + 30)), y=(height / 3) + 12.5)
                self.label_2 = tkinter.Label(self.frame_fitro, background=tela['bg'], font=fonte, bd=0,
                                             text='Coluna a filtrar')
                self.label_2.place(width=tam_peça, height=25, x=10 + ((2 * i) * (tam_peça + 30)), y=(height / 3) - 12.5)
                self.cbb_2.bind('<<ComboboxSelected>>', self.bind_cbb_filtro)
                self.entry_2 = entry_personalizado(master=self.frame_fitro,
                                                   xPixel=10 + (((i * 2) + 1) * (tam_peça + 30)),
                                                   yPixel=(height / 3) + 20, width=tam_peça,
                                                   height=25, nome=f'Cbb {i + 1} vazia', tam_Letra=tamLetra,
                                                   password=False)
                self.esc_2_1 = tkinter.Label(self.frame_fitro, background=tela['bg'], fg='white', font=fonte, bd=0,
                                             text='>=')
                self.esc_2_1.bind('<Button-1>', self.escolha_sinal_filtro)
                self.esc_2_1.place(x=10 + (((i * 2) + 2) * (tam_peça + 30)) - 22.5, y=(height / 3) - 20, height=20)
                self.esc_2_2 = tkinter.Label(self.frame_fitro, background=tela['bg'], fg='white', font=fonte, bd=0,
                                             text='==')
                self.esc_2_2.bind('<Button-1>', self.escolha_sinal_filtro)
                self.esc_2_2.place(x=10 + (((i * 2) + 2) * (tam_peça + 30)) - 22.5, y=(height / 3), height=20)
                self.esc_2_3 = tkinter.Label(self.frame_fitro, background=tela['bg'], fg='white', font=fonte, bd=0,
                                             text='<=')
                self.esc_2_3.bind('<Button-1>', self.escolha_sinal_filtro)
                self.esc_2_3.place(x=10 + (((i * 2) + 2) * (tam_peça + 30)) - 22.5, y=(height / 3) + 20, height=20)
                continue
            if i == 2:
                self.cbb_3 = tkinter.ttk.Combobox(self.frame_fitro, background='white', font=fonte,state='readonly',
                                                  values=informacoes)
                self.cbb_3.place(width=tam_peça, height=25, x=10 + ((2 * i) * (tam_peça + 30)), y=(height / 3) + 12.5)
                self.label_3 = tkinter.Label(self.frame_fitro, background=tela['bg'], font=fonte, bd=0,
                                             text='Coluna a filtrar')
                self.label_3.place(width=tam_peça, height=25, x=10 + ((2 * i) * (tam_peça + 30)), y=(height / 3) - 12.5)
                self.cbb_3.bind('<<ComboboxSelected>>', self.bind_cbb_filtro)
                self.entry_3 = entry_personalizado(master=self.frame_fitro,
                                                   xPixel=10 + (((i * 2) + 1) * (tam_peça + 30)),
                                                   yPixel=(height / 3) + 20, width=tam_peça,
                                                   height=25, nome=f'Cbb {i + 1} vazia', tam_Letra=tamLetra,
                                                   password=False)
                self.esc_3_1 = tkinter.Label(self.frame_fitro, background=tela['bg'], fg='white', font=fonte, bd=0,
                                             text='>=')
                self.esc_3_1.bind('<Button-1>', self.escolha_sinal_filtro)
                self.esc_3_1.place(x=10 + (((i * 2) + 2) * (tam_peça + 30)) - 22.5, y=(height / 3) - 20, height=20)
                self.esc_3_2 = tkinter.Label(self.frame_fitro, background=tela['bg'], fg='white', font=fonte, bd=0,
                                             text='==')
                self.esc_3_2.bind('<Button-1>', self.escolha_sinal_filtro)
                self.esc_3_2.place(x=10 + (((i * 2) + 2) * (tam_peça + 30)) - 22.5, y=(height / 3), height=20)
                self.esc_3_3 = tkinter.Label(self.frame_fitro, background=tela['bg'], fg='white', font=fonte, bd=0,
                                             text='<=')
                self.esc_3_3.bind('<Button-1>', self.escolha_sinal_filtro)
                self.esc_3_3.place(x=10 + (((i * 2) + 2) * (tam_peça + 30)) - 22.5, y=(height / 3) + 20, height=20)
                continue
            if i == 3:
                self.cbb_4 = tkinter.ttk.Combobox(self.frame_fitro, background='white', font=fonte,state='readonly',
                                                  values=informacoes)
                self.cbb_4.place(width=tam_peça, height=25, x=10 + ((2 * i) * (tam_peça + 30)), y=(height / 3) + 12.5)
                self.label_4 = tkinter.Label(self.frame_fitro, background=tela['bg'], font=fonte, bd=0,
                                             text='Coluna a filtrar')
                self.label_4.place(width=tam_peça, height=25, x=10 + ((2 * i) * (tam_peça + 30)), y=(height / 3) - 12.5)
                self.cbb_4.bind('<<ComboboxSelected>>', self.bind_cbb_filtro)
                self.entry_4 = entry_personalizado(master=self.frame_fitro,
                                                   xPixel=10 + (((i * 2) + 1) * (tam_peça + 30)),
                                                   yPixel=(height / 3) + 20, width=tam_peça,
                                                   height=25, nome=f'Cbb {i + 1} vazia', tam_Letra=tamLetra,
                                                   password=False)
                self.esc_4_1 = tkinter.Label(self.frame_fitro, background=tela['bg'], fg='white', font=fonte, bd=0,
                                             text='>=')
                self.esc_4_1.bind('<Button-1>', self.escolha_sinal_filtro)
                self.esc_4_1.place(x=10 + (((i * 2) + 2) * (tam_peça + 30)) - 22.5, y=(height / 3) - 20, height=20)
                self.esc_4_2 = tkinter.Label(self.frame_fitro, background=tela['bg'], fg='white', font=fonte, bd=0,
                                             text='==')
                self.esc_4_2.bind('<Button-1>', self.escolha_sinal_filtro)
                self.esc_4_2.place(x=10 + (((i * 2) + 2) * (tam_peça + 30)) - 22.5, y=(height / 3), height=20)
                self.esc_4_3 = tkinter.Label(self.frame_fitro, background=tela['bg'], fg='white', font=fonte, bd=0,
                                             text='<=')
                self.esc_4_3.bind('<Button-1>', self.escolha_sinal_filtro)
                self.esc_4_3.place(x=10 + (((i * 2) + 2) * (tam_peça + 30)) - 22.5, y=(height / 3) + 20, height=20)
                continue
            if i == 4:
                self.cbb_5 = tkinter.ttk.Combobox(self.frame_fitro, background='white', font=fonte,state='readonly',
                                                  values=informacoes)
                self.cbb_5.place(width=tam_peça, height=25, x=10 + ((2 * i) * (tam_peça + 30)), y=(height / 3) + 12.5)
                self.label_5 = tkinter.Label(self.frame_fitro, background=tela['bg'], font=fonte, bd=0,
                                             text='Coluna a filtrar')
                self.label_5.place(width=tam_peça, height=25, x=10 + ((2 * i) * (tam_peça + 30)), y=(height / 3) - 12.5)
                self.cbb_5.bind('<<ComboboxSelected>>', self.bind_cbb_filtro)
                self.entry_5 = entry_personalizado(master=self.frame_fitro,
                                                   xPixel=10 + (((i * 2) + 1) * (tam_peça + 30)),
                                                   yPixel=(height / 3) + 20, width=tam_peça,
                                                   height=25, nome=f'Cbb {i + 1} vazia', tam_Letra=tamLetra,
                                                   password=False)
                self.esc_5_1 = tkinter.Label(self.frame_fitro, background=tela['bg'], fg='white', font=fonte, bd=0,
                                             text='>=')
                self.esc_5_1.bind('<Button-1>', self.escolha_sinal_filtro)
                self.esc_5_1.place(x=10 + (((i * 2) + 2) * (tam_peça + 30)) - 22.5, y=(height / 3) - 20, height=20)
                self.esc_5_2 = tkinter.Label(self.frame_fitro, background=tela['bg'], fg='white', font=fonte, bd=0,
                                             text='==')
                self.esc_5_2.bind('<Button-1>', self.escolha_sinal_filtro)
                self.esc_5_2.place(x=10 + (((i * 2) + 2) * (tam_peça + 30)) - 22.5, y=(height / 3), height=20)
                self.esc_5_3 = tkinter.Label(self.frame_fitro, background=tela['bg'], fg='white', font=fonte, bd=0,
                                             text='<=')
                self.esc_5_3.bind('<Button-1>', self.escolha_sinal_filtro)
                self.esc_5_3.place(x=10 + (((i * 2) + 2) * (tam_peça + 30)) - 22.5, y=(height / 3) + 20, height=20)
        self.bt_filtro = botao_de_imagens(master=self.frame_fitro,xPixel=width-230, yPixel=height-55,
                                          imgBase='imagens\\filtro\\bt_filtro_base.gif',
                                          imgMouse='imagens\\filtro\\bt_filtro_mouse.gif')
        self.bt_filtro.lbBase.bind('<Button-1>',self.carregar_tabela_filtro)
    def gerar_aba_treeview(self):
        self.frame_treeview = tkinter.Frame(self.tela, background='white',highlightthickness=1)
        self.frame_treeview.place(x=0,y=500,width=self.width,height=200)
    def criar_frame_login(self):
        self.frame_login = tkinter.Frame(self.tela,background='white',highlightthickness=1)
        self.frame_login.place(x=0,y=0,width=self.width,height=100)
        self.lb_img = lb_img(frame=self.frame_login,id=self.matricula,x=10,y=0)
        self.estilo = tkFont.Font(family='Lucida Grande', size=12)
        self.lb_nome = tkinter.Label(self.frame_login,bd=0,background='white', text=f'Nome: {self.nome}',
                                     font=self.estilo)
        self.lb_nome.place(x=130,y=10)
        self.lb_matricula = tkinter.Label(self.frame_login,bd=0,background='white', text=f'ID: {self.matricula}',
                                     font=self.estilo)
        self.lb_matricula.place(x=130, y=30)
        self.lb_equipe = tkinter.Label(self.frame_login, bd=0, background='white', text=f'Equipe: {self.equipe}',
                                          font=self.estilo)
        self.lb_equipe.place(x=130, y=50)
        self.lb_turno = tkinter.Label(self.frame_login, bd=0, background='white', text=f'Turno: {self.turno}',
                                       font=self.estilo)
        self.lb_turno.place(x=130, y=70)
        self.lb_numero = tkinter.Label(self.frame_login, bd=0, background='white', text=f'Numero: {self.numero}',
                                       font=self.estilo)
        self.lb_numero.place(x=130, y=70)
        self.logout = lb_exit(self.frame_login,1020,20,14)
        self.logout.mudar_texto('Logout')
        self.logout.label.bind('<Button-1>', self.abrir_login)
    def chamar_login(self):
        app_login()
    def gerar_obj_notificacoes(self):
        self.carregar_cabecalho_treeview('pedidos',colunas=[1,2,3,4,5,6,7,8,9,10,11])
        self.treev_principal = my_Treeview(master=self.frame_treeview,x=0,y=0,width=self.width-20,height=200,
                                           colunas=self.cabecalho,pathern=True)
        self.carregar_tabela_com_codigo(nome_aba='pedidos',caso_pai=[3,'pedido'],colunas=[1,2,3,4,5,6,7,8,9,10,11],
                                        treeview=self.treev_principal,filtro=False,
                                        tags=[[6,'espera-alerta'],[7,'aceito-ok','pendente-alerta','negado-perigo']])
        self.criar_frame_filtro(quantos_filtros=4, nome_aba='pedidos',treeview=self.treev_principal, tela=self.tela,
                                width=self.width, height=150, x=0, y=350, tamLetra=10,caso_pai=[3,'pedido'],
                                colunas=[1,2,3,4,5,6,7,8,9,10,11],
                                tags=[[6,'espera-alerta'],[7,'aceito-ok','pendente-alerta','negado-perigo']])
        self.criar_frame_interacao_bd()
        self.treev_principal.treeview.bind('<<TreeviewSelect>>', self.select_tree)
    def evento_tree_not(self):
        if str(self.treev_principal.treeview.selection()[0]).find('_'):
            self.iid = str(self.treev_principal.treeview.selection()[0])[
                  str(self.treev_principal.treeview.selection()[0]).find('_')+1:]
        else: self.iid = self.treev_principal.treeview.selection()[0]
        self.codigo_selecionado=list(self.treev_principal.treeview.item(self.iid).values())[0]
        id = list(self.treev_principal.treeview.item(self.iid).values())[0][:str(list(self.treev_principal.treeview.item(self.iid).values())[0]).find('_')]
        nome_tec = list(self.treev_principal.treeview.item(self.iid).values())[2][0]
        self.data_pedido = list(self.treev_principal.treeview.item(self.iid).values())[2][6]
        self.respondido = list(self.treev_principal.treeview.item(self.iid).values())[2][4]
        self.id_ferramenta = str(list(self.treev_principal.treeview.item(self.iid).values())[2][2])

        nome_f, fab_f, numb_f  = self.textos_ferramenta(id=self.id_ferramenta[:self.id_ferramenta.find('-')],nome_aba='Tipos')
        self.id_ferramenta = self.id_ferramenta[:self.id_ferramenta.find('-')]
        self.lb_tec = lb_img(frame=self.frame_interacao,id=id,x=240,y=50)
        self.nome_tec = tkinter.Label(self.frame_interacao,background='white', bd=0,text=nome_tec,font=self.estilo)
        self.nome_tec.place(x=350,y=60)
        self.lb_ferr = lb_img(frame=self.frame_interacao, id=self.id_ferramenta, x=560, y=50)
        self.nome_ferr = tkinter.Label(self.frame_interacao, background='white', bd=0, text=nome_f, font=self.estilo)
        self.nome_ferr.place(x=670, y=60)
        self.nome_fab = tkinter.Label(self.frame_interacao, background='white', bd=0, text=fab_f, font=self.estilo)
        self.nome_fab.place(x=670, y=80)
        self.lb_Numb = tkinter.Label(self.frame_interacao, background='white', bd=0, text=numb_f, font=self.estilo)
        self.lb_Numb.place(x=670, y=100)
    def evento_tree_acao_estoque(self):
        if str(self.treev_principal.treeview.selection()[0]).find('_'):
            self.iid = str(self.treev_principal.treeview.selection()[0])[
                       str(self.treev_principal.treeview.selection()[0]).find('_') + 1:]
        else:
            self.iid = self.treev_principal.treeview.selection()[0]
        self.iid_linha = self.treev_principal.treeview.selection()[0]
        self.codigo_selecionado = list(self.treev_principal.treeview.item(self.iid).values())[0]
        id = list(self.treev_principal.treeview.item(self.iid).values())[0][
             :str(list(self.treev_principal.treeview.item(self.iid).values())[0]).find('-')]
        nome_tec = list(self.treev_principal.treeview.item(self.iid_linha).values())[2][0]
        self.data_pedido = list(self.treev_principal.treeview.item(self.iid).values())[2][5]
        self.acao = list(self.treev_principal.treeview.item(self.iid).values())[2][4]
        self.id_ferramenta = self.codigo_selecionado

        nome_f, fab_f, numb_f = self.textos_ferramenta(id=self.id_ferramenta[:self.id_ferramenta.find('-')],
                                                       nome_aba='Tipos')
        self.id_ferramenta = self.id_ferramenta[:self.id_ferramenta.find('-')]
        self.lb_tec = lb_img(frame=self.frame_interacao, id=nome_tec, x=240, y=50)
        self.nome_tec = tkinter.Label(self.frame_interacao, background='white', bd=0, text=nome_tec, font=self.estilo)
        self.nome_tec.place(x=350, y=60)
        self.lb_ferr = lb_img(frame=self.frame_interacao, id=self.id_ferramenta, x=560, y=50)
        self.nome_ferr = tkinter.Label(self.frame_interacao, background='white', bd=0, text=nome_f, font=self.estilo)
        self.nome_ferr.place(x=670, y=60)
        self.nome_fab = tkinter.Label(self.frame_interacao, background='white', bd=0, text=fab_f, font=self.estilo)
        self.nome_fab.place(x=670, y=80)
        self.lb_Numb = tkinter.Label(self.frame_interacao, background='white', bd=0, text=numb_f, font=self.estilo)
        self.lb_Numb.place(x=670, y=100)
    def evento_tree_dash(self):
        print('fazer')
    def evento_tree_compra_descarte(self):
        print('fazer')
    def evento_tree_cadastro(self):
        self.iid = self.treev_principal.treeview.selection()[0]
        self.id = list(self.treev_principal.treeview.item(self.iid).values())[2][0]
        if self.cbb_aba_cadastro.get() == 'ferramentas':
            nome_ferr = f'Nome: {list(self.treev_principal.treeview.item(self.iid).values())[2][1]}'
            nome_fab = f'Fabricante: {list(self.treev_principal.treeview.item(self.iid).values())[2][3]}'
            part_numb = f'Part Number: {list(self.treev_principal.treeview.item(self.iid).values())[2][5]}'
        else:
            nome_ferr = f'Nome: {list(self.treev_principal.treeview.item(self.iid).values())[2][2]}'
            nome_fab = f'CPF: {list(self.treev_principal.treeview.item(self.iid).values())[2][1]}'
            part_numb = f'Telefone: {list(self.treev_principal.treeview.item(self.iid).values())[2][3]}'

        self.lb_ferr = lb_img(frame=self.frame_interacao, id=self.id, x=560, y=50)
        self.nome_ferr_lb = tkinter.Label(self.frame_interacao, background='white', bd=0, text=nome_ferr, font=self.estilo)
        self.nome_ferr_lb.place(x=670, y=60)
        self.nome_fab_lb = tkinter.Label(self.frame_interacao, background='white', bd=0, text=nome_fab, font=self.estilo)
        self.nome_fab_lb.place(x=670, y=80)
        self.lb_Numb = tkinter.Label(self.frame_interacao, background='white', bd=0, text=part_numb, font=self.estilo)
        self.lb_Numb.place(x=670, y=100)

    def criar_frame_interacao_bd(self, y=150):
        self.frame_interacao = tkinter.Frame(self.tela, background=self.tela['bg'], highlightthickness=1)
        self.frame_interacao.place(x=0,y=y,width=self.width,height=200)
    def botoes_frame_interacao(self, inf='sem inf'):
        for item in self.frame_interacao.winfo_children():
            item.destroy()
        if self.nGerar == True: return
        self.bt_Responder = botao_de_imagens(master=self.frame_interacao, xPixel=20, yPixel=70,
                                                  imgBase='imagens\\frame-informacao\\adicionar_base.gif',
                                                  imgMouse='imagens\\frame-informacao\\adicionar_mouse.gif')
        self.bt_Responder.lbBase.bind('<Button-1>',self.evento_add)
        '''
        if self.matricula.find('adm') > -1:
            self.bt_Editar = botao_de_imagens(master=self.frame_interacao, xPixel=20, yPixel=80,
                                                    imgBase='imagens\\frame-informacao\\editar_base.gif',
                                                    imgMouse='imagens\\frame-informacao\\editar_mouse.gif')
        if inf == '':
            self.bt_Deletar = botao_de_imagens(master=self.frame_interacao, xPixel=20, yPixel=140,
                                                    imgBase='imagens\\frame-informacao\\deletar_base.gif',
                                                    imgMouse='imagens\\frame-informacao\\deletar_mouse.gif')
        '''
    def criar_frame_to_bd(self):
        self.frame_to_BD = tkinter.Frame(self.tela, background='white', highlightthickness=1)
        self.frame_to_BD.place(x=0, y=100, width=self.width, height=600)
        self.lb_exit_fbd = lb_exit(self.frame_to_BD, 1060, 0)
        self.lb_exit_fbd.label.bind('<Button-1>', self.fechar_frame_to_BD)
    def bts_frameBD_not(self):

        self.cab_label_matricula = tkinter.Label(self.frame_to_BD,bd=0,bg='#FFFFFF', font=self.estilo, text='ID')
        self.cab_label_matricula.place(x=20, y=40,height=20)
        self.label_matricula = tkinter.Label(self.frame_to_BD,bd=0,bg='#c3c3c3',font=self.estilo, text=self.matricula)
        self.label_matricula.place(x=20, y=60,height=20)
        self.cab_label_locutor = tkinter.Label(self.frame_to_BD, bd=0, bg='#FFFFFF', font=self.estilo, text='Locutor')
        self.cab_label_locutor.place(x=100, y=40, height=20)
        self.label_locutor = tkinter.Label(self.frame_to_BD, bd=0, bg='#c3c3c3', font=self.estilo,
                                             text=self.nome)
        self.label_locutor.place(x=100, y=60, height=20)
        self.cab_label_cod = tkinter.Label(self.frame_to_BD, bd=0, bg='#FFFFFF', font=self.estilo, text='Código')
        self.cab_label_cod.place(x=950, y=40, height=20)
        self.label_cod = tkinter.Label(self.frame_to_BD, bd=0, bg='#FFFFFF', font=self.estilo,background='#c3c3c3',
                                       text=self.codigo_selecionado)
        self.label_cod.place(x=950, y=60, height=20)
        #entrys liberadas
        self.entry_Mensagem = entry_personalizado(master=self.frame_to_BD, xPixel=20, yPixel=120, width=300,
                                                  height=20, nome='Mensagem', tam_Letra=12,
                 password= False, tipo_de_texto='texto',quant_carac=60)
        self.cab_conclusao = tkinter.Label(self.frame_to_BD, bd=0, bg='white', font=self.estilo, text='Conclusão')
        self.cab_conclusao.place(x=340, y=100, height=20)
        self.cbb_conclusao = ttk.Combobox(self.frame_to_BD, values=['aceito', 'pendente', 'negado'], background='white',
                                          state='readonly')
        self.cbb_conclusao.place(x=340, y=120, width=100, height=20)
        self.entry_Data_liberacao = entry_personalizado(master=self.frame_to_BD, xPixel=460, yPixel=120, width=140,
                                                  height=20, nome='Data da Reserva', tam_Letra=12,
                                                  password=False, tipo_de_texto='data', quant_carac=60)
        self.entry_Data_liberacao.bloquear_entry()
        self.entry_tempo_limite = entry_personalizado(master=self.frame_to_BD, xPixel=620, yPixel=120, width=140,
                                                        height=20, nome='Tempo liberado', tam_Letra=12,
                                                        password=False, tipo_de_texto='numero', quant_carac=60)
        self.entry_tempo_limite.casas_decimais = 0
        self.entry_tempo_limite.bloquear_entry()
        self.cbb_conclusao.bind('<<ComboboxSelected>>',self.mostrar_entry_data)
        self.bt_enviar_resposta = botao_de_imagens(master=self.frame_to_BD,xPixel=760,yPixel=120,
                                                   imgBase='imagens\\frame-informacao\\bt_enviar_base.gif',
                                                   imgMouse='imagens\\frame-informacao\\bt_enviar_mouse.gif')
        self.bt_enviar_resposta.lbBase.bind('<Button-1>',self.enviarBD_notificacoes)
        if self.bt_press == 'add': return
    def bts_frameBD_acao_estoque(self):
        print('fazer')
    def gerar_componentes_compra_descarte(self):
        self.label_imgCD = lb_img(self.frame_to_BD,str(self.cbb_id.get()),20,90)
        self.lb_nomeF = tkinter.Label(self.frame_to_BD,background='white', font=self.estilo,
                                      text=f'Nome: {self.inf_ferramenta[1]}')
        self.lb_FabF = tkinter.Label(self.frame_to_BD, background='white', font=self.estilo,
                                      text=f'Fabricante: {self.inf_ferramenta[3]}')
        self.lb_materialF = tkinter.Label(self.frame_to_BD, background='white', font=self.estilo,
                                      text=f'Material: {self.inf_ferramenta[9]}')
        self.lb_partNumberF = tkinter.Label(self.frame_to_BD, background='white', font=self.estilo,
                                      text=f'Part Number: {self.inf_ferramenta[5]}')
        self.lb_tamanhoF = tkinter.Label(self.frame_to_BD, background='white', font=self.estilo,
                                            text=f'Tamanho: {str(self.inf_ferramenta[6])} {str(self.inf_ferramenta[7])}')
        self.lb_nomeF.place(x=140,y=90,height=20)
        self.lb_FabF.place(x=140,y=110,height=20)
        self.lb_materialF.place(x=140,y=130,height=20)
        self.lb_partNumberF.place(x=140,y=150,height=20)
        self.lb_tamanhoF.place(x=140, y=170, height=20)

        self.entry_quantidade = entry_personalizado(master=self.frame_to_BD, xPixel=20, yPixel=230, width=180,
                                                      height=20, nome='Quantidade', tam_Letra=12,
                                                      password=False, tipo_de_texto='numero', quant_carac=20)
        self.entry_quantidade.casas_decimais = 0
        self.entry_valorUn = entry_personalizado(master=self.frame_to_BD, xPixel=20, yPixel=280, width=180,
                                                      height=20, nome='Valor unitário', tam_Letra=12,
                                                      password=False, tipo_de_texto='numero', quant_carac=20)
        self.entry_data_compra = entry_personalizado(master=self.frame_to_BD, xPixel=20, yPixel=330, width=180,
                                                      height=20, nome='Data de compra', tam_Letra=12,
                                                      password=False, tipo_de_texto='data', quant_carac=20)
        self.entry_mensagem = entry_personalizado(master=self.frame_to_BD, xPixel=20, yPixel=380, width=540,
                                                     height=20, nome='Mensagem', tam_Letra=12,
                                                     password=False, tipo_de_texto='texto', quant_carac=60)
        self.bt_enviar_resposta = botao_de_imagens(master=self.frame_to_BD, xPixel=760, yPixel=230,
                                                  imgBase='imagens\\frame-informacao\\bt_enviar_base.gif',
                                                  imgMouse='imagens\\frame-informacao\\bt_enviar_mouse.gif')
        self.bt_enviar_resposta.lbBase.bind('<Button-1>', self.enviarBD_Compra)
    def gerar_cab_frameBD_compra_descarte(self):
        self.cab_cbbFerramenta = tkinter.Label(self.frame_to_BD, background='white', font=self.estilo,
                                               text='Nome ferramenta')
        self.cab_cbbFab = tkinter.Label(self.frame_to_BD, background='white', font=self.estilo,
                                        text='Fabrica')
        self.cab_id = tkinter.Label(self.frame_to_BD, background='white', font=self.estilo,
                                    text='ID')
        self.cab_cbbFerramenta.place(x=20, y=40, width=270, height=20)
        self.cab_cbbFab.place(x=310, y=40, width=135, height=20)
        self.cab_id.place(x=455, y=40, width=50, height=20)
    def bts_frameBD_compra_descarte(self):
        self.criar_frame_to_bd()
        self.frame_to_BD.place(height=500, y=200)
        self.lb_exit_fbd.label.destroy()
        self.gerar_cab_frameBD_compra_descarte()
        self.string_cbbNomeF = tkinter.StringVar(self.frame_to_BD)
        self.string_cbbFab = tkinter.StringVar(self.frame_to_BD)
        self.string_cbbId = tkinter.StringVar(self.frame_to_BD)
        self.cbb_nomeFerramenta = tkinter.ttk.Combobox(self.frame_to_BD,state='readonly',background='white',
                                                 textvariable=self.string_cbbNomeF, font=self.estilo)
        self.cbb_nomeFerramenta.place(x=20,y=60,height=20,width=270)
        self.carregar_nomeFerramentas()
        self.cbb_fabricantes = tkinter.ttk.Combobox(self.frame_to_BD,state='readonly', background='white',
                                                   textvariable=self.string_cbbFab, font=self.estilo)
        self.cbb_fabricantes.place(x=310,y=60,width=135, height=20)
        self.cbb_id = tkinter.ttk.Combobox(self.frame_to_BD,state='readonly', background='white',
                                           textvariable=self.string_cbbId, font= self.estilo)
        self.cbb_id.place(x=455,y=60,height=20,width=50)
        self.cbb_nomeFerramenta.bind('<<ComboboxSelected>>',self.carregar_cbb_fabricantes)
        self.cbb_fabricantes.bind('<<ComboboxSelected>>', self.carregar_cbb_id)
        self.cbb_id.bind('<<ComboboxSelected>>', self.verificar_cbbs_compra_descarte)

    def bts_frameBD_cadastro(self):

        if self.cbb_aba_cadastro.get() == 'ferramentas':
            self.entry_codigo = entry_personalizado(master=self.frame_to_BD, xPixel=20, yPixel=70, width=180,
                                                      height=20, nome='ID ferramenta', tam_Letra=12,
                                                      password=False, tipo_de_texto='numero', quant_carac=20)
            self.entry_codigo.entry.bind('<FocusOut>',self.verificaId_ferramentas)
            self.entry_codigo.casas_decimais = 0
            self.entry_nomeFerr = entry_personalizado(master=self.frame_to_BD, xPixel=20, yPixel=120, width=270,
                                                    height=20, nome='Nome ferramenta', tam_Letra=12,
                                                    password=False, tipo_de_texto='texto', quant_carac=25)
            self.entry_descricao = entry_personalizado(master=self.frame_to_BD, xPixel=20, yPixel=170, width=600,
                                                    height=20, nome='Descrição da ferramenta', tam_Letra=12,
                                                    password=False, tipo_de_texto='texto', quant_carac=60)
            self.entry_fabricante = entry_personalizado(master=self.frame_to_BD, xPixel=20, yPixel=220, width=270,
                                                       height=20, nome='Fabricante', tam_Letra=12,
                                                       password=False, tipo_de_texto='texto', quant_carac=30)
            self.entry_voltagem = entry_personalizado(master=self.frame_to_BD, xPixel=20, yPixel=270, width=135,
                                                        height=20, nome='Voltagem de uso', tam_Letra=12,
                                                        password=False, tipo_de_texto='texto', quant_carac=15)
            self.entry_partNumb = entry_personalizado(master=self.frame_to_BD, xPixel=20, yPixel=320, width=270,
                                                        height=20, nome='Part Number', tam_Letra=12,
                                                        password=False, tipo_de_texto='numero', quant_carac=25)
            self.entry_tamanho = entry_personalizado(master=self.frame_to_BD, xPixel=20, yPixel=370, width=180,
                                                      height=20, nome='Tamanho', tam_Letra=12,
                                                      password=False, tipo_de_texto='numero', quant_carac=20)
            self.entry_unMedida = entry_personalizado(master=self.frame_to_BD, xPixel=20, yPixel=420, width=180,
                                                     height=20, nome='Unidade de medida', tam_Letra=12,
                                                     password=False, tipo_de_texto='texto', quant_carac=15)
            self.entry_tipoFerramenta = entry_personalizado(master=self.frame_to_BD, xPixel=20, yPixel=470, width=180,
                                                       height=20, nome='Tipo de ferramenta', tam_Letra=12,
                                                       password=False, tipo_de_texto='texto', quant_carac=15)
            self.entry_materialFerr = entry_personalizado(master=self.frame_to_BD, xPixel=20, yPixel=520, width=180,
                                                            height=20, nome='Material da Ferramenta', tam_Letra=12,
                                                            password=False, tipo_de_texto='texto', quant_carac=15)
            self.entry_tempoReserva = entry_personalizado(master=self.frame_to_BD, xPixel=20, yPixel=570, width=300,
                                                          height=20, nome='Tempo máximo de reserva', tam_Letra=12,
                                                          password=False, tipo_de_texto='numero', quant_carac=15)
            self.entry_tempoReserva.casas_decimais = 0
            self.entry_partNumb.casas_decimais = 0
            self.bt_enviar_resposta = botao_de_imagens(master=self.frame_to_BD, xPixel=760, yPixel=150,
                                                       imgBase='imagens\\frame-informacao\\bt_enviar_base.gif',
                                                       imgMouse='imagens\\frame-informacao\\bt_enviar_mouse.gif')
            self.bt_enviar_resposta.lbBase.bind('<Button-1>', self.enviarBD_ferramentas)
            self.lb_caminho = tkinter.Label(self.frame_to_BD,text='S/N',background='#c3c3c3', foreground='#E25351',
                                            font=self.estilo)
            self.lb_caminho.place(y=120,x=300,width=440,height=20)
            self.bt_enviar_resposta = botao_de_imagens(master=self.frame_to_BD, xPixel=760, yPixel=105,
                                                       imgBase='imagens\\frame-informacao\\cfoto_base.gif',
                                                       imgMouse='imagens\\frame-informacao\\cfoto_mouse.gif')
            self.bt_enviar_resposta.lbBase.bind('<Button-1>', self.pegar_imagemCadastroTec)
            return
        id = self.nova_matricula()
        self.lb_matricula = tkinter.Label(self.frame_to_BD, text=id, background='#c3c3c3',
                                        font=self.estilo)
        self.lb_matricula.place(y=30, x=20, height=20,width=9*len('Matricula única:'))
        self.lb_matricula_c = tkinter.Label(self.frame_to_BD, text='Matricula única:', background='#c3c3c3',
                                            font=self.estilo)
        self.lb_matricula_c.place(y=10, x=20, height=20, width=9*len('Matricula única:'))
        self.entry_senha = entry_personalizado(master=self.frame_to_BD, xPixel=20, yPixel=90, width=180,
                                                height=20, nome='Senha', tam_Letra=12,
                                                password=True, tipo_de_texto='senha', quant_carac=20)
        self.entry_senha2 = entry_personalizado(master=self.frame_to_BD, xPixel=230, yPixel=90, width=180,
                                                height=20, nome='Verificar senha', tam_Letra=12,
                                                password=True, tipo_de_texto='texto', quant_carac=20)
        self.entry_senha.lb_forca.lift()
        self.entry_senha2.entry.bind('<FocusOut>', self.verifica_senha)
        self.entry_cpf = entry_personalizado(master=self.frame_to_BD, xPixel=20, yPixel=170, width=150,
                                             height=20, nome='CPF', tam_Letra=12,
                                             password=False, tipo_de_texto='cpf', quant_carac=20)
        self.entry_nome = entry_personalizado(master=self.frame_to_BD, xPixel=20, yPixel=220, width=360,
                                                height=20, nome='Nome', tam_Letra=12,
                                                password=False, tipo_de_texto='texto', quant_carac=40)
        self.entry_telefone = entry_personalizado(master=self.frame_to_BD, xPixel=20, yPixel=270, width=180,
                                                height=20, nome='Telefone', tam_Letra=12,
                                                password=False, tipo_de_texto='telefone', quant_carac=20)
        self.lb_turno = tkinter.Label(self.frame_to_BD, text=id, background='white',
                                          font=self.estilo)
        self.lb_turno.place(x=20,y=300,height=20,width=120)
        self.strT = tkinter.StringVar()
        self.cbb_turno = tkinter.ttk.Combobox(self.frame_to_BD, state='readonly', background='white', font=self.estilo,
                                              textvariable=self.strT, values=['manhã','tarde','noite'])
        self.cbb_turno.current(1)
        self.cbb_turno.place(y=320,x=20,width=120,height=20)
        self.entry_nomeEquipe = entry_personalizado(master=self.frame_to_BD, xPixel=20, yPixel=370, width=270,
                                                height=20, nome='Nome da equipe', tam_Letra=12,
                                                password=False, tipo_de_texto='texto', quant_carac=30)
        self.bt_enviar_resposta = botao_de_imagens(master=self.frame_to_BD, xPixel=760, yPixel=70,
                                                   imgBase='imagens\\frame-informacao\\bt_enviar_base.gif',
                                                   imgMouse='imagens\\frame-informacao\\bt_enviar_mouse.gif')
        self.bt_enviar_resposta.lbBase.bind('<Button-1>', self.enviarBD_tecnicos)
        self.lb_caminho = tkinter.Label(self.frame_to_BD, text='S/N', background='#c3c3c3', foreground='#E25351',
                                        font=self.estilo)
        self.lb_caminho.place(y=40, x=300, width=440, height=20)
        self.bt_enviar_resposta = botao_de_imagens(master=self.frame_to_BD, xPixel=760, yPixel=25,
                                                   imgBase='imagens\\frame-informacao\\cfoto_base.gif',
                                                   imgMouse='imagens\\frame-informacao\\cfoto_mouse.gif')
        self.bt_enviar_resposta.lbBase.bind('<Button-1>', self.pegar_imagemCadastroTec)
    def criar_binds_notificacao(self):
        if self.bt_Responder == None: return
    def gerar_obj_acao_estoque(self):
        self.carregar_cabecalho_treeview('acoes estoque', colunas=[1, 2, 3, 4, 5, 6, 7])
        self.treev_principal = my_Treeview(master=self.frame_treeview, x=0, y=0, width=self.width - 20, height=200,
                                           colunas=self.cabecalho, pathern=True)
        self.carregar_tabela_com_codigo(nome_aba='acoes estoque', caso_pai=[6, 'compra'],
                                        colunas=[1, 2, 3, 4, 5, 6, 7],
                                        treeview=self.treev_principal, filtro=False,
                                        tags=[[6, 'defeito-alerta'],
                                              [6, 'devolução-ok', 'retirada-alerta', 'manutenção-perigo']])
        self.criar_frame_filtro(quantos_filtros=4, nome_aba='acoes estoque', treeview=self.treev_principal, tela=self.tela,
                                width=self.width, height=150, x=0, y=350, tamLetra=10, caso_pai=[6, 'compra'],
                                colunas=[1, 2, 3, 4, 5, 6, 7],
                                tags=[[6, 'defeito-alerta'],
                                      [6, 'devolução-ok', 'retirada-alerta', 'manutenção-perigo']])
        self.criar_frame_interacao_bd()
        self.treev_principal.treeview.bind('<<TreeviewSelect>>', self.select_tree)
    def gerar_obj_dash(self):
        return print('fazer dash')
    def gerar_obj_compra_descarte(self):
        self.bts_frameBD_compra_descarte()
    def gerar_obj_cadastro(self):
        self.str_cbb_aba_var = tkinter.StringVar()
        self.frame_aba_cad = tkinter.Frame(self.tela, bd=0, background='white')
        self.frame_aba_cad.place(x=0, y=150, height=20, width=self.width)
        self.cbb_aba_cadastro = ttk.Combobox(self.frame_aba_cad, values=['tecnicos', 'ferramentas'], state='readonly',
                                             background='white', textvariable=self.str_cbb_aba_var)
        self.cbb_aba_cadastro.current(1)
        self.cbb_aba_cadastro.place(x=20, y=0, height=20, width=120)
        self.cbb_aba_cadastro.bind('<<ComboboxSelected>>',self.escolher_aba_cadastro)
        self.escolher_aba_cadastro('')



    def carregar_aba_cad_selecionada(self,nome_aba,colunas,tags):
        self.carregar_cabecalho_treeview(nome_aba=nome_aba, colunas=colunas)
        self.gerar_aba_treeview()
        self.treev_principal = my_Treeview(master=self.frame_treeview, x=0, y=0, width=self.width - 20, height=200,
                                           colunas=self.cabecalho, pathern=False)
        self.carregar_tabela(nome_aba,colunas=colunas, treeview=self.treev_principal, filtro=False, tags=tags)
        self.criar_frame_interacao_bd(y=170)
        self.botoes_frame_interacao()
        self.respondido = 'espera'
        self.treev_principal.treeview.bind('<<TreeviewSelect>>', self.select_tree)
    def criar_controle_abas(self):

        self.frame_abas = tkinter.Frame(self.tela, highlightthickness=1)
        self.frame_abas['bg']='white'
        self.frame_abas.place(x=0,y=100,width=self.width, height=50)
        self.bt_notificacoes = botao_de_imagens(master=self.frame_abas,xPixel=10, yPixel=0,
                                                imgBase='imagens\\adm\\botoes\\bt_notificacoes_base.gif',
                                                imgMouse='imagens\\adm\\botoes\\bt_notificacoes_mouse.gif',
                                                selecionar=True,
                                                img_clique='imagens\\adm\\botoes\\bt_notificacoes_sel.gif' )
        self.bt_acao_estoque = botao_de_imagens(master=self.frame_abas, xPixel=230, yPixel=0,
                                                imgBase='imagens\\adm\\botoes\\bt_situacao_base.gif',
                                                imgMouse='imagens\\adm\\botoes\\bt_situacao_mouse.gif',
                                                selecionar=True,
                                                img_clique='imagens\\adm\\botoes\\bt_situacao_sel.gif')
        self.bt_dash = botao_de_imagens(master=self.frame_abas, xPixel=450, yPixel=0,
                                                imgBase='imagens\\adm\\botoes\\bt_dash_base.gif',
                                                imgMouse='imagens\\adm\\botoes\\bt_dash_mouse.gif',
                                                selecionar=True,
                                                img_clique='imagens\\adm\\botoes\\bt_dash_sel.gif')
        self.bt_compra_descarte = botao_de_imagens(master=self.frame_abas, xPixel=670, yPixel=0,
                                                imgBase='imagens\\adm\\botoes\\bt_cd_base.gif',
                                                imgMouse='imagens\\adm\\botoes\\bt_cd_mouse.gif',
                                                selecionar=True,
                                                img_clique='imagens\\adm\\botoes\\bt_cd_sel.gif')
        self.bt_cadastro = botao_de_imagens(master=self.frame_abas, xPixel=890, yPixel=0,
                                                imgBase='imagens\\adm\\botoes\\bt_cad_base.gif',
                                                imgMouse='imagens\\adm\\botoes\\bt_cad_mouse.gif',
                                                selecionar=True,
                                                img_clique='imagens\\adm\\botoes\\bt_cad_sel.gif')
        for i in self.frame_abas.winfo_children():  #esse loop define pra todo o menu o mesmo evento
            i.bind('<Button-1>', self.clicar_menu)
    def bts_frameBD_dash(self):
        return
class app_Cli():
    def __init__(self):
        print('fazer')
