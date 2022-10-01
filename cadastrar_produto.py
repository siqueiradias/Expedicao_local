from PyQt5 import uic,QtWidgets
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QIntValidator, QDoubleValidator
import os
import sys

import App
from factory_db import *
from cadastrar_produto_db import *

class CadastrarProduto(QtWidgets.QMainWindow):
    def __init__(self):
        super(CadastrarProduto, self).__init__()
        uic.loadUi("gui/view/tela_cad_produto.ui", self)
        self._update = False
        self._banco = factory_db()
        self.abrir_cad_produto()
        
        """
        #DIGITAÇÃO DOS LINE_TEXT
        self.txt_cod.textChanged.connect(self.alterar_label)
        self.txt_volumes.textChanged.connect(self.alterar_label)
        self.btn_adicionar.setEnabled(False)
        """
        #VALIDADOR
        self.onlyInt = QIntValidator()
        self.onlyDouble = QDoubleValidator(999999, -999999, 3)
        self.txt_codigo.setValidator(self.onlyInt)
        self.txt_peso_liq.setValidator(self.onlyDouble)
        
        #BOTÕES
        self.btn_inserir.clicked.connect(self.inserir)
        #self.btn_atualizar.clicked.connect(self.salvar)
        #self.btn_remover.clicked.connect(self.remover_tabela)
        self.btn_sair.clicked.connect(self.Sair)
        #self.btn_cadastrar.clicked.connect()
        
    def abrir_cad_produto(self):
        self.inserir_tabela(cadastrar_produto_db.buscar(self._banco.get_cursor()))    

    def atualizar_tabela(self):
        self.inserir_tabela(cadastrar_produto_db.buscar(self._banco.get_cursor()))    

    def inserir(self):
        cod_produto = self.txt_codigo.text()
        descricao = self.txt_desc.text()
        peso_liq = float(self.txt_peso_liq.text().replace(',', '.'))
        
        try:
            op = cadastrar_produto_db.inserir(self._banco.get_cursor(), self._banco.get_conexao(), cod_produto, descricao, peso_liq)
            print(type(op))
            print(op)
        except Exception as e:
            print("Erro: ", e)
        
        if op == 1:
            #print(f"Cod.: {cod_produto} - {descricao} - {peso_liq}Kg") 
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowTitle("Notificação")
            msg_box.setText("Produto salvo com sucesso!")
            
            self.atualizar_tabela()
            
            return_value = msg_box.exec()
            
        elif op[0] == 2:
            if str(op[1]).count('UNIQUE'):
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Information)
                msg_box.setWindowTitle("Notificação")
                msg_box.setText("Produto já está cadastrado!")
            
                return_value = msg_box.exec()
            else:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Critical)
                msg_box.setWindowTitle("ERRO")
                msg_box.setText("Erro ao salvar Produto!")
                msg_box.setDetailedText(str(op[1]))
            
                return_value = msg_box.exec()
            
        else:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setWindowTitle("ERRO")
            msg_box.setText("Erro ao salvar Produto!")
            msg_box.setDetailedText(str(op[1]))
            
            return_value = msg_box.exec()
        

    def novo_espelho(self, espelho):
        self.lbl_espelho.setText(str(espelho))

    def atualizar_espelho(self, espelho):
        self._update = True
        self.lbl_espelho.setText(str(espelho))
        cad_espelho = cadastrar_espelho_db()
        self.inserir_tabela(cad_espelho.buscar_espelho(espelho))
        self.alterar_label()
    
    def closeEvent(self, event):
        #self.tela = App.Main_Window()
        #self.tela.show()
        event.accept()
    
    def Sair(self):
        msg = QMessageBox()
        msg.setWindowTitle("Atenção!")
        msg.setText(f"Deseja realmente SAIR do cadastro do produtos?")
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        msg.setEscapeButton(QMessageBox.Cancel)
        #msg.setDetailedText("Mais informações")

        msg.buttonClicked.connect(self.resultado)
 
        retorno = msg.exec()      
    
    def resultado(self, clicado):
        if clicado.text() == "&Yes":
            #self.tela = cadastrar_espelho.Main_Window()
            #self.tela.show()
            self.hide()

    def _buscar_dados(self):
        cadastrar_espelho_db().buscar(self.txt_cod.text())

    def _salvar_dados(self):
        pass

    def alterar_label(self):
        dados = cadastrar_espelho_db().buscar(self.txt_cod.text())
        desc_bool = False
        vol_bool = False
        try:
            self.lbl_descricao.setText(dados[1])
            #self.btn_adicionar.setEnabled(True)            
            desc_bool = True
        except Exception as e:
            #print("Erro ao alterar label descrição: ", e)
            self.lbl_descricao.setText('Não encontrado')
            #self.btn_adicionar.setEnabled(False)
            desc_bool = False

        try:
            self.lbl_peso.setText(f"{float(dados[2]*int(self.txt_volumes.text())):.3f} KG")
            vol_bool = True
        except Exception as e:
            #print("Erro ao alterar label peso: ", e)
            self.lbl_peso.setText("0.000 KG")
            vol_bool = False
        if desc_bool and vol_bool:
            self.btn_adicionar.setEnabled(True)
        else:
            self.btn_adicionar.setEnabled(False)

    def pegar_valor(self):
        """Pega os dados adicionados na tablea_resumo (GUI)
        e retorna em uma lista

        Returns:
            list: lista de tuplas(espelho, cod_produto, volume_prev., peso_previsto)
        """        
        volume_geral = 0
        peso_geral = float(0.0)
        cont = 0
        lista_espelho = []
        while cont < self.tbl_resumo.rowCount():
            volume_geral += int(self.tbl_resumo.item(cont, 2).text())
            peso_geral += float(self.tbl_resumo.item(cont, 3).text())
            #lista_espelho(espelho, cod_produto, volume_prev., peso_previsto)
            lista_espelho.append((self.lbl_espelho.text(),\
                int(self.tbl_resumo.item(cont, 0).text()),\
                     int(self.tbl_resumo.item(cont, 2).text()),\
                         float(self.tbl_resumo.item(cont, 3).text()),\
                             0,\
                                 float(0.0)))
            cont += 1
        return lista_espelho

    def salvar(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Salvar Espelho")
        msgBox.setText(f"Deseja salvar o {self.lbl_espelho.text()}?")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        msgBox.setDefaultButton(QMessageBox.Yes)
        msgBox.setEscapeButton(QMessageBox.Cancel)
        returnValue = msgBox.exec()

        if returnValue == QMessageBox.Yes:
            dados = self.pegar_valor()
            for item in dados:
                print(item)
            try:
                salvar_dados = cadastrar_espelho_db()
                if self._update:
                    #Tratamento dos dados do espelho_old
                    espelho_old = list()
                    espelho_new = list()
                    for item in salvar_dados.buscar_espelho(self.lbl_espelho.text()):
                        espelho_old.append((self.lbl_espelho.text(), item[0], int(item[2]), float(item[3])))
                    for item in dados:
                        espelho_new.append(item[0:4])
                    for item in espelho_old:
                        if not item in espelho_new:
                            salvar_dados.remover_produto(item[0], item[1])
                            print("item removido: ", item)
                    print("iniciando atualização")
                    for item in dados:
                        salvar_dados.atualizar_espelho(item)
                else:
                    print("inserindo dados sem UpDate")
                    salvar_dados.inserir_espelho(dados)
                self.tela = App.Main_Window()
                self.tela.show()
                self.hide()
            except Exception as e:
                print('Erro ao SALVAR os dados dos espelho: ', e)
        elif returnValue == QMessageBox.No:
            self.tela = App.Main_Window()
            self.tela.show()
            self.hide()
        elif returnValue == QMessageBox.Cancel:
            pass

    def adicionar(self):
        if self.verificar_tabela():
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowTitle("Atenção")
            msg_box.setText("""Produto ja consta no espelho.\nDeseja atualizar item?""")
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg_box.setDefaultButton(QMessageBox.No)

            return_value = msg_box.exec()

            if return_value == QMessageBox.Yes:
                self.remove_item_tabela()
                self.inserir_tabela()
                self.atualizar_label_geral()
                self.txt_cod.setText('')
                self.txt_volumes.setText('')
            else:
                self.txt_cod.setText('')
                self.txt_volumes.setText('')

        else:
            self.inserir_tabela()
            self.atualizar_label_geral()
            self.txt_cod.setText('')
            self.txt_volumes.setText('')
        self.txt_cod.setFocus()

    def verificar_tabela(self):
        """Verificar se o produto que se deseja adicionar já consta
        na tabela

        Returns:
            boolean: True = Produto consta, False = Produto NÃO consta
        """
        cont = 0
        while cont < self.tbl_resumo.rowCount():
            if self.tbl_resumo.item(cont, 0).text() == self.txt_cod.text():
                return(True)
            cont += 1
        return False

    """
    def inserir_tabela(self, lista_dados = None):
        #Insere os dados extraidos das labels e line_edit:
        #Cod_produto, desc_produto, e peso para a tabela_resumo
        
        #Organiza a lagura das colunas
        header = self.tbl_resumo.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        
        if lista_dados == None:
            rowCount = self.tbl_resumo.rowCount()
            self.tbl_resumo.insertRow(rowCount)
            # add more if there is more columns in the database.
            self.tbl_resumo.setItem(rowCount, 0, QtWidgets.QTableWidgetItem(str(int(self.txt_codigo.text()))))
            self.tbl_resumo.setItem(rowCount, 1, QtWidgets.QTableWidgetItem(self.txt_desc.text()))
            self.tbl_resumo.setItem(rowCount, 2, QtWidgets.QTableWidgetItem(self.txt_peso_liq.text().replace(',','.')))
            #self.pegar_valor()
        else:
            for itens in lista_dados:
                rowCount = self.tbl_resumo.rowCount()
                self.tbl_resumo.insertRow(rowCount)
                for item in enumerate(itens):
                    #Ingora o primeito item pois faz referencia ao espelho
                    #if coluna == 0:
                    #    continue

                    # add more if there is more columns in the database.
                    self.tbl_resumo.setItem(rowCount, coluna, QtWidgets.QTableWidgetItem(str(item)))
    """
    
    def inserir_tabela(self, dados):
        header = self.tbl_resumo.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

        rowCount = self.tbl_resumo.rowCount()
        cont = len(dados)
        while cont > 0:
            cont -= 1
            self.tbl_resumo.insertRow(rowCount)
            for coluna in range(3):    
                self.tbl_resumo.setItem(rowCount, coluna, QtWidgets.QTableWidgetItem(str(dados[cont][coluna]))) 
    
    def atualizar_label_geral(self):
        dados = self.pegar_valor()
        volume_geral = 0
        peso_geral = 0.0
        for item in dados:
            volume_geral += item[2]
            peso_geral += item[3]
        
        self.lbl_geral_volume.setText(str(volume_geral) + ' CX')
        self.lbl_geral_peso.setText(str(peso_geral) + ' KG')

    def remover_tabela(self):
        if self.tbl_resumo.rowCount() > 0:
            self.tbl_resumo.removeRow(self.tbl_resumo.currentRow())
            self.atualizar_label_geral()
    
    def remove_item_tabela(self):
        """Verificar se produto informado no formulario já consta na tabela,
        se SIM, remove o item da tabela
        """
        if self.tbl_resumo.rowCount() > 0:
            cont = 0
            while cont < self.tbl_resumo.rowCount():
                if self.tbl_resumo.item(cont, 0).text() == self.txt_cod.text():
                    self.tbl_resumo.removeRow(cont)
                cont += 1


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    janela = CadastrarProduto()
    janela.show()
    sys.exit(app.exec_())