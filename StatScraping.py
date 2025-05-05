#Author: Chase Rodie
#Date: 04/21/24
#Purpose: Using a python3 script to create an NBA Database for users to view data and suggest feedback

import requests
import pandas as pd
import openpyxl
from bs4 import BeautifulSoup
import csv
import psycopg2

# Connects to database
def connect_to_database():
    db_params = {
        "host": "localhost",
        "database": "Final Project",
        "user": "chaserodie",
        "password": "your_database_password", 
        "port": "5432"
    }
    try:
        connection = psycopg2.connect(**db_params)
        return connection
    except psycopg2.Error as error:
        print(f"Error connecting to the database: {error}")
        return None

#Uses Data Scraping/API Call to create the following table in an Excel File:
#Season = 23-24, Season Type = Regular Season, Per Mode = Per Game, Stat Category = PTS
#*****API Call no longer working the JSON file is now restricted******
def regularStats():
    response=requests.get('https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=PerGame&Scope=S&Season=2023-24&SeasonType=Regular%20Season&StatCategory=PTS')

    if response.status_code==200:
        data=response.json()
        headers=data['resultSet']['headers']
        rows=data['resultSet']['rowSet']

        df=pd.DataFrame(rows, columns=headers)

        df.to_excel("NBA_RegularSeasonStats_23-24.xlsx", index=False)
        print("Excel file created")
    else:
        print("Failed to fetch stats from source file")

#Uses Data Scraping/API Call to create the following table in an Excel File:
#Season = 22-23, Season Type = Playoff Season, Per Mode = Per Game, Stat Category = PTS
#*****API Call no longer working the JSON file is now restricted******
def playoffStats():
    response=requests.get('https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=PerGame&Scope=S&Season=2022-23&SeasonType=Playoffs&StatCategory=PTS')

    if response.status_code==200:
        data=response.json()
        headers=data['resultSet']['headers']
        rows=data['resultSet']['rowSet']

        df=pd.DataFrame(rows, columns=headers)

        df.to_excel("NBA_PlayoffStats_22-23.xlsx", index=False)

        print("Excel file created")
    else:
        print("Failed to fetch stats from source file")

#Adds Users to User Info Table
def loginFunction(connection):
    try:
        cursor = connection.cursor()
        userid = input("\nPlease enter your username: ").strip()
        cursor.execute('SELECT userid FROM "User Info" WHERE userid = %s', (userid,))
        result = cursor.fetchone()
        if result:
            return result[0]  # Return the user ID
        else:
            print("\nInvalid username. Please sign up to make an account or try again.")
            return None  # Invalid username
    except psycopg2.Error as error:
        print(f"Error logging in: {error}")
        return None  # Login failed
    finally:
        if cursor:
            cursor.close()

#signs users up
def signupFunction(connection):
    cursor = None
    try:
        cursor = connection.cursor()
        userid = input("Welcome to the NBA database please create a username to proceed: ").strip()
        
        # Check if userid already exists
        cursor.execute('SELECT userid FROM "User Info" WHERE userid = %s', (userid,))
        existing_user = cursor.fetchone()
        if existing_user:
            print("Username already exists. Please choose a different username.")
            return False 
        
        cursor.execute('INSERT INTO "User Info" (userid) VALUES (%s)', (userid,))
        connection.commit()
        print("Signup Successful!\n")
        return userid  # Return the user ID
    except psycopg2.Error as error:
        print(f"Error signing up: {error}")
        return None  # Signup failed
    finally:
        if cursor:
            cursor.close()

#displays player info from 23-24 regular season that user requests
def regularStatDisplay(connection):
    try:
        while True:
            cursor = connection.cursor()
            userid = input("Which player's stats would you like to see from the 2023-24 Regular Season?: ").strip()
            cursor.execute('SELECT "RANK", "PLAYER", "TEAM", "PTS", "REB", "AST" FROM "Regular Season Stats 23-24" WHERE "PLAYER" ILIKE %s', (userid,))
        
            rows = cursor.fetchall()  # Fetch all rows returned by the query
            if rows:
                print("Rank\tPlayer\t\tTeam\tPTS\tREB\tAST")
                for row in rows:
                    print("\t".join(map(str, row)))  # Print each row
                    continue_choice = input("Do you want to see another player's stats? (yes/no): ").strip().lower()
                if continue_choice == 'yes':
                    continue
                else:
                    return True
            else:
                print("Player could not be found in the database.")
                return False
    except psycopg2.Error as error:
        print(f"Error displaying regular season stats: {error}")
        return False
    finally:
        if cursor:
            cursor.close()

#displays player info from 22-23 playoff season that user requests
def playoffStatDisplay(connection):
    try:
        while True:
            cursor = connection.cursor()
            userid = input("Which player's stats would you like to see from the 2022-23 Post Season? (Enter 'exit' to return to main menu): ").strip()
            if userid.lower() == 'exit':
                return False
            
            cursor.execute('SELECT "RANK", "PLAYER", "TEAM", "PTS", "REB", "AST" FROM "Playoff Season Stats 22-23" WHERE "PLAYER" ILIKE %s', (userid,))
        
            rows = cursor.fetchall() 
            if rows:
                print("Rank\tPlayer\t\tTeam\tPTS\tREB\tAST")
                for row in rows:
                    print("\t".join(map(str, row))) 
                continue_choice = input("Do you want to see another player's stats? (yes/no): ").strip().lower()
                if continue_choice == 'yes':
                    continue
                else:
                    return True
            else:
                print("Player could not be found in the database.")
                return False
    except psycopg2.Error as error:
        print(f"Error displaying playoff stats: {error}")
        return False
    finally:
        if cursor:
            cursor.close()

#displays teams info from current season that user requests
def teamStatDisplay(connection):
    try:
        while True:
            cursor = connection.cursor()
            userid = input("\nWhich team's stats would you like to see? (Enter 'exit' to return to the main menu): ").strip()
            if userid.lower() == 'exit':
                return False
            
            cursor.execute('SELECT "Rk", "Team", "Overall", "Home", "Road" FROM "Team Stats" WHERE "Team" ILIKE %s', (userid,))
        
            rows = cursor.fetchall() 
            if rows:
                print("{:<6} {:<20} {:<8} {:<8} {:<8}".format("Rank", "Team", "Overall", "Home", "Road"))
                for row in rows:
                    print("{:<6} {:<20} {:<8} {:<8} {:<8}".format(*row))
                continue_choice = input("Do you want to see another team's stats? (yes/no): ").strip().lower()
                if continue_choice == 'yes':
                    continue
                else:
                    return True
            else:
                print("Team could not be found in the database.")
                return False
    except psycopg2.Error as error:
        print(f"Error displaying team stats: {error}")
        return False
    finally:
        if cursor:
            cursor.close()

#displays matchup info from teams who played on a a certain date
def matchupStatDisplay(connection):
    try:
        while True:
            cursor = connection.cursor()
            userid = input("\nWhich matchups from a day would you like to see? (ex: Wed Apr 24 2024) (Enter 'exit' to return to main menu): ").strip()
            if userid.lower() == 'exit':
                return False
            
            cursor.execute('SELECT "Date", "Visitor/Neutral", "Home/Neutral", "Arena", "Winner" FROM "Matchup Schedule" WHERE "Date" ILIKE %s', (userid,))
        
            rows = cursor.fetchall() 
            if rows:
                print("{:<20}{:<25}{:<25}{:<30}{}".format("Date", "Visitor", "Home", "Arena", "Winner"))
                for row in rows:
                    date, visitor, home, arena, winner = row
                    print("{:<20}{:<25}{:<25}{:<30}{}".format(date, visitor, home, arena, winner)) 
                continue_choice = input("Do you want to see info from another matchup? (yes/no): ").strip().lower()
                if continue_choice == 'yes':
                    continue
                else:
                    return True
            else:
                print("Date where games were played could not be found in the database.")
                return False
    except psycopg2.Error as error:
        print(f"Error displaying matchup info: {error}")
        return False
    finally:
        if cursor:
            cursor.close()

#gives user option to add feeback
def addFeedback(connection, userid):
    cursor = None
    try:
        cursor = connection.cursor()
        while True:
            feedback = input("What feedback would you like to give the database as far as future info you want to see?: ").strip()
            cursor.execute('INSERT INTO "User Info" (userid, feedback) VALUES (%s, %s)', (userid, feedback,))
            connection.commit()
            print("Feedback added successfully!")
            return True  
    except psycopg2.Error as error:
        print(f"Error adding feedback: {error}")
        return False 
    finally:
        if cursor:
            cursor.close()

#main function for logic and user menu/function calls
def main():
    connection = connect_to_database()
    if not connection:
        return
    try:
        while True:
            print("----------------------------")
            print("Welcome to the NBA Database!\n")
            print("Please login to view the database.\n")
            print("1. Login")
            print("2. Sign up")
            print("3. Exit\n")
            userchoice = input("Please select a choice: ")

            if userchoice == "1":
                userid = loginFunction(connection)
                if userid:
                    while True:
                        print("\n1. Regular Season Stats")
                        print("2. Playoff Stats")
                        print("3. Team Stats")
                        print("4. Matchup Stats")
                        print("5. Add Feedback")
                        print("6. Logout\n")
                        stats_choice = input("Please select the stats or action you want to perform: ")
                        if stats_choice == "1":
                            regularStatDisplay(connection)
                        elif stats_choice == "2":
                            playoffStatDisplay(connection)
                        elif stats_choice == "3":
                            teamStatDisplay(connection)
                        elif stats_choice == "4":
                            matchupStatDisplay(connection)
                        elif stats_choice == "5":
                            addFeedback(connection, userid)
                        elif stats_choice == "6":
                            # logs out (ends program)
                            break
                        else:
                            print("\nInvalid Choice. Please try again.")

            elif userchoice == "2":
                userid = signupFunction(connection)
                if userid:
                    while True:
                        print("\n1. Regular Season Stats")
                        print("2. Playoff Stats")
                        print("3. Team Stats")
                        print("4. Matchup Stats")
                        print("5. Add Feedback")
                        print("6. Logout\n")
                        stats_choice = input("Please select the stats or action you want to perform: ")
                        if stats_choice == "1":
                            regularStatDisplay(connection)
                        elif stats_choice == "2":
                            playoffStatDisplay(connection)
                        elif stats_choice == "3":
                            teamStatDisplay(connection)
                        elif stats_choice == "4":
                            matchupStatDisplay(connection)
                        elif stats_choice == "5":
                            addFeedback(connection, userid)
                        elif stats_choice == "6":
                            # logs out (ends program)
                            break
                        else:
                            print("\nInvalid Choice. Please try again.")
            elif userchoice == "3":
                break

            else:
                print("\nInvalid Choice. Please try again.")
    finally:
        connection.close()



if __name__ == "__main__":
    main()
