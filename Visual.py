import tkinter
import tkinter.font as tkFont
from tkinter import ttk
from PIL import ImageTk
from ttkthemes import ThemedStyle
import Operacional


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
            self.treeview.column("#0", width=0, stretch=NO)
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
    def __init__(self, master: tkinter.Tk, xPixel: int, yPixel: int, width: int, height: int, nome: str, tam_Letra: int, password: bool= False):
        #Configure cores na classe
        self.corLetra = 'black'
        self.corLinha1 = '#909090'
        self.corLinha2 = '#5100BC'       #'#21599D'

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
    def focus_entry(self,event):
        self.entry.focus()
    def escreve_entry(self,event):
            self.label_Class.place(y=self.yPixel-self.heightPixel)
            self.label_Class.configure(foreground=self.corLinha2, text=self.nome_Entry)
            self.canvas_entry.itemconfig(self.linhaCanvas, fill=self.corLinha2,width=2)
    def verificaTexto(self,event):
        if str(self.entry.get()) == '':
            self.label_Class.place(y=self.yPixel)
            self.label_Class.configure(foreground=self.corLinha1)
            self.canvas_entry.itemconfig(self.linhaCanvas, fill=self.corLinha1,width=1)
        else:
            self.label_Class.place(y=self.yPixel - self.heightPixel)
            self.label_Class.configure(foreground=self.corLinha2)
            self.canvas_entry.itemconfig(self.linhaCanvas, fill=self.corLinha2, width=2)
    def criar_Linha(self):
        self.canvas_entry = tkinter.Canvas(self.master,background=self.corFundo,bd=0,highlightthickness=0,
                                    width=self.widthPixel,height=self.heightPixel)
        self.canvas_entry.place(x=self.xPixel,y=self.yPixel+15)
        self.linhaCanvas = self.canvas_entry.create_line(0, 0, self.widthPixel, 0, fill=self.corLinha1)
    def criar_entry(self):
        self.entry = tkinter.Entry(self.master,background=self.corFundo,foreground=self.corLetra,
                              width=self.widthPixel,font=self.fonte_Class, bd=0)
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
class app_login(Operacional.funcoes_login):
    def __init__(self):
        self.Criar_tela()
        self.Criar_entrys()
        self.Criar_logo()
        self.Criar_botao()
        self.criar_Titulo()
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
    def abrir_appAdm(self):
        app_Adm()
    def abrir_appCli(self):
        app_Cli()
class app_Adm(Operacional.funcoes_adm):
    def __init__(self):
        self.criar_tela()
        self.criar_controle_abas()
    def criar_tela(self):
        self.tela = tkinter.Tk()
        self.width = 1100 # cuidado com esse tamanho. Caso queira mudar, muitos codigos precisam ser recalculados.
        self.height = 700 # pode mudar livremente
        self.tela.iconbitmap('imagens\\estacio_sem_nome.ico')
        self.tela.geometry(f'{self.width}x{self.height}')
        self.tela.resizable(False,False)
        self.tela.title('Central de Ferramentaria - ADM')
        self.tela['background']='white'
    def gerar_aba_treeview(self):
        self.frame_treeview = tkinter.Frame(self.tela, background='white')
        self.frame_treeview.place(x=0,y=400,width=self.width,height=300)
    def gerar_obj_notificacoes(self):
        self.carregar_cabecalho_treeview('pedidos',colunas=[1,2,3,4,5,6,7,8,9,10,11])
        self.treev_principal = my_Treeview(master=self.frame_treeview,x=0,y=0,width=self.width-20,height=300,
                                           colunas=self.cabecalho,pathern=True)
        self.carregar_tabela_com_codigo(nome_aba='pedidos',caso_pai=[3,'pedido'],colunas=[1,2,3,4,5,6,7,8,9,10,11],
                                        treeview=self.treev_principal,filtro=False,
                                        tags=[[6,'espera-alerta'],[7,'aceito-ok','pendente-alerta','negado-perigo']])
    def gerar_obj_acao_estoque(self):
        return print('fazer')
    def gerar_obj_dash(self):
        return print('fazer dash')
    def gerar_obj_compra_descarte(self):
        return print('fazer compra descarte')
    def gerar_obj_cadastro(self):
        return print('fazer cadastro')
    def criar_controle_abas(self):
        self.frame_abas = tkinter.Frame(self.tela)
        self.frame_abas['bg']='white'
        self.frame_abas.place(x=0,y=0,width=self.width, height=100)
        self.frame_notificacoes= None
        self.frame_acao_estoque = None
        self.frame_dash = None
        self.frame_compra_descarte = None
        self.frame_cadastro = None
        self.bt_notificacoes = botao_de_imagens(master=self.frame_abas,xPixel=10, yPixel=40,
                                                imgBase='imagens\\adm\\botoes\\bt_notificacoes_base.gif',
                                                imgMouse='imagens\\adm\\botoes\\bt_notificacoes_mouse.gif',
                                                selecionar=True,
                                                img_clique='imagens\\adm\\botoes\\bt_notificacoes_sel.gif' )
        self.bt_acao_estoque = botao_de_imagens(master=self.frame_abas, xPixel=230, yPixel=40,
                                                imgBase='imagens\\adm\\botoes\\bt_situacao_base.gif',
                                                imgMouse='imagens\\adm\\botoes\\bt_situacao_mouse.gif',
                                                selecionar=True,
                                                img_clique='imagens\\adm\\botoes\\bt_situacao_sel.gif')
        self.bt_dash = botao_de_imagens(master=self.frame_abas, xPixel=450, yPixel=40,
                                                imgBase='imagens\\adm\\botoes\\bt_dash_base.gif',
                                                imgMouse='imagens\\adm\\botoes\\bt_dash_mouse.gif',
                                                selecionar=True,
                                                img_clique='imagens\\adm\\botoes\\bt_dash_sel.gif')
        self.bt_compra_descarte = botao_de_imagens(master=self.frame_abas, xPixel=670, yPixel=40,
                                                imgBase='imagens\\adm\\botoes\\bt_cd_base.gif',
                                                imgMouse='imagens\\adm\\botoes\\bt_cd_mouse.gif',
                                                selecionar=True,
                                                img_clique='imagens\\adm\\botoes\\bt_cd_sel.gif')
        self.bt_cadastro = botao_de_imagens(master=self.frame_abas, xPixel=890, yPixel=40,
                                                imgBase='imagens\\adm\\botoes\\bt_cad_base.gif',
                                                imgMouse='imagens\\adm\\botoes\\bt_cad_mouse.gif',
                                                selecionar=True,
                                                img_clique='imagens\\adm\\botoes\\bt_cad_sel.gif')
        for i in self.frame_abas.winfo_children():  #esse loop define pra todo o menu o mesmo evento
            i.bind('<Button-1>', self.clicar_menu)
class app_Cli():
    def __init__(self):
        print('fazer')


