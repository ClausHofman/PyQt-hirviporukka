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
        connectionArguments = databaseOperation1.readDatabaseSettingsFromFile('settings.dat')
        databaseOperation1.getAllRowsFromTable(connectionArguments, 'public.jaetut_lihat')
        print(databaseOperation1.detailedMessage)
        #: TODO MessageBox if an error occured
        prepareData.prepareTable(databaseOperation1, self.summaryMeatSharedTableWidget)

        # Read data from view jakoryhma_yhteenveto, no need to read connection args twice
        databaseOperation2 = pgModule.DatabaseOperation()
        databaseOperation2.getAllRowsFromTable(connectionArguments, 'public.jakoryhma_yhteenveto')
        #: TODO MessageBox if an error occured
        prepareData.prepareTable(databaseOperation2, self.summaryGroupInfoTableWidget)
    
    def populateKillPage(self):
        # Read data from view kaatoluettelo
        databaseOperation1 = pgModule.DatabaseOperation()
        connectionArguments = databaseOperation1.readDatabaseSettingsFromFile('settings.dat')
        databaseOperation1.getAllRowsFromTable(connectionArguments, 'public.kaatoluettelo')
        print(databaseOperation1.detailedMessage)
        #: TODO MessageBox if an error occured
        prepareData.prepareTable(databaseOperation1, self.killPageKillsTW)
        prepareData.prepareTable(databaseOperation1, self.summaryGroupInfoTableWidget)

        # Read data from view nimivalinta
        databaseOperation2 = pgModule.DatabaseOperation()
        databaseOperation2.getAllRowsFromTable(connectionArguments, 'public.nimivalinta')
        self.shotById = prepareData.prepareComboBox(databaseOperation2, self.shotByCB, 1, 0)

    def populateAllPages(self):
        self.populateSummaryPage()
        self.populateKillPage()
    


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

    # Create the Main Window object from kayttoliittyma Class
    appWindow = Kayttoliittyma()
    appWindow.show()
    sys.exit(app.exec_())