# MODULE FOR CREATING DATABASE CONNECTIONS AND OPERATIONS
# =======================================================

# LIBRARIES AND MODULES
# ---------------------

import psycopg2 # Database
import datetime # For handling date and time values
import decimal # For handling decimal datatypes with extreme precision
import json # For converting settings to JSON format

#  CLASS DEFINITIONS
# ------------------

class DatabaseOperation():
    """Creates a connection to postgreSQL database and
    executes various SQL commands"""

    # Constructor method: create a new object and set initial properties
    def __init__(self):
        self.errorCode = 0
        self.errorMessage = 'OK'
        self.detailedMessage = 'No errors' 
        self.resultSet = []
        self.columnHeaders = []
        self.rows = 0
        self.columns = 0

    # Method for creating connection arguments
    def createConnectionArgumentDict(self, database, role, pwd, host='localhost', port='5432'):
        """Creates a dictionary from connection arguments

        Args:
            database (str): Database name
            role (str): Role ie. username
            pwd (str): Password
            host (str, optional): Server name or IP address. Defaults to 'localhost'.
            port (str, optional): Server's TCP port. Defaults to '5432'.

        Returns:
            dict: Connection arguments as key-value-pairs
        """
        return connectionArgumentDict

    # Method for saving connection arguments to a settings file

    def saveDatabaseSettingsToFile(self, file, connectionArgs):
        """Saves conection arguments to JSON based settings file

        Args:
            file (str): Name of the JSON settings file
            connectionArgs (dict): Connection arguments in key-value-pairs
        """
        pass

    # Method for reading connection arguments from the settings file
    def readDatabaseSettingsFromFile(self, file):
        """Reads conection arguments to JSON based settings file

        Args:
            file (str): Name of the settings file
        
        Returns:
            dict: Connection arguments in key-value-pairs
        """
        return connectionArgumentDict
    # Method to get all rows from a given table
    def getAllRowsFromTable(self, connectionArgs, table):
        """Selects all rows from the table

        Args:
            connectionArgs (dict): Connection arguments in key-value-pairs
            table (str): Name of the table to read from
        """
        pass
    # Method to insert a row to a given table
    def insertRowToTable(self, connectionArgs, sqlClause):
        """Inserts a row to table accordings to a SQL clause

        Args:
            connectionArgs (dict): Connection arguments in key-value-pairs
            sqlClause (str): Insert clause
        """
        pass

    # Method to update a table
    def updateTable(self, connectionArgs, table, column, whereClause):
        """Updates a table

        Args:
            connectionArgs (_type_): Connection arguments in key-value-pairs
            table (str): Table name
            column (str): Column to be updated
            whereClause (str): WHERE SQL statement
        """
        pass
    
    # Method to delete a row from table
    def deleteFromTable(self, connectionArgs, table, whereClause):
        """Delete rows from a table using limiting SQL statement

        Args:
            connectionArgs (dict): Connection arguments in key-value-pairs
            table (str): Table name
            whereClause (str): WHERE SQL statement
        """
        pass