"""Interface de interação com o usuario."""
import PySimpleGUI as sg
from webbrowser import open
from ProfitController import profitController as pc
from time import sleep

gitLink = 'https://github.com/DiegoAL/Profitchart_Cleaner'
sg.theme('DefaultNoMoreNagging')
nmIni = 'lastrun.txt'

# Elementos da janela
cbox_layout = [[sg.Checkbox('Iniciar o Profitchart após limpeza', True, enable_events=True, key='start')],
               [sg.Checkbox('Fechar após limpeza', enable_events=True, key='close')],
               [sg.Checkbox('Escolher um executável especifico', enable_events=True, key='newPath')]]

btn_layout = [[sg.Button('Limpar!', size=(10, 4), enable_events=True, key='clear')]]

layout = [[sg.Column(cbox_layout),
          sg.Column(btn_layout)],
          [sg.In(enable_events=True, key='pAdd', disabled=True),
          sg.FileBrowse(enable_events=True, disabled=True, key='flB')],
          [sg.Text('Idealizado por: Diego Alves'),
           sg.Text('Link do Projeto', size=(24, 0),
           justification='right', enable_events=True, key='link',
           text_color='blue', font='Aerial 10 underline')]]

# Criacao e demais configuracoes da janela
window = sg.Window('Profitchart Cleaner', layout)

# Verifica se existe o arquivo lastrun.ini e preenche o campo de custom path
''' BUG!!
if path.exists(nmIni):
    event, values = window.read()
    fl = io.open(nmIni, 'r')
    pth = fl.read()
    print(pth)
    window['pAdd'].update(disabled=False)
    window['flB'].update(disabled=False)
    # window['pAdd'].update(value=pth)
'''

# Leitura dos dados e eventos
while True:
    event, values = window.read()

    # Função que realiza a limpeza
    def cleanup():
        pc.profitClearDir()
        # Iniciar após limpeza
        if values['start']:
            # Verifica se o usuario quer iniciar por um caminho customizado
            if values['pAdd'] != '' and values['newPath']:
                # Ajusta a str para o fortato do win colocando sempre ""
                nlist = values['pAdd'].split('/')
                std = '"\\"'.join(nlist).replace(':"\\"', ':\\"') + '"'
                if pc.profitStart(std) is False:
                    sg.popup('Um erro ocorreu ao tentar abrir o arquivo')
            # Inicia o profit pelo diretorio padrao
            else:
                pc.profitStart()

    # Fechar aplicacao
    if event == sg.WINDOW_CLOSED:
        break

    # Acessar a pagina do Projeto
    if event == 'link':
        open(gitLink)

    # Popup com maiores informacoes sobre o diretorio customizado
    if values['newPath']:
        window['pAdd'].update(disabled=False)
        window['flB'].update(disabled=False)
        if values['pAdd'] == '':
            msg = 'Caso queira acessar o diretório padrão (%APPDATA%/Nelogica) não é necessario utilizar esta  opção'
            sg.popup(msg)
    else:
        window['pAdd'].update(disabled=True)
        window['flB'].update(disabled=True)

    # Execucao da limpeza
    if event == 'clear':
        # Verifica se o profit esta aberto
        if pc.profitIsRunningKill() is False:
            msg = 'O Profitchart está aberto, deseja forçar o encerramento??'
            ppyn = sg.popup_yes_no(msg)
            if ppyn == 'Yes':
                # Tenta encerrar o profit
                if pc.profitIsRunningKill(True):
                    # Chama o metodo de limpeza
                    cleanup()
                    # Fechar app
                    if values['close']:
                        sleep(3)
                        break
                else:
                    msg = 'Não foi possivel encerra o Profit, tente manualmente!'
                    sg.popup(msg)
            else:
                sg.popup('Finalize o Profitchart e tente novamente')
        # Segue com a limpeza
        else:
            # Chama o metodo de limpeza
            cleanup()
            # Fechar app
            if values['close']:
                sleep(3)
                break

window.close()


### @@TODO:
#   DAr um jeito de ler o lastrun e carregar se estiver preenchido
#   converter para exe e testar
#   upar no github
#   loading
