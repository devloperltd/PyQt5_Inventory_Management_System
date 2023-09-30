import sys
import MySQLdb
import images_rc
import os
import time
import tempfile
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PIL import Image


##########################################
############# Login Window ###############

class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
        # Load the login.ui file
        loadUi('login.ui', self)
        self.statusBar().setStyleSheet("background-color: #17202A;")
        self.login_Btn.clicked.connect(self.Login_App)
        self.SignUp_Button.clicked.connect(self.Show_Reg)

        self.Show_pass.clicked.connect(self.toggle_password)
        self.Hide_pass.clicked.connect(self.toggle_password)
        # Initially, hide the "Hide" button        
        self.Hide_pass.hide()

    def Login_App(self):
            UN = self.login_username.text()
            PW = self.login_password.text()
            self.login_username.setText("")
            self.login_password.setText("")
            self.db = MySQLdb.connect(host ='localhost' , user ='root' , password ='16031980' , db='laroussi_libary')
            self.cur = self.db.cursor()
            self.cur.execute("select * from registration where username = '"+ UN +"' and password = '"+ PW +"'")
            result = self.cur.fetchone()

            if result:
                success_text = '<font color="#2ECC71">Login System Successfully ...</font>'
                self.msg_label.setText(success_text)
                self.status_bar = self.statusBar()
                self.status_bar.setStyleSheet("background-color: #17202A; color: #58D68D;")
                self.status_bar.showMessage('Login details has been successfully registered')
                QMessageBox.information(self, 'Login successfully', 'Login system successfully !!!')               
                self.open_main_window()

            elif (UN == '' and PW == ''):
                warning_text = '<font color="#F5B041">Field Should Not Be Empty !!!</font>'
                self.msg_label.setText(warning_text)
                self.status_bar = self.statusBar()
                self.status_bar.setStyleSheet("background-color: #17202A; color: #F5B041;")
                self.status_bar.showMessage('This field is required and cannot be empty !!!')
                QMessageBox.warning(self, 'Warning', 'Field should not be empty !!!')                            

            else:    
                error_text = '<font color="#C0392B">Invalid User name Or Password !!!</font>'
                self.msg_label.setText(error_text)
                self.login_username.setText("")
                self.login_password.setText("")
                self.status_bar = self.statusBar()
                self.status_bar.setStyleSheet("background-color: #17202A; color: #E74C3C;")
                self.status_bar.showMessage('Invalid user name or password !!!')
                QMessageBox.critical(self, 'Error', 'Invalid user name or password !!!')

    # Initially, Show the password & Hide the password    
    def toggle_password(self):
        if self.login_password.echoMode() == QLineEdit.Normal:
            # Show the password (set QLineEdit to Normal mode)
            self.login_password.setEchoMode(QLineEdit.Password)
            self.Show_pass.show()
            self.Hide_pass.hide()
        else:
            # Hide the password (set QLineEdit to Password mode)
            self.login_password.setEchoMode(QLineEdit.Normal)
            self.Show_pass.hide()
            self.Hide_pass.show()

    def Show_Reg(self) :
        self.hide()
        self.Show_Reg = RegWindow()  # Keep a reference to RegWindow
        self.Show_Reg.show()


    def open_main_window(self):
        self.hide()
        self.main_window = main_project()  # Keep a reference to MainWindow
        self.main_window.show()


##########################################
######### Registration Window ############

class RegWindow(QMainWindow):
    def __init__(self):
        super(RegWindow, self).__init__()
        # Load the Registration.ui file
        loadUi('Registration.ui', self)
        self.statusBar().setStyleSheet("background-color: #17202A;")
        self.Reg_Btn.clicked.connect(self.Registration)
        self.backLogin_Button.clicked.connect(self.Show_Login)
        
        self.Reg_Show_pass.clicked.connect(self.toggle_reg_password)
        self.Reg_Hide_pass.clicked.connect(self.toggle_reg_password)
        # Initially, hide the "Hide" button        
        self.Reg_Hide_pass.hide()        

    def Registration(self):
        R_un = self.Reg_username.text()
        R_pw = self.Reg_password.text()
        R_em = self.Reg_email.text()
        R_ph = self.Reg_phone.text()
        self.Reg_username.setText("")
        self.Reg_password.setText("")
        self.Reg_email.setText("")
        self.Reg_phone.setText("")

        self.db = MySQLdb.connect(host ='localhost' , user ='root' , password ='16031980' , db='laroussi_libary')
        self.cur = self.db.cursor()
        self.cur.execute("select * from registration where username = %s and password = %s", (R_un, R_pw))
        result = self.cur.fetchone() 

        if result:
            self.status_bar = self.statusBar()
            self.status_bar.setStyleSheet("background-color: #17202A; color: #58D68D;")
            self.status_bar.showMessage('user name is already registered try to login !!!')            
            QMessageBox.information(self, 'Note !!!', 'user name is already registered !!!')

        elif (R_un == '' or R_pw == '' or R_em == '' or R_ph == ''):
            self.status_bar = self.statusBar()
            self.status_bar.setStyleSheet("background-color: #17202A; color: #F5B041;")
            self.status_bar.showMessage('This field is required and cannot be empty !!!')            
            QMessageBox.critical(self, 'Warning', 'Field should not be empty !!!') 

        else:
            self.cur.execute("INSERT INTO registration (username, password, email, phone) VALUES (%s, %s, %s, %s)", (R_un, R_pw, R_em, R_ph))
            self.db.commit()
            self.status_bar = self.statusBar()
            self.status_bar.setStyleSheet("background-color: #17202A; color: #58D68D;")
            self.status_bar.showMessage('Login details has been successfully registered')            
            QMessageBox.information(self, 'Success', 'user name is successfully registered !!!')

    # Initially, Show the password & Hide the password    
    def toggle_reg_password(self):
        if self.Reg_password.echoMode() == QLineEdit.Normal:
            # Show the password (set QLineEdit to Normal mode)
            self.Reg_password.setEchoMode(QLineEdit.Password)
            self.Reg_Show_pass.show()
            self.Reg_Hide_pass.hide()
        else:
            # Hide the password (set QLineEdit to Password mode)
            self.Reg_password.setEchoMode(QLineEdit.Normal)
            self.Reg_Show_pass.hide()
            self.Reg_Hide_pass.show()      


    def Show_Login(self):        
        self.hide()
        self.Login_App = LoginWindow()  # Keep a reference to LoginWindow
        self.Login_App.show()

##########################################
############# Main Window ################

class main_project(QMainWindow):
    def __init__(self):
        super(main_project, self).__init__()
        # Load the login.ui file
        loadUi('Project.ui', self)

        # Set Default Home Page
        self.Open_DashTab()

        # Load Data base From MySQL To QTableWidget Update_Date_Time 
        self.Load_Emp_Data()
        self.Load_Supp_Data()
        self.Load_Category_Data()
        self.Load_Products_Data()
        self.Load_Sales_Products_Data()
        self.Update_Date_Time()
        # Update Dashboard Content
        self.Dashboard_Content()


        self.Handel_Button() 

        # Update Date & Time
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.Update_Date_Time)
        self.timer.start(1000)

        # Load Data base From Bills To QListWidget
        self.Show_Bills()
        self.Invoice_listWidget.itemClicked.connect(self.Get_Data_Bills)

        # Customized Connect QTableWidget
        self.Em_tableWidget.itemSelectionChanged.connect(self.Update_Emp_Data)
        self.Supp_tableWidget.itemSelectionChanged.connect(self.Update_Supp_Data)
        self.Category_tableWidget.itemSelectionChanged.connect(self.Update_Category_Data)
        self.Product_tableWidget.itemSelectionChanged.connect(self.Update_Products_Data)

        # Customized Em_tableWidget
        self.Em_tableWidget.setColumnWidth(0, 50)
        self.Em_tableWidget.setColumnWidth(3, 50)
        self.Em_tableWidget.setColumnWidth(8, 70)
        self.Em_tableWidget.setColumnWidth(9, 205)

        # Customized Supp_tableWidget
        self.Supp_tableWidget.setColumnWidth(0, 70)
        self.Supp_tableWidget.setColumnWidth(2, 130)
        self.Supp_tableWidget.setColumnWidth(3, 215)

        # Customized Category_tableWidget
        self.Category_tableWidget.setColumnWidth(0, 180)
        self.Category_tableWidget.setColumnWidth(1, 495)

        # Customized Product_Cart_tableWidget
        self.Product_Cart_tableWidget.setColumnWidth(0, 50)
        self.Product_Cart_tableWidget.setColumnWidth(3, 70)
        self.Sales_Product_tableWidget.setColumnWidth(0, 50)
        self.Sales_Product_tableWidget.setColumnWidth(1, 180)
       
        # Customized Employee Button
        self.Empl_Save_Btn.clicked.connect(self.Add_Emp_Data)
        self.Empl_Update_Btn.clicked.connect(self.Update_Emp_Record)
        self.Empl_Delete_Btn.clicked.connect(self.Delete_Emp_Data)
        self.Empl_Clear_Btn.clicked.connect(self.Clear_Emp_Data)
        self.Empl_Search_Btn.clicked.connect(self.Search_Emp_Data)

        # Customized Supplier Button
        self.Supplier_Save_Btn.clicked.connect(self.Add_Supp_Data)
        self.Supplier_Update_Btn.clicked.connect(self.Update_Supp_Record)
        self.Supplier_Delete_Btn.clicked.connect(self.Delete_Supp_Data)
        self.Supplier_Clear_Btn.clicked.connect(self.Clear_Supp_Data)
        self.Supp_Search_Btn.clicked.connect(self.Search_Supp_Data)

        # Customized Category Button
        self.Save_Category_Btn.clicked.connect(self.Add_Category_Data)
        self.Delete_Category_Btn.clicked.connect(self.Delete_Category_Data)

        # Customized Product's Button
        self.Save_Product_Btn.clicked.connect(self.Add_Products_Data)
        self.Update_Product_Btn.clicked.connect(self.Update_Products_Record)
        self.Delete_Product_Btn.clicked.connect(self.Delete_Products_Data)
        self.Clear_Product_Btn.clicked.connect(self.Clear_Products_Data)
        self.Product_Search_Btn.clicked.connect(self.Search_Products_Data)

        # Customized Sales Product's Button
        self.Sales_Product_Search_Btn.clicked.connect(self.Search_Sales_Products_Data)
        self.Sales_checkBox.clicked.connect(self.Load_Sales_Products_Data)

        # Customized Bill's Reports Button
        self.Search_Bills_Btn.clicked.connect(self.Search_Bills)
        self.Clear_Bills_Btn.clicked.connect(self.Clear_Search_Bills)

        # Customized Calculator Button
        self.Calc_7_Btn.clicked.connect(lambda: self.press_it('7'))
        self.Calc_8_Btn.clicked.connect(lambda: self.press_it('8'))
        self.Calc_9_Btn.clicked.connect(lambda: self.press_it('9'))
        self.Calc_Plus_Btn.clicked.connect(lambda: self.press_it('+'))
        self.Calc_4_Btn.clicked.connect(lambda: self.press_it('4'))
        self.Calc_5_Btn.clicked.connect(lambda: self.press_it('5'))
        self.Calc_6_Btn.clicked.connect(lambda: self.press_it('6'))
        self.Calc_Minus_Btn.clicked.connect(lambda: self.press_it('-'))
        self.Calc_1_Btn.clicked.connect(lambda: self.press_it('1'))
        self.Calc_2_Btn.clicked.connect(lambda: self.press_it('2'))
        self.Calc_3_Btn.clicked.connect(lambda: self.press_it('3'))
        self.Calc_Multiplied_Btn.clicked.connect(lambda: self.press_it('*'))
        self.Calc_0_Btn.clicked.connect(lambda: self.press_it('0'))
        self.Calc_C_Btn.clicked.connect(lambda: self.press_it('C'))
        self.Calc_Equals_Btn.clicked.connect(lambda: self.math_it())
        self.Calc_Divided_Btn.clicked.connect(lambda: self.press_it('/'))

        # Customized Bill Area Button
        self.Print_Bill_Btn.clicked.connect(self.Print_Bill)
        self.Generate_Bill_Btn.clicked.connect(self.Generate_Bills)
        self.Cart_Clear_Btn.clicked.connect(self.Clear_Cart)
        self.Clear_All_Btn.clicked.connect(self.Clear_All)

        # Variables
        self.Category_List = []
        self.Supplier_List = []
        self.Cart_List = []
        self.Set_Print = 0
        "SELECT category_No, category_Name FROM category WHERE category_Name = %s"
        self.Fetch_Supplier_Category()

        # Quantity In Stock 
        self.Sales_Product_tableWidget.itemSelectionChanged.connect(self.update_in_stock)

        # Add Update Cart 
        self.Add_Update_Cart_Btn.clicked.connect(self.Add_Update_Cart)

        # Add Update Cart 
        self.Exit_Button.clicked.connect(self.ExitConfirmation)

##########################################
##### Customized Button & Interface ######

    def Handel_Button(self):
        self.tabWidget.tabBar().setVisible(False)
        self.Dash_Button.clicked.connect(self.Open_DashTab)
        self.Employee_Button.clicked.connect(self.Open_Employee_Tab)
        self.Supplier_Button.clicked.connect(self.Open_Supplier_Tab)
        self.Category_Button.clicked.connect(self.Open_Category_Tab)
        self.Products_Button.clicked.connect(self.Open_Products_Tab)
        self.Sales_Button.clicked.connect(self.Open_Sales_Tab)

    def Open_DashTab(self):
        self.tabWidget.setCurrentIndex(0)
    def Open_Employee_Tab(self):
        self.tabWidget.setCurrentIndex(1)
    def Open_Supplier_Tab(self):
        self.tabWidget.setCurrentIndex(2)
    def Open_Category_Tab(self):
        self.tabWidget.setCurrentIndex(3)
    def Open_Products_Tab(self):
        self.tabWidget.setCurrentIndex(4)
    def Open_Sales_Tab(self):
        self.tabWidget.setCurrentIndex(5)

#############################################
######### Add Employee To Database ##########

    def Add_Emp_Data(self):
        
        self.db = MySQLdb.connect(host ='localhost' , user ='root' , password ='16031980' , db='laroussi_inventory')
        self.cur = self.db.cursor()

        self.cur.execute("SELECT * FROM employee WHERE idemployee = %s", (self.Emp_No.text(),))
        row = self.cur.fetchone()
        if row:
            self.status_bar = self.statusBar()
            self.status_bar.showMessage('Employee ID is already registred!, Please try different...')
            QMessageBox.warning(self, 'Warrning', 'This Employee ID already Assigned !!')

        elif (self.Emp_No.text() == '' or self.Emp_Name.text() == ''): 
            self.status_bar = self.statusBar()
            self.status_bar.showMessage('Employee details must be required !!!...')
            QMessageBox.critical(self, 'Error!!', 'Employee details must be required !!!') 
            
        else:
            self.cur.execute("INSERT INTO employee (Emp_No, Name, Email, Gender, Contact_No, DOB, DOJ, Password, User_Type, Address, Salary) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(
                                            self.Emp_No.text(),
                                            self.Emp_Name.text(),
                                            self.Emp_Mail.text(),
                                            self.Gender_Comb.currentText(),
                                            self.Emp_ContactNo.text(),
                                            self.Emp_DOB.text(),
                                            self.Emp_DOJ.text(),
                                            self.Emp_Password.text(),
                                            self.UserType_Comb.currentText(),
                                            self.Emp_Address.toPlainText(),
                                            self.Emp_Salary.text()            
                        ))
            self.db.commit()
            QMessageBox.information(self, 'Success !!', 'Employee Added Successfully')
            # Clear all input fields
            self.Emp_No.clear()
            self.Emp_Name.clear()
            self.Emp_Mail.clear()
            self.Emp_ContactNo.clear()
            self.Emp_DOB.clear()
            self.Emp_DOJ.clear()
            self.Emp_Password.clear()
            self.Emp_Address.clear()
            self.Emp_Salary.clear()
            self.Gender_Comb.setCurrentIndex(0)
            self.UserType_Comb.setCurrentIndex(0)            
            self.Load_Emp_Data()
    
################################################
######### Load Employee From Database ##########

    def Load_Emp_Data(self):
        try:
            self.db = MySQLdb.connect(host ='localhost' , user ='root' , password ='16031980' , db='laroussi_inventory')
            self.cur = self.db.cursor()
            self.cur.execute("SELECT Emp_No, Name, Email, Gender, Contact_No, DOB, DOJ, Password, User_Type, Address, Salary FROM employee")
            row = self.cur.fetchall()
            self.Em_tableWidget.setRowCount(len(row))
            self.Em_tableWidget.setColumnCount(11)  # Adjust the number of columns

            for row_num, row_data in enumerate(row):
                for col_num, value in enumerate(row_data):
                    item = QTableWidgetItem(str(value))
                    self.Em_tableWidget.setItem(row_num, col_num, item)
            self.db.commit()
        except Exception as ex:           
            # Handle the exception by displaying an error message
            QMessageBox.critical(self, 'Error', f'An error occurred: {str(ex)}')
        finally:
            # Close the database connection in the finally block
            if hasattr(self, 'db'):
                self.db.close()

###########################################
######## Delete Employee Database #########
 
    def Delete_Emp_Data(self):
        try:
            self.db = MySQLdb.connect(host ='localhost' , user ='root' , password ='16031980' , db='laroussi_inventory')
            self.cur = self.db.cursor()
            selected_row = self.Em_tableWidget.currentRow()
            if selected_row >= 0:
                idemployee = self.Em_tableWidget.item(selected_row, 0).text()
                confirm_dialog = QMessageBox.question(self, 'Confirm Deletion', 'Are you sure you want to delete this employee?',
                                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if confirm_dialog == QMessageBox.Yes:

                    self.cur.execute("DELETE FROM employee WHERE Emp_No = %s", (idemployee,))
                    self.db.commit()
                    self.Em_tableWidget.removeRow(selected_row)
                    # Refresh the table to display the updated product list
                    self.Clear_Emp_Data()                                
                    QMessageBox.information(self, 'Success !!', 'Employee Has Been Deleted Successfully')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error deleting employee: {str(e)}')
            if self.db is not None:
                self.db.close()

#############################################
######## Update From Em_tableWidget #########  
               
    def Update_Emp_Data(self):
        try:
            selected_row = self.Em_tableWidget.currentRow()
            if selected_row >= 0:
                # Get the employee data from the selected row in the table
                idemployee = self.Em_tableWidget.item(selected_row, 0).text()
                Em_Name = self.Em_tableWidget.item(selected_row, 1).text()
                Em_Mail = self.Em_tableWidget.item(selected_row, 2).text()
                Em_Gender = self.Em_tableWidget.item(selected_row, 3).text()
                Em_Contact = self.Em_tableWidget.item(selected_row, 4).text()
                Em_DOB = self.Em_tableWidget.item(selected_row, 5).text()
                Em_DOJ = self.Em_tableWidget.item(selected_row, 6).text()
                Em_Password = self.Em_tableWidget.item(selected_row, 7).text()
                Em_UserType = self.Em_tableWidget.item(selected_row, 8).text()
                Em_Address = self.Em_tableWidget.item(selected_row, 9).text()
                Em_Salary = self.Em_tableWidget.item(selected_row, 10).text()

                # Display the employee details in the input fields for editing
                self.Emp_No.setText(idemployee)
                self.Emp_Name.setText(Em_Name)
                self.Emp_Mail.setText(Em_Mail)
                self.Gender_Comb.setCurrentText(Em_Gender)
                self.Emp_ContactNo.setText(Em_Contact)
                self.Emp_DOB.setText(Em_DOB)
                self.Emp_DOJ.setText(Em_DOJ)
                self.Emp_Password.setText(Em_Password)
                self.UserType_Comb.setCurrentText(Em_UserType)
                self.Emp_Address.setPlainText(Em_Address)
                self.Emp_Salary.setText(Em_Salary)

        except Exception as e:
                QMessageBox.critical(self, 'Error', f'Error updating employee data: {str(e)}')

#######################################
######## Update From Database #########  

    def Update_Emp_Record(self):
        try:
            selected_row = self.Em_tableWidget.currentRow()
            if selected_row >= 0:
                # Get the data from the input fields
                idemployee = self.Emp_No.text()
                Em_Name = self.Emp_Name.text()
                Em_Mail = self.Emp_Mail.text()
                Em_Gender = self.Gender_Comb.currentText()
                Em_Contact = self.Emp_ContactNo.text()
                Em_DOB = self.Emp_DOB.text()
                Em_DOJ = self.Emp_DOJ.text()
                Em_Password = self.Emp_Password.text()
                Em_UserType = self.UserType_Comb.currentText()
                Em_Address = self.Emp_Address.toPlainText()
                Em_Salary = self.Emp_Salary.text()

                self.db = MySQLdb.connect(host ='localhost' , user ='root' , password ='16031980' , db='laroussi_inventory')
                self.cur = self.db.cursor()

                update_query = """
                    UPDATE employee
                    SET Name=%s, Email=%s, Gender=%s, Contact_No=%s, DOB=%s, DOJ=%s, Password=%s, User_Type=%s, Address=%s, Salary=%s
                    WHERE idemployee=%s
                """
                self.cur.execute(update_query, (Em_Name, Em_Mail, Em_Gender, Em_Contact, Em_DOB, Em_DOJ, Em_Password, Em_UserType, Em_Address, Em_Salary, idemployee))
                self.db.commit()
                QMessageBox.information(self, 'Success !!', 'Employee Has Been Updated Successfully')
                
                # Update the data in the table widget
                self.Em_tableWidget.setItem(selected_row, 0, QTableWidgetItem(idemployee))
                self.Em_tableWidget.setItem(selected_row, 1, QTableWidgetItem(Em_Name))
                self.Em_tableWidget.setItem(selected_row, 2, QTableWidgetItem(Em_Mail))
                self.Em_tableWidget.setItem(selected_row, 3, QTableWidgetItem(Em_Gender))
                self.Em_tableWidget.setItem(selected_row, 4, QTableWidgetItem(Em_Contact))
                self.Em_tableWidget.setItem(selected_row, 5, QTableWidgetItem(Em_DOB))
                self.Em_tableWidget.setItem(selected_row, 6, QTableWidgetItem(Em_DOJ))
                self.Em_tableWidget.setItem(selected_row, 7, QTableWidgetItem(Em_Password))
                self.Em_tableWidget.setItem(selected_row, 8, QTableWidgetItem(Em_UserType))
                self.Em_tableWidget.setItem(selected_row, 9, QTableWidgetItem(Em_Address))
                self.Em_tableWidget.setItem(selected_row, 10, QTableWidgetItem(Em_Salary))

                # Update the data in the database (You should implement this part based on your database connection)
                # Example pseudocode:
                # commit changes to the database

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error updating employee data: {str(e)}')

#####################################
######## Clear Input Fields ######### 

    def Clear_Emp_Data(self):
            self.Emp_No.clear()
            self.Emp_Name.clear()
            self.Emp_Mail.clear()
            self.Emp_ContactNo.clear()
            self.Emp_DOB.clear()
            self.Emp_DOJ.clear()
            self.Emp_Password.clear()
            self.Emp_Address.clear()
            self.Emp_Salary.clear()
            self.Gender_Comb.setCurrentIndex(0)
            self.UserType_Comb.setCurrentIndex(0) 
            self.Emp_SearchBy_Comb.setCurrentIndex(0)
            self.Emp_Search_box.clear() 
            self.Load_Emp_Data()

###############################################
######## Search Employee From Database ########

    def Search_Emp_Data(self):
        # Your database connection
        self.db = MySQLdb.connect(host ='localhost' , user ='root' , password ='16031980' , db='laroussi_inventory')
        self.cur = self.db.cursor()

        selected_option = self.Emp_SearchBy_Comb.currentText()
        search_input = self.Emp_Search_box.text()

        try:
            if selected_option == '':
                QMessageBox.critical(self, 'Error !!', 'Please, Select Search by Option First...')
            elif search_input == '':
                QMessageBox.critical(self, 'Error !!', 'Search input should be Required !!!')
            else:
                # Construct the SQL query based on the selected option and search input
                if selected_option == 'Email':
                    query = "SELECT Emp_No, Name, Email, Gender, Contact_No, DOB, DOJ, Password, User_Type, Address, Salary FROM employee WHERE Email = %s"
                elif selected_option == 'Name':
                    query = "SELECT Emp_No, Name, Email, Gender, Contact_No, DOB, DOJ, Password, User_Type, Address, Salary FROM employee WHERE Name = %s"
                elif selected_option == 'Contact':
                    query = "SELECT Emp_No, Name, Email, Gender, Contact_No, DOB, DOJ, Password, User_Type, Address, Salary FROM employee WHERE Contact = %s"
                else:
                    QMessageBox.critical(self, 'Error !!', 'Invalid search option')
                    return

                self.cur.execute(query, (search_input,))
                rows = self.cur.fetchall()
                self.Em_tableWidget.setRowCount(0)  # Clear previous results

                # Process and display the search results in the table
                if rows:
                    for row_data in rows:
                        row_position = self.Em_tableWidget.rowCount()
                        self.Em_tableWidget.insertRow(row_position)
                        for column_index, value in enumerate(row_data):
                            self.Em_tableWidget.setItem(row_position, column_index, QTableWidgetItem(str(value)))

                else:
                    QMessageBox.information(self, 'Search Result', 'No records found.')

        except Exception as e:
            QMessageBox.critical(self, 'Error !!', f'Error while searching: {str(e)}')
            if self.db is not None:
                self.db.close()

###############################################
######### Add Supplier To Database ############

    def Add_Supp_Data(self):
        self.db = MySQLdb.connect(host ='localhost' , user ='root' , password ='16031980' , db='laroussi_inventory')
        self.cur = self.db.cursor()

        self.cur.execute("SELECT * FROM supplier WHERE idsupplier = %s", (self.Supp_invoice_No.text(),))
        row = self.cur.fetchone()
        if row:
            self.status_bar = self.statusBar()
            self.status_bar.showMessage('Supplier ID is already registred!, Please try different...')
            QMessageBox.warning(self, 'Warrning', 'This Supplier ID already Assigned !!')

        elif (self.Supp_invoice_No.text() == '' or self.Supp_Name.text() == ''): 
            self.status_bar = self.statusBar()
            self.status_bar.showMessage('Supplier details must be required !!!...')
            QMessageBox.critical(self, 'Error!!', 'Supplier details must be required !!!') 
            
        else:
            self.cur.execute("INSERT INTO supplier (invoice_N, supplier_Name, contact_N, description_supplier) VALUES (%s, %s, %s, %s)",(
                                            self.Supp_invoice_No.text(),
                                            self.Supp_Name.text(),
                                            self.Supp_Contact_No.text(),
                                            self.Supp_Description.toPlainText(),
                        ))
            self.db.commit()
            QMessageBox.information(self, 'Success !!', 'Supplier Added Successfully')
            # Clear all input fields
            self.Supp_invoice_No.clear()
            self.Supp_Name.clear()
            self.Supp_Contact_No.clear()
            self.Supp_Description.clear()           
            self.Load_Supp_Data()

################################################
######### Load Supplier From Database ##########

    def Load_Supp_Data(self):
        try:
            self.db = MySQLdb.connect(host='localhost', user='root', password='16031980', db='laroussi_inventory')
            self.cur = self.db.cursor()
            self.cur.execute("SELECT invoice_N, supplier_Name, contact_N, description_supplier FROM supplier")
            row = self.cur.fetchall()
            self.Supp_tableWidget.setRowCount(len(row))
            self.Supp_tableWidget.setColumnCount(4)  # Adjust the number of columns

            for row_num, row_data in enumerate(row):
                for col_num, value in enumerate(row_data):
                    item = QTableWidgetItem(str(value))
                    self.Supp_tableWidget.setItem(row_num, col_num, item)
            
        except Exception as ex:
            # Handle the exception by displaying an error message
            QMessageBox.critical(self, 'Error', f'An error occurred: {str(ex)}')

        finally:
            # Close the database connection in the finally block
            if hasattr(self, 'db'):
                self.db.close()

################################################
######## Update From Supp_tableWidget ##########  
               
    def Update_Supp_Data(self):
        try:
            selected_row = self.Supp_tableWidget.currentRow()
            if selected_row >= 0:
                # Get the Supplier data from the selected row in the table
                Supp_invoice_NU = self.Supp_tableWidget.item(selected_row, 0).text()
                Supp_NamE = self.Supp_tableWidget.item(selected_row, 1).text()
                Supp_Contact_NU = self.Supp_tableWidget.item(selected_row, 2).text()
                Supp_Descr = self.Supp_tableWidget.item(selected_row, 3).text()

                # Display the Supplier details in the input fields for editing
                self.Supp_invoice_No.setText(Supp_invoice_NU)
                self.Supp_Name.setText(Supp_NamE)
                self.Supp_Contact_No.setText(Supp_Contact_NU)
                self.Supp_Description.setPlainText(Supp_Descr)

        except Exception as e:
                QMessageBox.critical(self, 'Error', f'Error updating supplier data: {str(e)}')

################################################
######## Update From Supplier Database #########  

    def Update_Supp_Record(self):
        try:
            selected_row = self.Supp_tableWidget.currentRow()
            if selected_row >= 0:
                # Get the data from the input fields
                idsupplier = self.Supp_invoice_No.text()
                Supp_invoice_NU = self.Supp_invoice_No.text()
                Supp_NamE = self.Supp_Name.text()
                Supp_Contact_NU = self.Supp_Contact_No.text()
                Supp_Descr = self.Supp_Description.toPlainText()

                self.db = MySQLdb.connect(host ='localhost' , user ='root' , password ='16031980' , db='laroussi_inventory')
                self.cur = self.db.cursor()

                update_query = """
                    UPDATE supplier
                    SET invoice_N=%s, supplier_Name=%s, contact_N=%s, description_supplier=%s
                    WHERE idsupplier=%s
                """
                self.cur.execute(update_query, (Supp_invoice_NU, Supp_NamE, Supp_Contact_NU, Supp_Descr, idsupplier))
                self.db.commit()
                QMessageBox.information(self, 'Success !!', 'Supplier Has Been Updated Successfully')
                
                # Update the data in the table widget
                self.Supp_tableWidget.setItem(selected_row, 0, QTableWidgetItem(Supp_invoice_NU))
                self.Supp_tableWidget.setItem(selected_row, 1, QTableWidgetItem(Supp_NamE))
                self.Supp_tableWidget.setItem(selected_row, 2, QTableWidgetItem(Supp_Contact_NU))
                self.Supp_tableWidget.setItem(selected_row, 3, QTableWidgetItem(Supp_Descr))

                # Update the data in the database (You should implement this part based on your database connection)
                # commit changes to the database

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error updating supplier data: {str(e)}')
        finally:
            # Close the database connection in the finally block
            if hasattr(self, 'db'):
                self.db.close()

#############################################
######## Delete Supplier Database ###########
 
    def Delete_Supp_Data(self):
        try:
            self.db = MySQLdb.connect(host ='localhost' , user ='root' , password ='16031980' , db='laroussi_inventory')
            self.cur = self.db.cursor()
            selected_row = self.Supp_tableWidget.currentRow()
            if selected_row >= 0:
                idsupplier = self.Supp_tableWidget.item(selected_row, 0).text()
                confirm_dialog = QMessageBox.question(self, 'Confirm Deletion', 'Are you sure you want to delete this Supplier?',
                                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if confirm_dialog == QMessageBox.Yes:

                    self.cur.execute("DELETE FROM supplier WHERE invoice_N = %s", (idsupplier,))
                    self.db.commit()
                    self.Supp_tableWidget.removeRow(selected_row) 
                    # Refresh the table to display the updated product list
                    self.Clear_Supp_Data()                                 
                    QMessageBox.information(self, 'Success !!', 'Supplier Has Been Deleted Successfully')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error deleting Supplier: {str(e)}')
            if self.db is not None:
                self.db.close()

#######################################
######## Clear Input Fields ###########

    def Clear_Supp_Data(self):
            self.Supp_invoice_No.clear()
            self.Supp_Name.clear()
            self.Supp_Contact_No.clear()
            self.Supp_Description.clear() 
            self.Load_Supp_Data()

###############################################
######## Search Supplier From Database ########

    def Search_Supp_Data(self):
        # Your database connection
        self.db = MySQLdb.connect(host ='localhost' , user ='root' , password ='16031980' , db='laroussi_inventory')
        self.cur = self.db.cursor()

        selected_option = self.Supp_SearchBy_Comb.currentText()
        search_input = self.Supp_Search_box.text()

        try:
            if selected_option == '':
                QMessageBox.critical(self, 'Error !!', 'Please, Select Search by Option First...')
            elif search_input == '':
                QMessageBox.critical(self, 'Error !!', 'Search input should be Required !!!')
            else:
                # Construct the SQL query based on the selected option and search input
                if selected_option == 'Invoice_N':
                    query = "SELECT invoice_N, supplier_Name, contact_N, description_supplier FROM supplier WHERE Invoice_N = %s"
                elif selected_option == 'Supplier_Name':
                    query = "SELECT invoice_N, supplier_Name, contact_N, description_supplier FROM supplier WHERE Supplier_Name = %s"
                elif selected_option == 'Contact_N':
                    query = "SELECT invoice_N, supplier_Name, contact_N, description_supplier FROM supplier WHERE Contact_N = %s"
                else:
                    QMessageBox.critical(self, 'Error !!', 'Invalid search option')
                    return

                self.cur.execute(query, (search_input,))
                rows = self.cur.fetchall()

                self.Supp_tableWidget.setRowCount(0)  # Clear previous results

                # Process and display the search results in the table
                if rows:
                    for row_data in rows:
                        row_position = self.Supp_tableWidget.rowCount()
                        self.Supp_tableWidget.insertRow(row_position)
                        for column_index, value in enumerate(row_data):
                            self.Supp_tableWidget.setItem(row_position, column_index, QTableWidgetItem(str(value)))

                else:
                    QMessageBox.information(self, 'Search Result', 'No records found.')

        except Exception as e:
            QMessageBox.critical(self, 'Error !!', f'Error while searching: {str(e)}')
            if self.db is not None:
                self.db.close()

###############################################
######### Add Category To Database ############

    def Add_Category_Data(self):
        self.db = MySQLdb.connect(host ='localhost' , user ='root' , password ='16031980' , db='laroussi_inventory')
        self.cur = self.db.cursor()

        self.cur.execute("SELECT * FROM category WHERE category_Name = %s", (self.Category_Input_Name.text(),))
        row = self.cur.fetchone()
        if row:
            self.status_bar = self.statusBar()
            self.status_bar.showMessage('Category ID is already registred!, Please try different...')
            QMessageBox.warning(self, 'Warrning', 'This Category ID already Assigned !!')

        elif (self.Category_Input_Name.text() == ''): 
            self.status_bar = self.statusBar()
            self.status_bar.showMessage('Category details must be required !!!...')
            QMessageBox.critical(self, 'Error!!', 'Category details must be required !!!') 
            
        else:
            self.cur.execute("INSERT INTO category (category_No, category_Name) VALUES (%s, %s)", (0, self.Category_Input_Name.text()))
            self.db.commit()
            QMessageBox.information(self, 'Success !!', 'Supplier Added Successfully')
            # Clear input field
            self.Category_Input_Name.clear()
            # Refresh the table
            self.Load_Category_Data()

################################################
######### Load Category From Database ##########

    def Load_Category_Data(self):
        try:
            self.db = MySQLdb.connect(host='localhost', user='root', password='16031980', db='laroussi_inventory')
            self.cur = self.db.cursor()
            self.cur.execute("SELECT category_Name FROM category")
            rows = self.cur.fetchall()
            self.Category_tableWidget.setRowCount(len(rows))
            self.Category_tableWidget.setColumnCount(2)  # Set the correct number of columns

            for row_num, row_data in enumerate(rows):
                category_No = row_num + 1  # Generate sequential numbers starting from 1
                self.Category_tableWidget.setItem(row_num, 0, QTableWidgetItem(str(category_No)))  # Display category_No
                self.Category_tableWidget.setItem(row_num, 1, QTableWidgetItem(str(row_data[0])))  # Display category_Name
            
        except Exception as ex:
            # Handle the exception by displaying an error message
            QMessageBox.critical(self, 'Error', f'An error occurred: {str(ex)}')

        finally:
            # Close the database connection in the finally block
            if hasattr(self, 'db'):
                self.db.close()

################################################
######## Update From Category_tableWidget ###### 
               
    def Update_Category_Data(self):
        try:
            selected_row = self.Category_tableWidget.currentRow()
            if selected_row >= 0:
                # Get the Category data from the selected row in the table
                category_NamE = self.Category_tableWidget.item(selected_row, 1).text()

                self.Category_Input_Name.setText(category_NamE)

        except Exception as e:
                QMessageBox.critical(self, 'Error', f'Error updating supplier data: {str(e)}')

#############################################
######## Delete Category Database ###########

    def Delete_Category_Data(self):
        try:
            self.db = MySQLdb.connect(host ='localhost' , user ='root' , password ='16031980' , db='laroussi_inventory')
            self.cur = self.db.cursor()
            selected_row = self.Category_tableWidget.currentRow()
            if selected_row >= 0:
                idcategory = self.Category_tableWidget.item(selected_row, 0).text()
                confirm_dialog = QMessageBox.question(self, 'Confirm Deletion', 'Are you sure you want to delete this Category?',
                                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if confirm_dialog == QMessageBox.Yes:

                    self.cur.execute("DELETE FROM category WHERE idcategory = %s", (idcategory,))
                    self.db.commit()
                    self.Category_tableWidget.removeRow(selected_row)            
                    QMessageBox.information(self, 'Success !!', 'Category Has Been Deleted Successfully')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error deleting category: {str(e)}')
            if self.db is not None:
                self.db.close()

#############################################
######### Add Product's To Database #########

    def Add_Products_Data(self):
        try:
            self.db = MySQLdb.connect(host='localhost', user='root', password='16031980', db='laroussi_inventory')
            self.cur = self.db.cursor()

            product_name = self.Product_Name.text()

            if product_name == '' or self.Product_Price.text() == '' or self.Product_Qty.text() == '' or self.Product_Supplier_Comb.currentText() == '0':
                self.status_bar = self.statusBar()
                self.status_bar.showMessage('Product details must be required !!!...')
                QMessageBox.critical(self, 'Error!!', 'Product details must be required !!!')

            else:
                # Check if a product with the same name already exists
                self.cur.execute("SELECT * FROM products WHERE products_Name = %s", (product_name,))
                row = self.cur.fetchone()
                if row:
                    self.status_bar = self.statusBar()
                    self.status_bar.showMessage('Product Name is already registered! Please try a different name.')
                    QMessageBox.warning(self, 'Warning', 'This Product Name is already assigned!')

                else:
                    self.cur.execute(
                        "INSERT INTO products (products_Supplier, products_Category, products_Name, products_Price, products_QTY, products_Status) VALUES (%s, %s, %s, %s, %s, %s)",
                        (
                                self.Product_Supplier_Comb.currentText(),
                                self.Product_Category_Comb.currentText(),
                                self.Product_Name.text(),
                                self.Product_Price.text(),
                                self.Product_Qty.text(),
                                self.Product_Status_Comb.currentText(),
                        ))
                    self.db.commit()
                    QMessageBox.information(self, 'Success !!', 'Product Added Successfully')

                    # Clear all input fields
                    self.Product_Supplier_Comb.setCurrentIndex(0)
                    self.Product_Category_Comb.setCurrentIndex(0)
                    self.Product_Name.clear()
                    self.Product_Price.clear()
                    self.Product_Qty.clear()
                    self.Product_Status_Comb.setCurrentIndex(0)

                    # Refresh the table to display the updated product list
                    self.Load_Products_Data()
                    self.Load_Sales_Products_Data()               

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'An error occurred: {str(e)}')

##########################################################
####### Fetch Supplier & Category From Database ##########

    def Fetch_Supplier_Category(self):
        try:
            self.db = MySQLdb.connect(host='localhost', user='root', password='16031980', db='laroussi_inventory')
            self.cur = self.db.cursor()
            
            self.cur.execute("SELECT category_Name FROM category")
            Category_List = self.cur.fetchall()
            
            self.Product_Category_Comb.clear()  # Clear existing items
            self.Product_Category_Comb.addItem("Select")  # Add the "Select" option
            for category in Category_List:
                self.Product_Category_Comb.addItem(category[0])  # Add category names to the combobox

            self.cur.execute("SELECT supplier_Name FROM supplier")
            Supplier_List = self.cur.fetchall()
            
            self.Product_Supplier_Comb.clear()  # Clear existing items
            self.Product_Supplier_Comb.addItem("Select")  # Add the "Select" option
            for supplier in Supplier_List:
                self.Product_Supplier_Comb.addItem(supplier[0])  # Add supplier names to the combobox

        except Exception as ex:
            # Handle the exception by displaying an error message
            QMessageBox.critical(self, 'Error', f'An error occurred: {str(ex)}')

            if self.db is not None:
                self.db.close()

################################################
######### Load Product's From Database #########

    def Load_Products_Data(self):
        try:
            self.db = MySQLdb.connect(host ='localhost' , user ='root' , password ='16031980' , db='laroussi_inventory')
            self.cur = self.db.cursor()
            self.cur.execute("SELECT idproducts, products_Supplier, products_Category, products_Name, products_Price, products_QTY, products_Status FROM products")
            row = self.cur.fetchall()
            self.Product_tableWidget.setRowCount(len(row))
            self.Product_tableWidget.setColumnCount(7)  # Adjust the number of columns

            for row_num, row_data in enumerate(row):
                for col_num, value in enumerate(row_data):
                    item = QTableWidgetItem(str(value))
                    self.Product_tableWidget.setItem(row_num, col_num, item)
            self.db.commit()
        except Exception as ex:           
            # Handle the exception by displaying an error message
            QMessageBox.critical(self, 'Error', f'An error occurred: {str(ex)}')
        finally:
            # Close the database connection in the finally block
            if hasattr(self, 'db'):
                self.db.close()

#######################################################
######## Update Product's From Em_tableWidget #########  
               
    def Update_Products_Data(self):
        try:
            selected_row = self.Product_tableWidget.currentRow()
            if selected_row >= 0:
                # Get the Products data from the selected row in the table
                idproducts = self.Product_tableWidget.item(selected_row, 0).text()
                products_Supp = self.Product_tableWidget.item(selected_row, 1).text()
                products_Categ = self.Product_tableWidget.item(selected_row, 2).text()
                Products_Name = self.Product_tableWidget.item(selected_row, 3).text()
                Products_Price = self.Product_tableWidget.item(selected_row, 4).text()
                Products_Qty = self.Product_tableWidget.item(selected_row, 5).text()
                Products_Status = self.Product_tableWidget.item(selected_row, 6).text()

                # Store the selected idproducts in the instance variable
                self.idproducts = idproducts
                # Display the Products details in the input fields for editing
                self.Product_Supplier_Comb.setCurrentText(products_Supp)
                self.Product_Category_Comb.setCurrentText(products_Categ)
                self.Product_Name.setText(Products_Name)
                self.Product_Price.setText(Products_Price)
                self.Product_Qty.setText(Products_Qty)
                self.Product_Status_Comb.setCurrentText(Products_Status)

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error updating idproducts data: {str(e)}')

#################################################
######## Update Product's From Database #########  

    def Update_Products_Record(self):
        try:
            if self.idproducts:  # Check if idproducts has a valid value
                # Get the data from the input fields
                idproducts = self.idproducts
                products_Supp = self.Product_Supplier_Comb.currentText()
                products_Categ = self.Product_Category_Comb.currentText()
                Products_Name = self.Product_Name.text()
                Products_Price = self.Product_Price.text()
                Products_Qty = self.Product_Qty.text()
                Products_Status = self.Product_Status_Comb.currentText()

                self.db = MySQLdb.connect(host ='localhost' , user ='root' , password ='16031980' , db='laroussi_inventory')
                self.cur = self.db.cursor()

                update_query = """
                    UPDATE products
                    SET products_Supplier=%s, products_Category=%s, products_Name=%s, products_Price=%s, products_QTY=%s, products_Status=%s
                    WHERE idproducts=%s
                """
                self.cur.execute(update_query, (products_Supp, products_Categ, Products_Name, Products_Price, Products_Qty, Products_Status, idproducts))
                self.db.commit()
                QMessageBox.information(self, 'Success !!', 'Products Has Been Updated Successfully')
                
                # Update the data in the table widget
                selected_row = self.Product_tableWidget.currentRow()
                if selected_row >= 0:
                    self.Product_tableWidget.setItem(selected_row, 0, QTableWidgetItem(idproducts))
                    self.Product_tableWidget.setItem(selected_row, 1, QTableWidgetItem(products_Supp))
                    self.Product_tableWidget.setItem(selected_row, 2, QTableWidgetItem(products_Categ))
                    self.Product_tableWidget.setItem(selected_row, 3, QTableWidgetItem(Products_Name))
                    self.Product_tableWidget.setItem(selected_row, 4, QTableWidgetItem(Products_Price))
                    self.Product_tableWidget.setItem(selected_row, 5, QTableWidgetItem(Products_Qty))
                    self.Product_tableWidget.setItem(selected_row, 6, QTableWidgetItem(Products_Status))

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error updating idproducts data: {str(e)}')

###########################################
######## Delete Product's Database ########
 
    def Delete_Products_Data(self):
        try:
            self.db = MySQLdb.connect(host ='localhost' , user ='root' , password ='16031980' , db='laroussi_inventory')
            self.cur = self.db.cursor()
            selected_row = self.Product_tableWidget.currentRow()
            if selected_row >= 0:
                idproducts = self.Product_tableWidget.item(selected_row, 0).text()
                confirm_dialog = QMessageBox.question(self, 'Confirm Deletion', 'Are you sure you want to delete this Products?',
                                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if confirm_dialog == QMessageBox.Yes:

                    self.cur.execute("DELETE FROM products WHERE idproducts = %s", (idproducts,))
                    self.db.commit()
                    self.Product_tableWidget.removeRow(selected_row)
                    # Refresh the table to display the updated product list
                    self.Clear_Products_Data()            
                    QMessageBox.information(self, 'Success !!', 'Products Has Been Deleted Successfully')

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error deleting products: {str(e)}')

            if self.db is not None:
                self.db.close()

###############################################
######## Clear Product's Input Fields ######### 

    def Clear_Products_Data(self):
            self.Product_Supplier_Comb.setCurrentIndex(0)
            self.Product_Category_Comb.setCurrentIndex(0)             
            self.Product_Name.clear()
            self.Product_Price.clear()
            self.Product_Qty.clear()
            self.Product_Status_Comb.setCurrentIndex(0)             

            self.Load_Products_Data()

###############################################
######## Search Product's From Database #######

    def Search_Products_Data(self):
        # Your database connection
        self.db = MySQLdb.connect(host ='localhost' , user ='root' , password ='16031980' , db='laroussi_inventory')
        self.cur = self.db.cursor()

        selected_option = self.Product_SearchBy_Comb.currentText()
        search_input = self.Product_SearchBox_Comb.text()

        try:
            if selected_option == '':
                QMessageBox.critical(self, 'Error !!', 'Please, Select Search by Option First...')
            elif search_input == '':
                QMessageBox.critical(self, 'Error !!', 'Search input should be Required !!!')
            else:
                # Construct the SQL query based on the selected option and search input
                if selected_option == 'Supplier':
                    query = "SELECT invoice_N, supplier_Name, contact_N, description_supplier FROM supplier WHERE supplier_Name = %s"
                elif selected_option == 'Category':
                    query = "SELECT category_No, category_Name FROM category WHERE category_Name = %s"                
                elif selected_option == 'Name':
                    query = "SELECT products_Supplier, products_Category, products_Name, products_Price, products_QTY, products_Status FROM products WHERE products_Name = %s"
                else:
                    QMessageBox.critical(self, 'Error !!', 'Invalid search option')
                    return

                self.cur.execute(query, (search_input,))
                rows = self.cur.fetchall()

                self.Product_tableWidget.setRowCount(0)  # Clear previous results

                # Process and display the search results in the table
                if rows:
                    for row_data in rows:
                        row_position = self.Product_tableWidget.rowCount()
                        self.Product_tableWidget.insertRow(row_position)
                        for column_index, value in enumerate(row_data):
                            self.Product_tableWidget.setItem(row_position, column_index, QTableWidgetItem(str(value)))

                else:
                    QMessageBox.information(self, 'Search Result', 'No records found.')

        except Exception as e:
            QMessageBox.critical(self, 'Error !!', f'Error while searching: {str(e)}')
            if self.db is not None:
                self.db.close()

###############################################
########  Sale's Tab Functions ################

    def Show_Bills(self):
        self.Invoice_listWidget.clear()
        Bills = "C:\\Users\\LAROUSSI\\Desktop\\Inventory Management System\\Bills"
        for i in os.listdir(Bills):
            if i.split('.')[-1] == 'txt':
                self.Invoice_listWidget.addItem(i)

    def Get_Data_Bills(self, item):
        file_name = item.text()
        self.Invoice_plainTextEdit.clear()
        try:
            with open(f'C:\\Users\\LAROUSSI\\Desktop\\Inventory Management System\\Bills\\{file_name}', 'r') as fp:
                content = fp.read()
                self.Invoice_plainTextEdit.setPlainText(content)
        except Exception as e:
            print(f"Error opening file '{file_name}': {str(e)}")

    def Search_Bills(self):
        invoice_number = self.Invoice_Sales.text()  # Assuming you have a method Invoice_Sales.text() to get the invoice number

        if invoice_number == '':
            QMessageBox.critical(self, 'Error !!', 'Invoice N. must be required !!!...')
        else:
            file_name = f'C:\\Users\\LAROUSSI\\Desktop\\Inventory Management System\\Bills\\{invoice_number}.txt'
            try:
                with open(file_name, 'r') as fp:
                    content = fp.read()
                    self.Invoice_plainTextEdit.clear()
                    self.Invoice_plainTextEdit.setPlainText(content)
            except Exception as e:
                QMessageBox.critical(self, 'Error !!', 'Invalid Invoice N°...!!!')
                self.Invoice_Sales.clear()

    def Clear_Search_Bills(self):
        self.Invoice_plainTextEdit.clear()
        self.Invoice_Sales.clear()
        
###############################################
######## Billing/Purchase Functions ###########

    # Calculator method
    def press_it(self, pressed):
        if pressed == 'C':
            self.Calc_Input.setText('0')
        else:
            if self.Calc_Input.text() == '0':
                self.Calc_Input.setText('')
            self.Calc_Input.setText(f'{self.Calc_Input.text()}{pressed}')

    def math_it(self):
        screen = self.Calc_Input.text()
        answer = eval(screen)
        self.Calc_Input.setText(str(answer))

#####################################################
######### Load Sales_Products From Database #########

    def Load_Sales_Products_Data(self):
        try:
            self.db = MySQLdb.connect(host='localhost', user='root', password='16031980', db='laroussi_inventory')
            self.cur = self.db.cursor()
            self.cur.execute("SELECT idproducts, products_Name, products_Price, products_QTY, products_Status FROM products")
            rows = self.cur.fetchall()
            self.Sales_Product_tableWidget.setRowCount(len(rows))
            self.Sales_Product_tableWidget.setColumnCount(5)  # Adjust the number of columns

            for row_num, row_data in enumerate(rows):
                for col_num, value in enumerate(row_data):
                    if col_num == 3:  # Assuming the quantity column is at index 3
                        item = QTableWidgetItem(str(int(value)))  # Convert quantity to int
                    else:
                        item = QTableWidgetItem(str(value))
                    self.Sales_Product_tableWidget.setItem(row_num, col_num, item)
            self.db.commit()
        except Exception as ex:
            # Handle the exception by displaying an error message
            QMessageBox.critical(self, 'Error', f'An error occurred: {str(ex)}')
        finally:
            # Close the database connection in the finally block
            if hasattr(self, 'db'):
                self.db.close()


#####################################################
######## Search Sales Product's From Database #######

    def Search_Sales_Products_Data(self):
        # Your database connection
        self.db = MySQLdb.connect(host='localhost', user='root', password='16031980', db='laroussi_inventory')
        self.cur = self.db.cursor()

        search_input = self.Sales_Search_Product_Input.text()

        try:
            if search_input == '':
                # Show an error message
                QMessageBox.critical(self, 'Error !!', 'Search input should be Required !!!')
                return

            if search_input == 'Name':
                # Select row with the name 'Name'
                query = "SELECT idproducts, products_Name, products_Price, products_QTY, products_Status FROM products WHERE products_Name = %s"
                self.cur.execute(query, ('Name',))

            else:
                # Select row with the given name (assuming 'search_input' is the name to search for)
                query = "SELECT idproducts, products_Name, products_Price, products_QTY, products_Status FROM products WHERE products_Name = %s"
                self.cur.execute(query, (search_input,))

            rows = self.cur.fetchall()

            # Process and display the search results in the table
            if rows:
                self.Sales_Product_tableWidget.setRowCount(0)  # Clear previous results
                for row_data in rows:
                    row_position = self.Sales_Product_tableWidget.rowCount()
                    self.Sales_Product_tableWidget.insertRow(row_position)
                    for column_index, value in enumerate(row_data):
                        self.Sales_Product_tableWidget.setItem(row_position, column_index, QTableWidgetItem(str(value)))
            else:
                # Display a message
                QMessageBox.information(self, 'Search Result', 'No records found.')

                # Load all rows again (modify the query as needed)
                query = "SELECT idproducts, products_Name, products_Price, products_QTY, products_Status FROM products"
                self.cur.execute(query)
                rows = self.cur.fetchall()

                if rows:
                    self.Sales_Product_tableWidget.setRowCount(0)  # Clear previous results
                    for row_data in rows:
                        row_position = self.Sales_Product_tableWidget.rowCount()
                        self.Sales_Product_tableWidget.insertRow(row_position)
                        for column_index, value in enumerate(row_data):
                            self.Sales_Product_tableWidget.setItem(row_position, column_index, QTableWidgetItem(str(value)))

        except Exception as e:
            QMessageBox.critical(self, 'Error !!', f'Error while searching: {str(e)}')
        finally:
            if self.db is not None:
                self.db.close()

##########################################
######## Show Quantity In Stock ##########

    def update_in_stock(self):
        selected_items = self.Sales_Product_tableWidget.selectedItems()
        if not selected_items:
            self.In_Stock.setText("[]")
            self.Product_Name_Bill_Area.clear()
            self.Price_PreQty_Bill_Area.clear()
            return

        row = selected_items[0].row()
        product_name = self.Sales_Product_tableWidget.item(row, 1).text()  # Assuming product name is in column 1
        product_price = self.Sales_Product_tableWidget.item(row, 2).text()  # Assuming product price is in column 2
        in_stock = self.Sales_Product_tableWidget.item(row, 3).text()  # Assuming QTY is in column 3

        # Update the QLineEdit widgets with the loaded data
        self.Product_Name_Bill_Area.setText(product_name)
        self.Price_PreQty_Bill_Area.setText(product_price)
        #self.Price_PreQty_Bill_Area.setText(product_price)
        self.In_Stock.setText(f"[{in_stock}]")


############################################
######## Add Update Cart ###################

    def Add_Update_Cart(self):
        if self.Cuantity_Bill_Area.text() == '':
            QMessageBox.critical(self, 'Error !!', 'Quantity should be Required !!!')
        elif int(self.Cuantity_Bill_Area.text().strip('[]')) > int(self.In_Stock.text().strip('[]')):
            QMessageBox.critical(self, 'Error !!', 'There is not enough quantity in stock !!!')    
        else:
            # Assuming you have some criteria to identify the product you want
            product_name = self.Product_Name_Bill_Area.text()

            self.db = MySQLdb.connect(host='localhost', user='root', password='16031980', db='laroussi_inventory')
            self.cur = self.db.cursor()
            # Modify your SQL query to retrieve the specific product by name
            self.cur.execute("SELECT idproducts, products_Price, products_QTY, products_Status FROM products WHERE products_Name = %s", (product_name,))
            row = self.cur.fetchone()  # Use fetchone() to retrieve one row

            price_cal = 0  # Initialize price_cal to 0

            if row:
                quantity = float(self.Cuantity_Bill_Area.text())
                price = float(row[1])  # Assuming products_Price is in the second column (index 1)
                price_cal = quantity * price

                # Extract the idproducts from the fetched row
                ID_Product = row[0]

                # Retrieve the selected product status from Product_Status_Comb
                product_status_index = self.Product_Status_Comb.currentIndex()
                product_status = self.Product_Status_Comb.itemText(product_status_index)

                # Load 'idproducts, products_Name, products_Price, products_QTY, products_Status' into cart_data
                cart_data = [
                    ID_Product,
                    product_name, 
                    price_cal, 
                    quantity,
                    product_status
                ]
            else:
                QMessageBox.critical(self, 'Error !!', 'Product not found !!!')

            # Update the Cart
            present = 'no'
            index_ = 0
            for row in self.Cart_List:
                if ID_Product == row[0]:
                    present = 'yes'
                    break
                index_ += 1
            if present == 'yes':
                Op = QMessageBox.question(self, 'Confirm Deletion', 'Product already present\nDo you want to update?| Remove from the Cart List')
                if Op == QMessageBox.Yes:
                    if self.Cuantity_Bill_Area.text() == '0':
                        self.Cart_List.pop(index_)
                    else:
                        print("Updating row")
                        self.Cart_List[index_][2] = price_cal  # Update the price with the calculated price
                        self.Cart_List[index_][3] = int(self.Cuantity_Bill_Area.text())  # Update the quantity as an integer

                    # Subtract the quantity from Product_Cart_tableWidget and update the database
                    new_quantity_in_cart = int(self.Cuantity_Bill_Area.text())
                    current_quantity_in_stock = int(self.In_Stock.text().strip('[]'))
                    remaining_quantity_in_stock = current_quantity_in_stock - new_quantity_in_cart

                    # Update the Product_Cart_tableWidget
                    self.In_Stock.setText(f"[{remaining_quantity_in_stock}]")

                    # Update the database with the new quantity
                    self.cur.execute("UPDATE products SET products_QTY = %s WHERE products_Name = %s", (remaining_quantity_in_stock, product_name))
                    self.db.commit()

            else:
                self.Cart_List.append(cart_data)
            
            self.Show_Cart()
            self.Bill_Updates()

###########################################
######## Update Bill ######################

    def Bill_Updates(self):
        self.bill_amnt= 0 
        self.net_pay = 0
        self.discount = 0
        for row in self.Cart_List:
            self.bill_amnt = self.bill_amnt + float(row[2])

        self.discount = (self.bill_amnt * 5)/100   
        self.net_pay = self.bill_amnt-self.discount
        self.Label_Bill_Amnt.setText(f"[{self.bill_amnt}]")
        self.Label_Net_Pay.setText(f"[{self.net_pay}]")
        self.Label_Total_Products.setText(f"[{str(len(self.Cart_List))}]")  

###########################################
######## Add Show Cart ####################

    def Show_Cart(self):
        try:
            # Clear the cart table
            self.Product_Cart_tableWidget.setRowCount(0)
            
            # Iterate through the rows in Cart_List and add them to the cart table
            for row_data in self.Cart_List:
                row_position = self.Product_Cart_tableWidget.rowCount()
                self.Product_Cart_tableWidget.insertRow(row_position)

                # Assuming row_data contains ['idproducts', 'products_Name', 'products_Price', 'products_QTY', 'products_Status']
                for column_index, value in enumerate(row_data):
                    item = QTableWidgetItem(str(int(value) if column_index == 3 else value))  # Convert quantity to int
                    self.Product_Cart_tableWidget.setItem(row_position, column_index, item)
        except Exception as ex:           
            # Handle the exception by displaying an error message
            QMessageBox.critical(self, 'Error', f'An error occurred: {str(ex)}')

###########################################
######## Generate Bills ###################

    def Generate_Bills(self):
        if self.Costomer_Name.text() == '' or self.Contact_N.text() == '':
            QMessageBox.critical(self, 'Error !!', 'Customer Details should be Required !!!')
        elif len(self.Cart_List) == 0:
            QMessageBox.critical(self, 'Error !!', 'Please Add Product To The Cart !!!')
        else:
            ### Bill Top ####
            bill_top = self.Bill_Top()
            ### Bill Middle ####
            bill_middle = self.Bill_Middle()  # Get the bill middle content
            ### Bill Bottom ####
            bill_bottom = self.Bill_Bottom()
            
            # Subtract quantities from Product_Cart_tableWidget and update the database
            for cart_item in self.Cart_List:
                product_name = cart_item[1]
                quantity_in_cart = cart_item[3]
                
                # Update the Product_Cart_tableWidget
                for row in range(self.Sales_Product_tableWidget.rowCount()):
                    if self.Sales_Product_tableWidget.item(row, 1).text() == product_name:
                        current_quantity_in_stock = int(self.Sales_Product_tableWidget.item(row, 3).text())
                        remaining_quantity_in_stock = current_quantity_in_stock - quantity_in_cart
                        self.Sales_Product_tableWidget.item(row, 3).setText(str(remaining_quantity_in_stock))
                        
                        # Update the database with the new quantity
                        self.cur.execute("UPDATE products SET products_QTY = %s WHERE products_Name = %s", (remaining_quantity_in_stock, product_name))
                        self.db.commit()

            # Combine the content from Bill_Top, Bill_Middle, and Bill_Bottom
            full_bill = bill_top + bill_middle + bill_bottom

            # Replace any occurrences of ".0" with an empty string in the full_bill
            full_bill = full_bill.replace('.0', '')

            self.Costomer_Bill_Area.setPlainText(full_bill)

            fp = open(f'Bills/{str(self.invoice)}.txt','w')
            fp.write(self.Costomer_Bill_Area.toPlainText())
            fp.close()
            QMessageBox.information(self, 'Saved', 'Bill has been Generated/Save in Backend !!!')
            self.Set_Print = 1

###########################################
######## Bill's Content ###################

    def Bill_Top(self):
        self.invoice = int(time.strftime('%H%M%S')) + int(time.strftime('%d%m%Y'))
        bill_top_temp = f'''
\t\tLAROUSSI-Inventory
\t Phone N°. +213***** , Ouled Djellal-07002
{str('='*53)}
Costomer Name : {self.Costomer_Name.text()}
Phone N° : {self.Contact_N.text()}
Bill N°. {str(self.invoice)}\t\t\tDate : {str(time.strftime('%d/%m/%Y'))}
{str('='*53)}
Product Name\t\tQty\t\tPrice 
{str('='*53)}
        '''
        self.Costomer_Bill_Area.clear()
        self.Costomer_Bill_Area.setPlainText(bill_top_temp)
        return bill_top_temp  # Return the content

    def Bill_Bottom(self):
        bill_bottom_temp = f'''
{str('='*53)}
Bill Amount\t\t\t\tDA.{self.bill_amnt}
Discount\t\t\t\tDA.{self.discount}
Net Pay\t\t\t\tDA.{self.net_pay}
{str('='*53)}\n
        '''
        self.Costomer_Bill_Area.setPlainText(bill_bottom_temp)
        return bill_bottom_temp  # Return the content    

    def Bill_Middle(self):
        bill_middle_temp = ''
        for row in self.Cart_List:
            Name = row[1]
            QTY = str(row[3])  # Convert QTY to string
            Price = int(float(row[2]) * int(row[3]))  # Convert to int before converting to string
            # Accumulate the lines
            bill_middle_temp += '\n' + Name + '\t\t' + QTY + '\t\tDA.' + str(Price)  # Convert Price to string here
        return bill_middle_temp  # Return the bill middle content

###########################################
######## Clear All ########################

    def Clear_Cart(self):
        self.Product_Name_Bill_Area.clear()
        self.Price_PreQty_Bill_Area.clear()
        self.Cuantity_Bill_Area.clear()
        self.In_Stock.clear()

    def Clear_All(self):
        del self.Cart_List[:]
        self.Costomer_Name.clear()
        self.Contact_N.clear()
        self.Costomer_Bill_Area.clear()
        self.Label_Total_Products.setText(f"[0]")
        self.Sales_Search_Product_Input.clear()
        self.Clear_Cart()
        self.show()
        self.Show_Cart()

###########################################
######## Display Date & Time ##############

    def Update_Date_Time(self):
        current_time = time.strftime('%I:%M:%S')
        current_date = time.strftime('%d-%m-%Y')
        self.Date_Time.setText(f'Welcome to Laroussi Inventory Management System\t\t\t\t Date : {current_date}\t\t\t\t Time : {current_time}')

    def Print_Bill(self):
        if self.Set_Print == 1:
            QMessageBox.information(self, 'Print', 'Please wait while Printing !!!')
            new_file = tempfile.mktemp('.txt')
            open(new_file, 'w').write(self.Costomer_Bill_Area.toPlainText())
            os.startfile(new_file, 'print')            
        else:
            QMessageBox.critical(self, 'Print', 'Please Generate Bill, to print the receipt !!!')

###########################################
######## Dashboard Functions ##############

    def Dashboard_Content(self):
            self.db = MySQLdb.connect(host='localhost', user='root', password='16031980', db='laroussi_inventory')
            self.cur = self.db.cursor()
            try:

                self.cur.execute('SELECT * FROM employee')
                employee = self.cur.fetchall()
                self.Total_Employee_Label.setText(f"[{str(len(employee))}]")

                self.cur.execute('SELECT * FROM supplier')
                supplier = self.cur.fetchall()
                self.Total_Supplier_Label.setText(f"[{str(len(supplier))}]")

                self.cur.execute('SELECT * FROM category')
                category = self.cur.fetchall()
                self.Total_Category_Label.setText(f"[{str(len(category))}]")

                self.cur.execute('SELECT * FROM products')
                products = self.cur.fetchall()
                self.Total_Products_Label.setText(f"[{str(len(products))}]")

                Bills = len(os.listdir('Bills'))
                self.Total_Sales_Label.setText(f"[{Bills}]")

                self.db.commit()
            except Exception as ex:           
                # Handle the exception by displaying an error message
                QMessageBox.critical(self, 'Error', f'An error occurred: {str(ex)}')

    def ExitConfirmation(self):
        reply = QMessageBox.question(self, 'Exit Confirmation', 'Are you sure you want to exit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # User clicked 'Yes,' so exit the application
            QApplication.quit()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
