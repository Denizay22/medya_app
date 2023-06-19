import sys
from operator import index
import qdarktheme
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import aspose.pdf as ap

cred = credentials.Certificate('admin_key.json')
firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://yazilimapp-9e2a2-default-rtdb.europe-west1.firebasedatabase.app'
        })
ref = db.reference()




class Surveyor_Item(QWidget):
    def __init__(self, info, parent=None):
        super(Surveyor_Item, self).__init__(parent)       
       
        self.info = info
        self.setFixedSize(560,150)
        self.name = QLabel("Anketör Adı")
        self.area = QLabel("Anketör Çalışma Alanı")
        self.time = QLabel("Anketin Tamamlanma Süresi")
        self.price = QLabel("Anketör Ücreti")
        self.name_1 = QLabel(self.info["name"])
        self.area_1 = QLabel(self.info["area"])
        self.time_1 = QLabel(self.info["time"])
        self.price_1 = QLabel(self.info["price"])
        self.buy = QPushButton("Satın Al", clicked = lambda: self.buy_survey())
        self.remove = QPushButton("Kaldır", clicked = lambda: self.remove_survey())

        if self.info["isAdmin"] == "False":
            self.remove.hide()
        else:
            self.buy.hide()
        
        layout = QGridLayout()

        layout.addWidget(self.name, 0, 0, 1, 1)
        layout.addWidget(self.area, 1, 0, 1, 1)
        layout.addWidget(self.time, 2, 0, 1, 1)
        layout.addWidget(self.price, 3, 0, 1, 1)
        layout.addWidget(self.name_1, 0, 1, 1, 1)
        layout.addWidget(self.area_1, 1, 1, 1, 1)
        layout.addWidget(self.time_1, 2, 1, 1, 1)
        layout.addWidget(self.price_1, 3, 1, 1, 1)
        layout.addWidget(self.remove, 4, 0, 1, 1)
        layout.addWidget(self.buy, 4, 1, 1, 1)
        self.setLayout(layout)
        self.setStyleSheet('background-color: #39404d;')
        self.dest = self.info["name"] + "+" + self.info["area"] + "+" + self.info["price"]

        if self.info["new"] == "True":
            info_tmp = self.info.copy()
            info_tmp.pop("isAdmin", None)
            info_tmp.pop("new", None)
            info_tmp.pop("bought", None)
            info_tmp.pop("username", None)
            ref.child("surveyor").child(self.dest).set(info_tmp)
        
        
        if  self.info["bought"] == "True":
            self.remove.hide()
            self.buy.hide()
            self.setFixedSize(560,120)
        
    def buy_survey(self):
        self.info.pop("isAdmin", None)
        self.info.pop("new", None)
        self.info.pop("bought", None)
        ref.child("bought_survey").child(self.info["username"]).child(self.dest).set(self.info)

    def remove_survey(self):
        ref.child("surveyor").child(self.dest).delete()
        self.hide()

class Media_Item(QWidget):
    def __init__(self, info, parent=None):
        super(Media_Item, self).__init__(parent)

        self.info = info
        self.setFixedSize(960, 120)
        self.name = QLabel("Medya Organı")
        self.name.setAlignment(Qt.AlignCenter)
        self.area = QLabel("Medya Kaynağı")
        self.area.setAlignment(Qt.AlignCenter)
        self.name_1 = QLabel(self.info["name"])
        self.name_1.setAlignment(Qt.AlignCenter)
        self.area_1 = QLabel(self.info["area"])
        self.area_1.setAlignment(Qt.AlignCenter)
        self.update_media_button = QPushButton("Güncelle", clicked = lambda: self.update_media())
        self.remove_media_button = QPushButton("Kaldır", clicked = lambda: self.remove_media())

        layout = QGridLayout()

        layout.addWidget(self.name, 0, 0, 1, 1)
        layout.addWidget(self.area, 1, 0, 1, 1)
        layout.addWidget(self.name_1, 0, 1, 1, 1)
        layout.addWidget(self.area_1, 1, 1, 1, 1)
        layout.addWidget(self.update_media_button, 2, 0, 1, 1)
        layout.addWidget(self.remove_media_button, 2, 1, 1, 1)
        self.setLayout(layout)
        self.setStyleSheet('background-color: #39404d;')
        self.dest = self.info["name"] + "+" + self.info["area"]

        if self.info["new"] == "True":
            self.info.pop("new", None)
            ref.child("media").child(self.dest).set(self.info)

    def update_media(self):
        ex = Update_Media_MsgBox(self.info)
        ex.show()

    def remove_media(self):
        ref.child("media").child(self.dest).delete()
        self.hide()

        #kaldıırlan medyayla alakalı tüm habelrerin kaldırılması
        all_news = ref.child("news").get()
        if all_news is not None:
            for k, v in all_news.items():
                if v is not None:
                    for kk, vv in v.items():
                        if(vv["name"] == self.info["name"] and vv["area"] == self.info["area"]):
                            #sil mi güncelle mi

                            #silme kodu
                            ref.child("news").child(k).child(kk).delete()

                            #güncelleme kodu
                            
class Haber_Item(QWidget):
    def __init__(self, info, parent=None):
        super(Haber_Item, self).__init__(parent)

        self.info = info
        self.setFixedSize(960, 180)
        self.name = QLabel("Medya Organı")
        self.name.setAlignment(Qt.AlignCenter)
        self.area = QLabel("Medya Kaynağı")
        self.area.setAlignment(Qt.AlignCenter)
        self.text = QLabel("Haber İçeriği")
        self.text.setAlignment(Qt.AlignCenter)
        self.name_1 = QLabel(self.info["name"])
        self.name_1.setAlignment(Qt.AlignCenter)
        self.area_1 = QLabel(self.info["area"])
        self.area_1.setAlignment(Qt.AlignCenter)
        self.text_1 = QLabel(self.info["text"])
        self.text_1.setWordWrap(True)

        layout = QGridLayout()

        layout.addWidget(self.name, 0, 0, 1, 1)
        layout.addWidget(self.area, 1, 0, 1, 1)
        layout.addWidget(self.text, 2, 0, 4, 1)
        layout.addWidget(self.name_1, 0, 1, 1, 2)
        layout.addWidget(self.area_1, 1, 1, 1, 2)
        layout.addWidget(self.text_1, 2, 1, 4, 2)
        self.setLayout(layout)
        self.setStyleSheet('background-color: #39404d;')

class Update_Media_MsgBox(QMessageBox):
    def __init__(self, info):
        QMessageBox.__init__(self)
        
        self.info = info

        self.setSizeGripEnabled(False)

        self.setWindowTitle("Medya Güncelle")
        
        self.addButton(QPushButton("Güncelle"), QMessageBox.YesRole)

        self.add_widget(self)

        currentClick = self.exec_()

        if currentClick == 0:
            old_path = self.info["name"] + "+" + self.info["area"]
            new_path = self.line_edit1.text() + "+" + self.line_edit2.text()
            ref.child("media").child(old_path).delete()
            ref.child("media").child(new_path).set({"name": self.line_edit1.text(),
                                                    "area": self.line_edit2.text()})
            all_news = ref.child("news").get()
            if all_news is not None:
                for k, v in all_news.items():
                    if v is not None:
                        for kk, vv in v.items():
                            if(vv["name"] == self.info["name"] and vv["area"] == self.info["area"]):
                                #sil mi güncelle mi?

                                #silme kodu
                                #ref.child("news").child(k).child(kk).delete()

                                #güncelleme kodu
                                text = ref.child("news").child(k).child(kk).child("text").get()
                                ref.child("news").child(k).child(kk).set({"name": self.line_edit1.text(),
                                                                          "area": self.line_edit2.text(),
                                                                          "text": text})
            



    def add_widget(self, parentItem):
        self.label1 = QLabel("Medya Organı:")
        self.label2 = QLabel("Medya Kaynağı:")

        self.line_edit1 = QLineEdit(self.info["name"])
        self.line_edit2 = QLineEdit(self.info["area"])


        self.layout = self.layout()
        self.layout.addWidget(self.label1)
        self.layout.addWidget(self.label2)
        self.layout.addWidget(self.line_edit1)
        self.layout.addWidget(self.line_edit2)

class User_Item(QWidget):
    def __init__(self, info, parent=None):
        super(User_Item, self).__init__(parent)

        self.setFixedSize(960, 150)

        self.info = info
        self.name = QLabel("İsim")
        self.sub_type = QLabel("Üyelik Tipi")
        self.price = QLabel("Ücret")
        self.activated = QLabel("Aktive Durumu")
        
        self.button_activate = QPushButton("Hesabı Aktifleştir", clicked = lambda: self.activate_user())

        self.setStyleSheet('background-color: #39404d;')
        self.name_1 = QLabel(self.info["username"])
        self.sub_type_1 = QLabel(self.info["subscription_type"])
        self.price_1 = QLabel(self.info["price"])
        self.activated_1 = QLabel()
        if self.info["isActivated"] == "True":
            self.activated_1.setText("Aktif")
            self.setFixedSize(970, 120)
            self.button_activate.hide()
        else:
            self.activated_1.setText("Deaktif")
            self.setFixedSize(970, 150)


        layout = QGridLayout()

        layout.addWidget(self.name, 0, 0, 1, 1)
        layout.addWidget(self.name_1, 0, 1, 1, 1)
        layout.addWidget(self.sub_type, 1, 0, 1, 1)
        layout.addWidget(self.sub_type_1, 1, 1, 1, 1)
        layout.addWidget(self.price, 2, 0, 1, 1)
        layout.addWidget(self.price_1, 2, 1, 1, 1)
        layout.addWidget(self.activated, 3, 0, 1, 1)
        layout.addWidget(self.activated_1, 3, 1, 1, 1)
        layout.addWidget(self.button_activate, 4, 1, 1, 1)

        self.setLayout(layout)

    def activate_user(self):
        self.activated_1.setText("Aktif")
        self.setFixedSize(970, 120)
        self.button_activate.hide()

        ref.child("users").child(self.info["user_type"]).child(self.info["username"]).child("isActivated").set("True")

        
        


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setObjectName("Form")
        self.setFixedSize(1600,900)

        self.isAdmin = False

        self.central_wid = QWidget()
        self.layout_for_wids = QStackedLayout()


        #GİRİŞ SAYFASI
        self.login_page_widget = QWidget()
        self.login_page_widget.setFixedSize(1600,900)
        self.init_login_page()
        
        #MAIN SAYFA
        self.main_page_widget = QWidget()
        self.main_page_widget.setFixedSize(1600,900)

        #ANKETLER SAYFASI
        self.survey_page_widget = QWidget()
        self.survey_page_widget.setFixedSize(1600,900)

        #HABERLER SAYFASI
        self.haber_page_widget = QWidget()
        self.haber_page_widget.setFixedSize(1600,900)

        #KULLANICI SAYFASI(admin only)
        self.user_page_widget = QWidget()
        self.user_page_widget.setFixedSize(1600,900)
        
        
        ########
        self.layout_for_wids.addWidget(self.login_page_widget)
        self.layout_for_wids.addWidget(self.main_page_widget),
        self.layout_for_wids.addWidget(self.survey_page_widget)
        self.layout_for_wids.addWidget(self.haber_page_widget)
        self.layout_for_wids.addWidget(self.user_page_widget)
        self.central_wid.setLayout(self.layout_for_wids)
        self.setCentralWidget(self.central_wid)
        self.current_page = "LOGIN"
        
    def init_login_page(self):
        #TODO logo ekle
        #login inputs
        
        self.login_inputs_widget = QWidget(self.login_page_widget)
        self.login_inputs_widget.setObjectName("login_inputs")
        self.login_inputs_widget.setGeometry(QRect(100, 400, 600, 120))
        self.login_inputs_grid = QGridLayout(self.login_inputs_widget)
        self.login_inputs_grid.setContentsMargins(0, 0, 0, 0)
        self.login_inputs_grid.setObjectName("login_inputs_grid")
        

        self.login_username_input = QLineEdit(self.login_inputs_widget)
        self.login_username_input.setObjectName("login_username_input")
        self.login_inputs_grid.addWidget(self.login_username_input, 0, 1, 1, 1)
        
        self.login_username_text = QLabel(self.login_inputs_widget)
        self.login_username_text.setObjectName("login_username_text")
        self.login_inputs_grid.addWidget(self.login_username_text, 0, 0, 1, 1)

        self.login_password_input = QLineEdit(self.login_inputs_widget)
        self.login_password_input.setObjectName("login_password_input")
        self.login_inputs_grid.addWidget(self.login_password_input, 1, 1, 1, 1)

        self.login_password_text = QLabel(self.login_inputs_widget)
        self.login_password_text.setObjectName("login_password_text")
        self.login_inputs_grid.addWidget(self.login_password_text, 1, 0, 1, 1)

        self.login_user_type_text = QtWidgets.QLabel(self.login_inputs_widget)
        self.login_user_type_text.setObjectName("user_type_text")
        self.login_inputs_grid.addWidget(self.login_user_type_text, 2, 0, 1, 1)

        self.login_user_type_combobox = QtWidgets.QComboBox(self.login_inputs_widget)
        self.login_user_type_combobox.setObjectName("user_type_combobox")
        self.login_inputs_grid.addWidget(self.login_user_type_combobox, 2, 1, 1, 1)

        self.login_button = QPushButton(self.login_inputs_widget, clicked = lambda: self.login_user())
        self.login_button.setObjectName("login_button")
        self.login_inputs_grid.addWidget(self.login_button, 3, 1, 1, 1)
        

        #register inputs
        self.gridLayoutWidget_2 = QWidget(self.login_page_widget)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(900, 400, 600, 210))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")

        self.register_inputs = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.register_inputs.setContentsMargins(0, 0, 0, 0)
        self.register_inputs.setObjectName("register_inputs")

        self.register_username_text = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.register_username_text.setObjectName("register_username_text")
        self.register_inputs.addWidget(self.register_username_text, 0, 0, 1, 1)

        self.register_password_text = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.register_password_text.setObjectName("register_password_text")
        self.register_inputs.addWidget(self.register_password_text, 1, 0, 1, 1)

        self.register_type_text = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.register_type_text.setObjectName("register_type_text")
        self.register_inputs.addWidget(self.register_type_text, 2, 0, 1, 1)

        self.register_custom_type_text = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.register_custom_type_text.setObjectName("register_custom_type_text")
        self.register_inputs.addWidget(self.register_custom_type_text, 3, 0, 1, 1)

        self.register_type_price_text = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.register_type_price_text.setObjectName("register_type_price_text")
        self.register_inputs.addWidget(self.register_type_price_text, 4, 0, 1, 1)

        self.register_user_type_text = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.register_user_type_text.setObjectName("user_type_text")
        self.register_inputs.addWidget(self.register_user_type_text, 5, 0, 1, 1)

        self.register_username_input = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.register_username_input.setObjectName("register_username_input")
        self.register_inputs.addWidget(self.register_username_input, 0, 1, 1, 1)

        self.register_password_input = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.register_password_input.setObjectName("register_password_input")
        self.register_inputs.addWidget(self.register_password_input, 1, 1, 1, 1)

        self.subscription_type_box = QtWidgets.QComboBox(self.gridLayoutWidget_2)
        self.subscription_type_box.activated.connect(self.check_custom)
        self.subscription_type_box.setObjectName("subscription_type_box")
        self.register_inputs.addWidget(self.subscription_type_box, 2, 1, 1, 1)

        self.custom_type_input = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.custom_type_input.setObjectName("custom_type_input")
        self.custom_type_input.textChanged.connect(self.set_custom_price)
        self.register_inputs.addWidget(self.custom_type_input, 3, 1, 1, 1)

        self.register_type_price_text_2 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.register_type_price_text_2.setObjectName("register_type_price_text_2")
        self.register_inputs.addWidget(self.register_type_price_text_2, 4, 1, 1, 1)

        self.register_user_type_combobox = QtWidgets.QComboBox(self.gridLayoutWidget_2)
        self.register_user_type_combobox.setObjectName("user_type_combobox")
        self.register_user_type_combobox.activated.connect(self.check_custom)
        self.register_inputs.addWidget(self.register_user_type_combobox, 5, 1, 1, 1)

        self.register_button = QtWidgets.QPushButton(self.gridLayoutWidget_2, clicked = lambda: self.register_user())
        self.register_button.setObjectName("register_button")
        self.register_inputs.addWidget(self.register_button, 6, 1, 1, 1)

        self.register_custom_type_text.setEnabled(False)
        self.custom_type_input.setEnabled(False)


        ################

        _translate = QCoreApplication.translate
        self.login_username_text.setText(_translate("Form", "Kullanıcı Adı"))
        self.login_password_text.setText(_translate("Form", "Şifre"))
        self.login_button.setText(_translate("Form", "Giriş"))
        self.register_custom_type_text.setText(_translate("Form", "Özel üyelik Tipi"))
        self.register_username_text.setText(_translate("Form", "Kullanıcı Adı"))
        self.register_password_text.setText(_translate("Form", "Şifre"))
        self.register_type_text.setText(_translate("Form", "Üyelik Tipi"))
        self.register_button.setText(_translate("Form", "Kayıt Ol"))
        self.login_user_type_text.setText(_translate("Form", "Kullanıcı Tipi"))
        self.register_user_type_text.setText(_translate("Form", "Kullanıcı Tipi"))


        #################

        self.login_user_type_combobox.addItems(['Kişi', 'Şirket'])
        self.register_user_type_combobox.addItems(['Kişi', 'Şirket'])
        self.sub_types = ['Günlük', 'Haftalık', 'Aylık']
        self.prices = [50000, 10000, 5000]
        self.register_custom_type_text.setText("Özel")
        self.register_type_price_text.setText("Fiyat")
        self.register_type_price_text_2.setText("20000TL")
        self.subscription_type_box.addItems(self.sub_types)
        self.subscription_type_box.addItem("Özel")

    def init_main_page(self, widget):
        self.top_buttons_widget = QWidget(widget)
        self.top_buttons_widget.setObjectName("top_buttons_widget")
        self.top_buttons_widget.setGeometry(QRect(100, 30, 1400, 60))
        self.top_buttons_grid = QGridLayout(self.top_buttons_widget)
        self.top_buttons_grid.setContentsMargins(0,0,0,0)
        self.top_buttons_grid.setObjectName("top_buttons_grid")

        self.top_buttons_survey = QPushButton(self.top_buttons_widget, clicked = lambda: self.switch_to_survey())
        self.top_buttons_survey.setObjectName("top_buttons_survey")
        self.top_buttons_grid.addWidget(self.top_buttons_survey, 0, 0, 1, 1)

        self.top_buttons_media = QPushButton(self.top_buttons_widget, clicked = lambda: self.switch_to_haber())
        self.top_buttons_media.setObjectName("top_buttons_media")
        self.top_buttons_grid.addWidget(self.top_buttons_media, 0, 1, 1, 1)

        self.top_buttons_users = QPushButton(self.top_buttons_widget, clicked = lambda: self.switch_to_users())
        self.top_buttons_users.setObjectName("top_buttons_users")
        self.top_buttons_grid.addWidget(self.top_buttons_users, 1, 0, 1, 1)

        self.user_info_text = QLabel(widget)
        self.user_info_text.setObjectName("user_info_text")
        self.user_info_text.setAlignment(Qt.AlignCenter)
        self.top_buttons_grid.addWidget(self.user_info_text, 1, 1, 1, 1)


        if self.isAdmin != True:
            self.top_buttons_users.hide()
        

        
        
        
        ##############

        _translate = QCoreApplication.translate
        self.top_buttons_survey.setText(_translate("Form", "Anketörler"))
        self.top_buttons_media.setText(_translate("Form", "Haberler"))
        self.top_buttons_users.setText(_translate("Form", "Kullanıcılar"))
        if self.isAdmin:
            self.top_buttons_users.show()
            self.user_info_text.setText("Admin girişi yapıldı.")
            self.top_buttons_media.setText(_translate("Form", "Medya Organları"))

        else:
            self.user_info_text.setText("Hoşgeldin " + self.db_user_info["username"] + ".")
            self.top_buttons_users.hide()

        ###############
    
    def check_custom(self):
        selected = self.subscription_type_box.currentText()
        user_type = self.register_user_type_combobox.currentText()
        price = 0
        if selected == "Günlük":
            price = self.prices[0]

            if user_type == "Şirket":
                price = price * 2
            self.register_type_price_text_2.setText(str(price) + "TL")
            
        elif selected == "Haftalık":
            price = self.prices[1]
            if user_type == "Şirket":
                price = price * 2
            self.register_type_price_text_2.setText(str(price) + "TL")
        elif selected == "Aylık":
            price = self.prices[2]
            if user_type == "Şirket":
                price = price * 2
            self.register_type_price_text_2.setText(str(price) + "TL")
        else:
            self.show_warning_messagebox("Özel kısmına haberlerin kaç saatte bir güncellenmesini istediğinizi giriniz. " + 
                                         "\nFiyatlandırma şu şekildedir:\n" + 
                                         "\nSaat başı güncelleme ücreti: 100000TL" +  
                                         "\nEklenen her saat için ücret 2000TL düşer." + 
                                         "\nMaksimum 12 saat girilebilir." + 
                                         "\nŞirketler için fiyatlar 2 katıdır ve ücret indirimi yarı yarıyadır.")
            self.register_type_price_text_2.setText("Lütfen özel üyelik kısmını doldurunuz.")


        if selected not in self.sub_types:
            self.register_custom_type_text.setEnabled(True)
            self.custom_type_input.setEnabled(True)
        else:
            self.register_custom_type_text.setEnabled(False)
            self.custom_type_input.setEnabled(False)

    def set_custom_price(self):
        text = self.custom_type_input.text()
        price = 100000
        deduct = 2000
        user_type = self.register_user_type_combobox.currentText()
        if user_type == "Şirket":
            price = price * 2
            deduct = deduct / 2
        if len(text) == 0:
            self.register_type_price_text_2.setText("")
        elif int(text) > 12:
            self.show_warning_messagebox("Lütfen 12'den küçük bir değer giriniz.")
            self.custom_type_input.setText("") 
        else:
            price = price - int(self.custom_type_input.text()) * deduct
            self.register_type_price_text_2.setText(str(int(price)) + "TL")
    
    def init_survey_page(self):
        self.init_main_page(self.survey_page_widget)
        if self.isAdmin == True:

            self.gridlayoutWidget_3 = QWidget(self.survey_page_widget)
            self.gridlayoutWidget_3.setGeometry(QRect(760, 150, 300, 150))
            self.gridlayoutWidget_3.setObjectName("gridLayoutWidget_3")
            self.new_survey_inputs = QtWidgets.QGridLayout(self.gridlayoutWidget_3)
            self.new_survey_inputs.setContentsMargins(0,0,0,0)
            self.new_survey_inputs.setObjectName("new_survey_inputs")

            self.new_survey_name_label = QtWidgets.QLabel(self.gridlayoutWidget_3)
            self.new_survey_name_label.setObjectName("new_survey_name_label")
            self.new_survey_inputs.addWidget(self.new_survey_name_label, 0, 0, 1, 1)

            self.new_survey_area_label = QtWidgets.QLabel(self.gridlayoutWidget_3)
            self.new_survey_area_label.setObjectName("new_survey_area")
            self.new_survey_inputs.addWidget(self.new_survey_area_label, 1, 0, 1, 1)

            self.new_survey_time_label = QtWidgets.QLabel(self.gridlayoutWidget_3)
            self.new_survey_time_label.setObjectName("new_survey_area")
            self.new_survey_inputs.addWidget(self.new_survey_time_label, 2, 0, 1, 1)

            self.new_survey_price_label = QtWidgets.QLabel(self.gridlayoutWidget_3)
            self.new_survey_price_label.setObjectName("new_survey_name_label")
            self.new_survey_inputs.addWidget(self.new_survey_price_label, 3, 0, 1, 1)

            self.new_survey_name_input = QtWidgets.QLineEdit(self.gridlayoutWidget_3)
            self.new_survey_name_input.setObjectName("new_survey_name_input")
            self.new_survey_inputs.addWidget(self.new_survey_name_input, 0, 1, 1, 1)

            self.new_survey_area_input = QtWidgets.QLineEdit(self.gridlayoutWidget_3)
            self.new_survey_area_input.setObjectName("new_survey_name_input")
            self.new_survey_inputs.addWidget(self.new_survey_area_input, 1, 1, 1, 1)

            self.new_survey_time_input = QtWidgets.QLineEdit(self.gridlayoutWidget_3)
            self.new_survey_time_input.setObjectName("new_survey_name_input")
            self.new_survey_inputs.addWidget(self.new_survey_time_input, 2, 1, 1, 1)

            self.new_survey_price_input = QtWidgets.QLineEdit(self.gridlayoutWidget_3)
            self.new_survey_price_input.setObjectName("new_survey_name_input")
            self.new_survey_inputs.addWidget(self.new_survey_price_input, 3, 1, 1, 1)

            self.new_survey_add_button = QtWidgets.QPushButton(self.gridlayoutWidget_3, clicked = lambda: self.add_survey())
            self.new_survey_add_button.setObjectName("register_button")
            self.new_survey_inputs.addWidget(self.new_survey_add_button, 4, 1, 1, 1)

            
            ########################

            self.new_survey_name_label.setText("Anketör Adı")
            self.new_survey_area_label.setText("Anketör Alanı")
            self.new_survey_price_label.setText("Anketör Ücreti")
            self.new_survey_time_label.setText("Anketin Tamamlanma Süresi")
            self.new_survey_add_button.setText("Anketör Ekle")




        self.surveyor_list_label = QLabel(self.survey_page_widget)
        self.surveyor_list_label.setGeometry(QRect(150, 100, 600, 50))
        self.surveyor_list_label.setAlignment(Qt.AlignCenter)
        self.surveyor_list_label.setFont(QFont("Arial", 20))
        self.surveyor_list_label.setText("Anket Listesi")

        self.surveyor_bought_list_label = QLabel(self.survey_page_widget)
        self.surveyor_bought_list_label.setGeometry(QRect(850, 100, 600, 50))
        self.surveyor_bought_list_label.setAlignment(Qt.AlignCenter)
        self.surveyor_bought_list_label.setFont(QFont("Arial", 20))
        self.surveyor_bought_list_label.setText("Satın Alınan Anketler")

        self.scroll_layout_surveyor_list = QFormLayout(self.survey_page_widget)
        self.scroll_widget_surveyor_list = QWidget(self.survey_page_widget)
        self.scroll_widget_surveyor_list.setLayout(self.scroll_layout_surveyor_list)
        
        self.scroll_area_surveryor_list = QScrollArea(self.survey_page_widget)
        self.scroll_area_surveryor_list.setWidgetResizable(True)
        self.scroll_area_surveryor_list.setWidget(self.scroll_widget_surveyor_list)
        self.scroll_area_surveryor_list.setGeometry(QRect(150, 150, 600, 700))
        self.scroll_area_surveryor_list.setStyleSheet('background-color: #4f5a6e;')

        self.scroll_layout_bought_list = QFormLayout(self.survey_page_widget)
        self.scroll_widget_bought_list = QWidget(self.survey_page_widget)
        self.scroll_widget_bought_list.setLayout(self.scroll_layout_bought_list)
        
        self.scroll_area_bought_list = QScrollArea(self.survey_page_widget)
        self.scroll_area_bought_list.setWidgetResizable(True)
        self.scroll_area_bought_list.setWidget(self.scroll_widget_bought_list)
        self.scroll_area_bought_list.setGeometry(QRect(850, 150, 600, 700))
        self.scroll_area_bought_list.setStyleSheet('background-color: #4f5a6e;')

        if self.isAdmin == True:
            self.surveyor_bought_list_label.hide()
            self.scroll_area_bought_list.hide()

        surveyor_list = ref.child("surveyor").get()

        if surveyor_list is not None:
            for k, v in surveyor_list.items():
                self.add_survey_from_db(v)


    
        bought_survey_list = ref.child("bought_survey").child(self.db_user_info["username"]).get()
        
        if bought_survey_list is not None:
            for k,v in bought_survey_list.items():
                self.add_bought_survey_from_db(v)

    def add_bought_survey_from_db(self, data):
        data["new"] = "false"
        data["bought"] = "True"
        data["username"] = self.db_user_info["username"]
        data["isAdmin"] = "False"
        self.scroll_layout_bought_list.addRow(Surveyor_Item(data))
        
    def add_survey_from_db(self, data):
        data["new"] = "False"
        data["bought"] = "False"
        data["username"] = self.db_user_info["username"]
        if self.isAdmin:
            data["isAdmin"] = "True"
        else:
            data["isAdmin"] = "False"
        
        self.scroll_layout_surveyor_list.addRow(Surveyor_Item(data))

    def add_survey(self):
        data = {}
        data["name"] = self.new_survey_name_input.text()
        data["area"] = self.new_survey_area_input.text()
        data["time"] = self.new_survey_time_input.text()
        data["price"] = self.new_survey_price_input.text()
        data["new"] = "True"
        data["bought"] = "False"
        data["username"] = self.db_user_info["username"]
        if self.isAdmin:
            data["isAdmin"] = "True"
        else:
            data["isAdmin"] = "False"
        
        self.scroll_layout_surveyor_list.addRow(Surveyor_Item(data))

    def init_haber_page(self):
        self.init_main_page(self.haber_page_widget)
        if self.isAdmin == True:

            self.gridlayoutWidget_4 = QWidget(self.haber_page_widget)
            self.gridlayoutWidget_4.setGeometry(QRect(1110, 150, 300, 90))
            self.gridlayoutWidget_4.setObjectName("gridLayoutWidget_3")
            self.new_media_inputs = QtWidgets.QGridLayout(self.gridlayoutWidget_4)
            self.new_media_inputs.setContentsMargins(0,0,0,0)
            self.new_media_inputs.setObjectName("new_media_inputs")

            self.new_media_name_label = QtWidgets.QLabel(self.gridlayoutWidget_4)
            self.new_media_name_label.setObjectName("new_media_name_label")
            self.new_media_inputs.addWidget(self.new_media_name_label, 0, 0, 1, 1)

            self.new_media_area_label = QtWidgets.QLabel(self.gridlayoutWidget_4)
            self.new_media_area_label.setObjectName("new_media_area_label")
            self.new_media_inputs.addWidget(self.new_media_area_label, 1, 0, 1, 1)

            self.new_media_name_input = QtWidgets.QLineEdit(self.gridlayoutWidget_4)
            self.new_media_name_input.setObjectName("new_media_name_input")
            self.new_media_inputs.addWidget(self.new_media_name_input, 0, 1, 1, 1)

            self.new_media_area_input = QtWidgets.QLineEdit(self.gridlayoutWidget_4)
            self.new_media_area_input.setObjectName("new_media_area_input")
            self.new_media_inputs.addWidget(self.new_media_area_input, 1, 1, 1, 1)

            self.new_media_add_button = QtWidgets.QPushButton(self.gridlayoutWidget_4, clicked = lambda: self.add_media())
            self.new_media_add_button.setObjectName("new_media_add_button")
            self.new_media_inputs.addWidget(self.new_media_add_button, 2, 1, 1, 1)

            
            ########################

            self.new_media_name_label.setText("Medya Organı")
            self.new_media_area_label.setText("Medya Kaynağı")
            self.new_media_add_button.setText("Ekle")

        self.media_list_label = QLabel(self.haber_page_widget)
        self.media_list_label.setGeometry(QRect(100, 100, 1000, 50))
        self.media_list_label.setAlignment(Qt.AlignCenter)
        self.media_list_label.setFont(QFont("Arial", 20))
        self.media_list_label.setText("Haber Listesi")

        self.scroll_layout_media_list = QFormLayout(self.haber_page_widget)
        self.scroll_widget_media_list = QWidget(self.haber_page_widget)
        self.scroll_widget_media_list.setLayout(self.scroll_layout_media_list)
        
        self.scroll_area_media_list = QScrollArea(self.haber_page_widget)
        self.scroll_area_media_list.setWidgetResizable(True)
        self.scroll_area_media_list.setWidget(self.scroll_widget_media_list)
        self.scroll_area_media_list.setGeometry(QRect(100, 150, 1000, 700))
        self.scroll_area_media_list.setStyleSheet('background-color: #4f5a6e;')

        self.sub_type_label = QLabel(self.haber_page_widget)
        self.sub_type_label.setGeometry(QRect(1110, 150, 150, 30))
        if self.isAdmin == False:

            if self.db_user_info["subscription_type"] != "Özel":
                self.sub_type_label.setText("Güncellenme Sıklığı: " + self.db_user_info["subscription_type"])
            else:
                self.sub_type_label.setText("Güncellenme Sıklığı: " + self.db_user_info["custom_hours"] + " saat")

            self.sub_price = QLabel(self.haber_page_widget)
            self.sub_price.setGeometry(QRect(1110, 180, 150, 30))
            self.sub_price.setText("Ücret: " + self.db_user_info["price"])


            self.export_to_pdf = QPushButton(self.haber_page_widget, clicked= lambda: self.export_pdf())
            self.export_to_pdf.setGeometry(QRect(1110, 820, 200, 30))
            self.export_to_pdf.setText("PDF Dosyasına Rapor Oluştur")


        if self.isAdmin == True:
            self.media_list_label.setText("Medya Organları")

            media_list = ref.child("media").get()
            if media_list is not None:
                for k, v in media_list.items():
                    self.add_media_from_db(v)
        
        else:
            haber_list = ref.child("news").child(self.db_user_info["username"]).get()
            
            if haber_list is not None:
                for k, v in haber_list.items():
                    print(v)
                    self.add_haber_from_db(v)
        
    def export_pdf(self):
        document = ap.Document()
        page = document.pages.add()
        haber_list = ref.child("news").child(self.db_user_info["username"]).get()
        if haber_list is not None:
            for k,v in haber_list.items():
                text = ap.text.TextFragment("Medya Organı: " + v["name"] + 
                                                  "\nMedya Kaynağı: " + v["area"] + 
                                                  "\nHaber Metni: " + v["text"] + "\n\n\n" + 41 * "—" + "\n\n\n")
                page.paragraphs.add(text)

        document.save(self.db_user_info["username"] + ".pdf")

        self.show_warning_messagebox("Haberler raporu başarıyla oluşturuldu.")

    def add_haber_from_db(self, data):
        self.scroll_layout_media_list.addRow(Haber_Item(data))

    def add_media_from_db(self, data):
        data["new"] = "False"
        self.scroll_layout_media_list.addRow(Media_Item(data))

    def add_media(self):
        data = {}
        data["name"] = self.new_media_name_input.text()
        data["area"] = self.new_media_area_input.text()
        data["new"] = "True"
        self.scroll_layout_media_list.addRow(Media_Item(data))
        
    def init_user_page(self):
        self.init_main_page(self.user_page_widget)
        
        self.user_list_label = QLabel(self.user_page_widget)
        self.user_list_label.setGeometry(QRect(100, 100, 1000, 50))
        self.user_list_label.setAlignment(Qt.AlignCenter)
        self.user_list_label.setFont(QFont("Arial", 20))
        self.user_list_label.setText("Kullanıcılar")

        self.scroll_layout_user_list = QFormLayout(self.user_page_widget)
        self.scroll_widget_user_list = QWidget(self.user_page_widget)
        self.scroll_widget_user_list.setLayout(self.scroll_layout_user_list)
        
        self.scroll_area_user_list = QScrollArea(self.user_page_widget)
        self.scroll_area_user_list.setWidgetResizable(True)
        self.scroll_area_user_list.setWidget(self.scroll_widget_user_list)
        self.scroll_area_user_list.setGeometry(QRect(100, 150, 1000, 700))
        self.scroll_area_user_list.setStyleSheet('background-color: #4f5a6e;')

        users_list = ref.child("users").get()
        for k,v in users_list["Kişi"].items():
            print(v)
            if v["username"] != "admin":
                self.scroll_layout_user_list.addRow(User_Item(v))
            
        for k,v in users_list["Şirket"].items():
            self.scroll_layout_user_list.addRow(User_Item(v))

    def switch_to_main(self):
        self.init_main_page(self.main_page_widget)

        self.top_buttons_survey.setStyleSheet('')
        self.top_buttons_media.setStyleSheet('')
        self.top_buttons_users.setStyleSheet('')

        if self.current_page == "NEWS":
            self.haber_page_widget.hide()
        elif self.current_page == "USERS":
            self.user_page_widget.hide()
        elif self.current_page == "SURVEY":
            self.survey_page_widget.hide()
        elif self.current_page == "LOGIN":
            self.login_page_widget.hide()

        self.main_page_widget.show()
        self.current_page = "MAIN"

    def switch_to_survey(self):
        self.init_survey_page()
        self.top_buttons_survey.setStyleSheet('background-color: #4f5a6e;')
        self.top_buttons_media.setStyleSheet('')
        self.top_buttons_users.setStyleSheet('')
        if self.current_page == "MAIN":
            self.main_page_widget.hide()
        elif self.current_page == "NEWS":
            self.haber_page_widget.hide()
        elif self.current_page == "USERS":
            self.user_page_widget.hide()
        
        self.survey_page_widget.show()
        self.current_page = "SURVEY"

    def switch_to_haber(self):
        self.init_haber_page()
        self.top_buttons_media.setStyleSheet('background-color: #4f5a6e;')
        self.top_buttons_survey.setStyleSheet('')
        self.top_buttons_users.setStyleSheet('')
        if self.current_page == "MAIN":
            self.main_page_widget.hide()
        elif self.current_page == "SURVEY":
            self.survey_page_widget.hide()
        elif self.current_page == "USERS":
            self.user_page_widget.hide()

        self.haber_page_widget.show()
        self.current_page = "NEWS"
        
    def switch_to_users(self):
        self.init_user_page()
        self.top_buttons_users.setStyleSheet('background-color: #4f5a6e;')
        self.top_buttons_media.setStyleSheet('')
        self.top_buttons_survey.setStyleSheet('')
        if self.current_page == "MAIN":
            self.main_page_widget.hide()
        elif self.current_page == "NEWS":
            self.haber_page_widget.hide()
        elif self.current_page == "SURVEY":
            self.survey_page_widget.hide()

        self.user_page_widget.show()
        self.current_page = "USERS"

        #TODO
        #sadece adminler buraya girebiliyor (ayarlı)
        #Tüm kullanıcıların oldugu bir liste görünür. onaylanmamış kullanıcıları admin burdan onaylayabilir veya reddedebilir. eğer reddedilirse kulalnıcının bilgileri
        #database'den silinir.
        #admin aynı zamanda sistemde kayıtlı herhangi bir kullanıcıyı da silebilir
        #eğer bir kullanıcı silinirse database'deki o kullanıcı ile alakalı haberler ve anketler de silinmelidir (zorunlu değil)

    def register_user(self):
        username = self.register_username_input.text()
        password = self.register_password_input.text()
        user_type = self.register_user_type_combobox.currentText()
        subscription_type = self.subscription_type_box.currentText()
        price = self.register_type_price_text_2.text()
        custom_hours = self.custom_type_input.text()
        if len(username) == 0:
            self.show_warning_messagebox("Kullanıcı adı boş bıraklamaz.")
        elif len(password) < 8:
            self.show_warning_messagebox("Şifre en az 8 karakter olmalıdır.")
        else:
            db_info = ref.child("users").child(user_type).child(username).get()
            if db_info is not None:
                self.show_warning_messagebox("Bu isimde bir kullanıcı sistemde mevcut.")
            else:
                #kullanıcı bilgisini oluştur
                user_info = {"username": username,
                            "password": password,
                            "subscription_type": subscription_type,
                            "price": price,
                            "custom_hours": custom_hours,
                            "user_type": user_type,
                            "isActivated": "False"}
                #database'e yazdır
                ref.child("users").child(user_type).child(username).set(user_info)
                self.show_warning_messagebox("Kaydınız tamamlandı, yöneticiler kaydınızı onayladıktan sonra giriş yapabilirsiniz.")

    def login_user(self):
        username = self.login_username_input.text()
        password = self.login_password_input.text()

        if len(username) == 0:
            self.show_warning_messagebox("Kullanıcı adı boş bıraklamaz.")
        elif len(password) < 8:
            self.show_warning_messagebox("Şifre en az 8 karakter olmalıdır.")
        else:
            user_type = self.login_user_type_combobox.currentText()
            self.db_user_info = ref.child("users").child(user_type).child(username).get()
            if self.db_user_info is None:
                self.show_warning_messagebox("Bu isimde bir kullanıcı sistemde bulunmuyor.")
            elif self.db_user_info["password"] != password:
                self.show_warning_messagebox("Lütfen şifrenizi kontrol ediniz.")
            elif username == "admin":
                self.isAdmin = True
                self.switch_to_main()
            elif self.db_user_info["isActivated"] == "False":
                self.show_warning_messagebox("Hesabınız yöneticiler tarafından onaylanmamış.")
            else:
                self.isAdmin = False
                self.switch_to_main()

    def show_warning_messagebox(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(message)
        msg.setWindowTitle("Hata")
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()
                
    #unittestler için database call'ları
    def if_user_exists(username, user_type):
        user = ref.child("users").child(user_type).child(username).get()
        if user is not None:
            return True
        return False

    def get_sub_type(username, user_type):
        user = ref.child("users").child(user_type).child(username).get()
        if user is not None:
            return user["subscription_type"]
        return None
    
    def get_new_count_for_user(username):
        news_for_user = ref.child("news").child(username).get()
        return len(news_for_user)
    

    def if_user_activated(username, user_type):
        user = ref.child("users").child(user_type).child(username).get()
        if user["isActivated"] == "True":
            return True
        return False
    
    def did_user_bought_a_survey(username):
        survey = ref.child("bought_survey").child(username).get()

        if survey is not None:
            return True
        return False
    
    def does_media_exist(media_source):
        medias = ref.child("media").get()

        for k, v in medias.items():
            if v["area"] == media_source:
                return True
        return False



if __name__ == "__main__":
        app = QApplication(sys.argv)
        qdarktheme.setup_theme()
        app.setApplicationName("Medya Arama Uygulaması")
        main = MainWindow()
        main.resize(1600,900)
        main.show()
        sys.exit(app.exec_())