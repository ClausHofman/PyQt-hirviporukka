# APPLICATION FOR SHOWING SUMMARY DATA ABOUT MEAT GIVEN TO SHARE GROUP
# ====================================================================

# LIBRARIES AND MODULES
# ---------------------

import sys # Needed for starting the application
from PyQt5.QtWidgets import * # All widgets
from PyQt5.uic import loadUi
from PyQt5.QtCore import * # FIXME: Everything, change to individual components
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
        self.connectionArguments = databaseOperation.readDatabaseSettingsFromFile('settings.dat')

        # UI ELEMENTS TO PROPERTIES
        # -------------------------

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
        self.killPageSaveBtn.clicked.connect(self.saveShot)
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
    
    # Agent method is used for receiving a signal from an UI element
    def populateSummaryPage(self):

        # Read data from view jaetut_lihat
        databaseOperation1 = pgModule.DatabaseOperation()

        databaseOperation1.getAllRowsFromTable(self.connectionArguments, 'public.jaetut_lihat')
        print(databaseOperation1.detailedMessage)
        #: TODO MessageBox if an error occured
        prepareData.prepareTable(databaseOperation1, self.summaryMeatSharedTableWidget)

        # Read data from view jakoryhma_yhteenveto, no need to read connection args twice
        databaseOperation2 = pgModule.DatabaseOperation()
        databaseOperation2.getAllRowsFromTable(self.connectionArguments, 'public.jakoryhma_yhteenveto')
        #: TODO MessageBox if an error occured
        prepareData.prepareTable(databaseOperation2, self.summaryGroupInfoTableWidget)
    
    def populateKillPage(self):
        # Read data from view kaatoluettelo
        databaseOperation1 = pgModule.DatabaseOperation()
        connectionArguments = databaseOperation1.readDatabaseSettingsFromFile('settings.dat')
        databaseOperation1.getAllRowsFromTable(self.connectionArguments, 'public.kaatoluettelo')
        print(databaseOperation1.detailedMessage)
        #: TODO MessageBox if an error occured
        prepareData.prepareTable(databaseOperation1, self.killPageKillsTW)
        prepareData.prepareTable(databaseOperation1, self.summaryGroupInfoTableWidget) # poista?

        # Read data from view nimivalinta
        databaseOperation2 = pgModule.DatabaseOperation()
        databaseOperation2.getAllRowsFromTable(
            self.connectionArguments, 'public.nimivalinta')
        self.shotByIdList = prepareData.prepareComboBox(
            databaseOperation2, self.shotByCB, 1, 0)

        # Read data from table elain and populate the combo box
        databaseOperation3 = pgModule.DatabaseOperation()
        databaseOperation3.getAllRowsFromTable(
            self.connectionArguments, 'public.elain')
        self.shotAnimalText = prepareData.prepareComboBox(
            databaseOperation3, self.killPageAnimalCB, 0, 0)

        # Read data from table aikuinenvasa and populate the combo box
        databaseOperation4 = pgModule.DatabaseOperation()
        databaseOperation4.getAllRowsFromTable(
            self.connectionArguments, 'public.aikuinenvasa')
        self.shotAgeGroupText = prepareData.prepareComboBox(
            databaseOperation4, self.killPageAgeGroupCB, 0, 0)

        # Read data from table sukupuoli and populate the combo box
        databaseOperation5 = pgModule.DatabaseOperation()
        databaseOperation5.getAllRowsFromTable(
            self.connectionArguments, 'public.sukupuoli')
        self.shotGenderText = prepareData.prepareComboBox(
            databaseOperation5, self.killPageGenderCB, 0, 0)

        # Read data from table kasittely
        databaseOperation6 = pgModule.DatabaseOperation()
        databaseOperation6.getAllRowsFromTable(
            self.connectionArguments, 'public.kasittely')
        self.shotUsageIdList = prepareData.prepareComboBox(
            databaseOperation6, self.killPageUsageCB, 1, 0)


    def populateAllPages(self):
        self.populateSummaryPage()
        self.populateKillPage()
    
    def saveShot(self):
        # TODO: Add error handling and msg box when an error occurs
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
        
        print(sqlClause) # FIXME: Remove this line in production
        
        # Create a database operation object to execute the SQL clause
        databaseOperation = pgModule.DatabaseOperation()
        databaseOperation.insertRowToTable(self.connectionArguments, sqlClause)

        # TODO: Add refresh method to update kaadot table widget
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