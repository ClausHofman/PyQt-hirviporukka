# APPLICATION FOR SHOWING SUMMARY DATA ABOUT MEAT GIVEN TO SHARE GROUP
# ====================================================================

# LIBRARIES AND MODULES
# ---------------------

import sys # Needed for starting the application
from PyQt5.QtWidgets import * # All widgets
from PyQt5.uic import loadUi
from PyQt5.QtCore import * # FIXME: Everything, change to individual components
from datetime import date
import pgModule
import prepareData

# CLASS DEFINITIONS FOR THE APP
# -----------------------------

class Kayttoliittyma(QMainWindow):
    
    # Constructor, a method for creating objects from this class
    def __init__(self):
        QMainWindow.__init__(self)

        # Create an UI from the ui file
        loadUi('kayttoliittyma.ui', self)

        # Read database connection arguments from the settings file
        databaseOperation = pgModule.DatabaseOperation()
        # self.connectionArguments = databaseOperation.readDatabaseSettingsFromFile('settings.dat')
        self.connectionArguments = databaseOperation.readDatabaseSettingsFromFile(
            'settings.dat')
        
        # UI ELEMENTS TO PROPERTIES
        # -------------------------

        # Create a status bar to show informative messages (replaces print function used in previous exercises)
        self.statusBar = QStatusBar()  # Create a status bar object
        # Set it as the status bar for the main window
        self.setStatusBar(self.statusBar)
        self.statusBar.show()  # Make it visible

        # Set current date when the app starts
        self.currentDate = date.today()        
        
        # Summary page (Yhteenveto)
        self.summaryRefreshBtn = self.meatSharedPushButton
        self.summaryMeatSharedTableWidget = self.meatSharedTableWidget
        self.summaryGroupInfoTableWidget = self.groupSummaryTableWidget

        # Kill page
        self.shotByCB = self.shotByComboBox
        self.killPageDate = self.killPageDateEdit
        self.killPageLocation = self.locationLineEdit
        self.killPageAnimalCB = self.animalComboBox
        self.killPageAgeGroupCB = self.ageGroupComboBox
        self.killPageGenderCB = self.genderComboBox
        self.killPageWeightLE = self.killPageWeightLineEdit
        self.killPageUsageCB = self.killPageUsageComboBox
        self.killPageInfoTE = self.killPageAdditionalInfoPlainTextEdit
        self.killPageSaveBtn = self.saveShotPushButton
        self.killPageSaveBtn.clicked.connect(self.saveShot) # Signal
        self.killPageKillsTW = self.killPageKillsTableWidget

        # Shared meat page
        self.meatSharePageKillsTW = self.meatSharePageKillsTableWidget
        self.meatSharePageDate = self.meatSharePageDateEdit
        self.meatSharePageSharedGroupCB = self.meatSharePageShareGroupComboBox
        self.meatSharePageAnimalPartCB = self.meatSharePageAnimalPartComboBox
        self.meatSharePageWeightLE = self.meatSharePageWeightLineEdit
        self.meatSharePageSaveBtn = self.meatSharePageSavePushButton
        self.meatSharePageGrpBox = self.meatSharePageGroupBox

        # License page
        self.licenseYearLE = self.licenseYearLineEdit
        self.licenseAnimalCB = self.licenseAnimalComboBox
        self.licenseAgeGroupCB = self.licenseAgeGroupComboBox
        self.licenseGenderCB = self.licenseGenderComboBox
        self.licenseAmountLE = self.licenseAmountLineEdit
        self.licenseSaveBtn = self.licenseSaveButton
        self.licenseSummaryTW = self.licenseSummaryTableWidget

        # Signal when a page is opened
        self.pageTab = self.tabWidget
        self.pageTab.currentChanged.connect(self.populateAllPages)


        # OTHER SIGNALS THAN EMITTED BY UI ELEMENTS
        self.populateAllPages()


        # Emit a signal when refresh push button is pressed
        self.summaryRefreshBtn.clicked.connect(self.populateSummaryPage)


    # SLOTS
        
    # Create an alert dialog for critical failures, eg no database connection established
    def alert(self, windowTitle, alertMsg, additionalMsg, details):
        """Creates a message box for critical errors
        Args:
            windowTitle (str): Title of the message box
            alertMsg (str): Short description of the error in Finnish
            additionalMsg (str): Additional information in Finnish
            details (str): Details about the error in English
        """
        alertDialog = QMessageBox()  # Create a message box object
        # Add appropriate title to the message box
        alertDialog.setWindowTitle(windowTitle)
        alertDialog.setIcon(QMessageBox.Critical)  # Set icon to critical
        # Basic information about the error in Finnish
        alertDialog.setText(alertMsg)
        # Additional information about the error in Finnish
        alertDialog.setInformativeText(additionalMsg)
        # Technical details in English (from psycopg2)
        alertDialog.setDetailedText(details)
        # Only OK is needed to close the dialog
        alertDialog.setStandardButtons(QMessageBox.Ok)
        alertDialog.exec_()  # Open the message box        
    
    # A method to populate summaryPage's table widgets
        
    def populateSummaryPage(self):

        # Read data from view jaetut_lihat
        databaseOperation1 = pgModule.DatabaseOperation()

        databaseOperation1.getAllRowsFromTable(
                self.connectionArguments, 'public.jaetut_lihat')
        print(databaseOperation1.detailedMessage)

        #: TODO MessageBox if an error occured
        # prepareData.prepareTable(databaseOperation1, self.summaryMeatSharedTableWidget)

        # Read data from view jakoryhma_yhteenveto, no need to read connection args twice
        databaseOperation2 = pgModule.DatabaseOperation()
        databaseOperation2.getAllRowsFromTable(
            self.connectionArguments, 'public.jakoryhma_yhteenveto')
        
        # Check if error has occurred
        if databaseOperation2.errorCode != 0:
            self.alert('Vakava virhe', 'Tietokantaoperaatio epäonnistui',
                       databaseOperation2.errorMessage, databaseOperation2.detailedMessage)
        else:
            prepareData.prepareTable(
                databaseOperation2, self.summaryMeatSharedTableWidget)
        
        #: TODO MessageBox if an error occured
        prepareData.prepareTable(
                databaseOperation2, self.summaryGroupInfoTableWidget)
        
        # Check if error has occurred
        if databaseOperation2.errorCode != 0:
            self.alert('Vakava virhe', 'Tietokantaoperaatio epäonnistui',
                       databaseOperation2.errorMessage, databaseOperation2.detailedMessage)
        else:
            prepareData.prepareTable(
                databaseOperation2, self.summaryGroupInfoTableWidget)
    
    def populateKillPage(self):
        # Set default date to current date
        self.killPageDate.setDate(self.currentDate)
        # Read data from view kaatoluettelo
        databaseOperation1 = pgModule.DatabaseOperation()
        databaseOperation1.getAllRowsFromTable(self.connectionArguments, 'public.kaatoluettelo')
        print(databaseOperation1.detailedMessage)

        # Check if error has occurred
        if databaseOperation1.errorCode != 0:
            self.alert('Vakava virhe', 'Tietokantaoperaatio epäonnistui',
                       databaseOperation1.errorMessage, databaseOperation1.detailedMessage)
        else:
            prepareData.prepareTable(databaseOperation1, self.killPageKillsTW)

        # Read data from view nimivalinta
        databaseOperation2 = pgModule.DatabaseOperation()
        databaseOperation2.getAllRowsFromTable(
            self.connectionArguments, 'public.nimivalinta')
        
        # Check if error has occurred
        if databaseOperation2.errorCode != 0:
            self.alert('Vakava virhe', 'Tietokantaoperaatio epäonnistui',
                       databaseOperation2.errorMessage, databaseOperation2.detailedMessage)
        else:
            self.shotByIdList = prepareData.prepareComboBox(
                databaseOperation2, self.shotByCB, 1, 0)

        # Read data from table elain and populate the combo box
        databaseOperation3 = pgModule.DatabaseOperation()
        databaseOperation3.getAllRowsFromTable(
            self.connectionArguments, 'public.elain')

        # Check if error has occurred
        if databaseOperation3.errorCode != 0:
            self.alert('Vakava virhe', 'Tietokantaoperaatio epäonnistui',
                       databaseOperation3.errorMessage, databaseOperation3.detailedMessage)
        else:
            self.shotAnimalText = prepareData.prepareComboBox(
                databaseOperation3, self.killPageAnimalCB, 0, 0)

        # Read data from table aikuinenvasa and populate the combo box
        databaseOperation4 = pgModule.DatabaseOperation()
        databaseOperation4.getAllRowsFromTable(
            self.connectionArguments, 'public.aikuinenvasa')
        
        # Check if error has occurred
        if databaseOperation4.errorCode != 0:
            self.alert('Vakava virhe', 'Tietokantaoperaatio epäonnistui',
                       databaseOperation4.errorMessage, databaseOperation4.detailedMessage)            
        else:
            self.shotAgeGroupText = prepareData.prepareComboBox(
                databaseOperation4, self.killPageAgeGroupCB, 0, 0)

        # Read data from table sukupuoli and populate the combo box
        databaseOperation5 = pgModule.DatabaseOperation()
        databaseOperation5.getAllRowsFromTable(
            self.connectionArguments, 'public.sukupuoli')
        
        if databaseOperation5.errorCode != 0:
            self.alert('Vakava virhe', 'Tietokantaoperaatio epäonnistui',
                       databaseOperation5.errorMessage, databaseOperation5.detailedMessage)
        else:            
            self.shotGenderText = prepareData.prepareComboBox(
                databaseOperation5, self.killPageGenderCB, 0, 0)

        # Read data from table kasittely
        databaseOperation6 = pgModule.DatabaseOperation()
        databaseOperation6.getAllRowsFromTable(
            self.connectionArguments, 'public.kasittely')
        
        if databaseOperation6.errorCode != 0:
            self.alert('Vakava virhe', 'Tietokantaoperaatio epäonnistui',
                       databaseOperation6.errorMessage, databaseOperation6.detailedMessage)
        else:            
            self.shotUsageIdList = prepareData.prepareComboBox(
                databaseOperation6, self.killPageUsageCB, 1, 0)


    def populateAllPages(self):
        self.populateSummaryPage()
        self.populateKillPage()
    
    def saveShot(self):
        # TODO: Add error handling and msg box when an error occurs
        try:
            shotByChosenItemIx = self.shotByCB.currentIndex() # Row index of the selected row
            shotById = self.shotByIdList[shotByChosenItemIx] # Id of the selected row
            shootingDay = self.killPageDate.date().toPyDate() # Python date is in ISO format
            shootingPlace = self.killPageLocation.text() # Text value of the line edit
            animal = self.killPageAnimalCB.currentText() # Selected text of the combo box
            ageGroup = self.killPageAgeGroupCB.currentText() # Selected text of the combo box
            gender = self.killPageGenderCB.currentText() # Selected text of the combo box
            weight = float(self.killPageWeightLE.text()) # Convert line edit value to float (real in the DB)
            useIx = self.killPageUsageCB.currentIndex() # Row index of the selected row
            use = self.shotUsageIdList[useIx] # Id value of the selected row
            additionalInfo = self.killPageInfoTE.toPlainText() # Convert multiline text edit to plain text

            # Insert data into kaato table

            # Create a SQL clause to insert element values to the DB
            sqlClauseBeginning = "INSERT INTO public.kaato(jasen_id, kaatopaiva, ruhopaino, paikka_teksti, kasittelyid, elaimen_nimi, sukupuoli, ikaluokka, lisatieto) VALUES("
            sqlClauseValues = f"{shotById}, '{shootingDay}', {weight}, '{shootingPlace}', {use}, '{animal}', '{gender}', '{ageGroup}', '{additionalInfo}'"
            sqlClauseEnd = ");"
            sqlClause = sqlClauseBeginning + sqlClauseValues + sqlClauseEnd
        except:
            self.alert('Virheellinen syöte', 'Tarkista antamasi tiedot', 'jotain meni väärin','hippopotamus')
        
        print(sqlClause) # FIXME: Remove this line in production
        
        # Create a database operation object to execute the SQL clause
        databaseOperation = pgModule.DatabaseOperation()
        databaseOperation.insertRowToTable(self.connectionArguments, sqlClause)

        if databaseOperation.errorCode != 0:
            self.alert('Vakava virhe', 'Tietokantaoperaatio epäonnistui',
                       databaseOperation.errorMessage, databaseOperation.detailedMessage)
        else:
            # Update the page to show new data and clear previous data from elements
            self.populateKillPage()
            self.killPageLocation.clear()
            self.killPageWeightLE.clear()
            self.killPageInfoTE.clear()        
        '''    
        # To avoid Fatal error crashing the app use try-except-finally structure
        try:
            # Create a connection object
            dbaseconnetion = psycopg2.connect(database=self.database, user=self.user, password=self.userPassword,
                                            host=self.server, port=self.port)
            
            # Create a cursor to execute commands and retrieve result set
            cursor = dbaseconnetion.cursor()
            
            # Execute a SQL command to get hunters (jasen)
            command = "SELECT * FROM public.jaetut_lihat;"
            cursor.execute(command)
            result_set = cursor.fetchall()
            print("Lihaa on jaettu seuraavasti:", result_set)

        # Throw an error if connection or cursor creation fails                                     
        except(Exception, psycopg2.Error) as e:
            print("Tietokantayhteydessä tapahtui virhe", e)

        # If or if not successfull close the cursor and the connection   
        finally:
            if (dbaseconnetion):
                cursor.close()
                dbaseconnetion.close()
                print("Yhteys tietokantaan katkaistiin")
    '''

# Check if app will be created and started directly 
if __name__ == "__main__":

    # Create an application object
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    # Create the Main Window object from Kayttoliittyma Class
    appWindow = Kayttoliittyma()
    appWindow.show() # This can also be included in the Kayttoliittyma class
    sys.exit(app.exec_())