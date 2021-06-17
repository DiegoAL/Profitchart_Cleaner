"""Classe para interação com os arquivos temporarios do profitchart."""

import os
import shutil
import psutil
from time import sleep

# Diretorio do profitchart
profitDir = os.getenv('APPDATA') + '\\Nelogica'


class profitController():
    def profitIsRunningKill(tryKill=False):
        """Verificar se o processo do profit.exe esta aberto.

        :param tryKill: Indica se o programa deve tentar encerrar o processo
        :return: Retorna true se não estiver aberto e false se estiver
        """
        procName = 'profitchart'
        procFounded = False

        for proc in psutil.process_iter():
            if proc.name().find(procName) != -1:
                procFounded = True
                if tryKill:
                    pPid = proc.pid
                    proc.kill()
                    proc.wait()
                    # Verifica se o processo foi mesmo encerrado
                    if psutil.pid_exists(pPid):
                        return False
                    else:
                        return True
                else:
                    return False
        if procFounded is False:
            return True


    def profitClearDir():
        """Acessa o diretorio de dados do profitchart.

        Para cada subdiretorio remove o conteudo da pasta 'profPath'.
        """

        # os.chdir(os.getenv('APPDATA') + '\\Nelogica')
        os.chdir(profitDir)
        profPath = '\\database\\assets'

        # Para cada subdiretorio remove o conteudo da pasta 'profPath'
        fl = os.listdir()
        for i in fl:
            if os.path.exists(i + profPath):
                shutil.rmtree(i + profPath)
                os.mkdir(i + profPath)


    def profitStart(ctmProfitPath=None):
        """Inicia o profitchart.

        Se for informado um caminho até um executavel tenta abrir este .exe e
            caso haja sucesso retorna True e gera um arquivo com este caminho
        Se não for informado um caminho customizado verifica se existe algum profit
            aberto se não houver abre o profit padrão
            Caso o diretorio padrao não seja encontrado varre a pasta em busca do
                primeiro executavel compativel

        :param ctmProfitPath: Caminho customizado do profit.exe
        :return: True se executado com sucesso e False caso não encontre o .exe
        """

        pDefault = profitDir + '\\Profit'
        pExeName = '\\profitchart.exe'
        if ctmProfitPath is None:
            # Iniciando o profit no diretorio padrão
            # ou no primeiro diretorio que encontrar
            if os.path.exists(pDefault) and profitController.profitIsRunningKill(False):
                sleep(3)
                os.system(r"start " + pDefault + pExeName)
                return True
            # Busca o primeiro diretorio com um .exe
            elif profitController.profitIsRunningKill(False):
                ldir = os.listdir(profitDir)
                # Variavel de controle
                exeFounded = False
                for pd in ldir:
                    pathExe = profitDir + '\\' + pd + pExeName
                    # Ao encontrar o primeiro .exe encerra a execucao
                    if os.path.exists(pathExe):
                        # @@TODO: Bug na hora de abrir o profit em outro diretorio
                        # Ajusta a variavel para executar o arquivo
                        pathExe = profitDir + '\\"' + pd + '\"' + pExeName
                        os.system(r"start " + pathExe)
                        sleep(3)
                        return True
                # Se nenhum arquivo for encontrado retorna o False
                if exeFounded is False:
                    return False
        else:
            # Executar o .exe informado se não for encontrado retorna False
            try:
                if os.system(r"start " + ctmProfitPath) == 0:
                    sleep(3)
                    fl = open('lastrun.txt', 'w')
                    fl.write(ctmProfitPath)
                    return True
                else:
                    return False
            except Exception:
                return False
