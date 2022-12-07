import os, sqlite3, csv

conn = sqlite3.connect("database.db")
c = conn.cursor()

# Creating tables

create_tables_commands = [
    """
        CREATE TABLE IF NOT EXISTS abbreviations (
            Type TEXT,
            Code TEXT,
            FullName TEXT,
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS AwardsCoaches (
            CoachId TEXT,
            Award TEXT,
            Year INTEGER,
            LgId TEXT,
            Note TEXT,
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS AwardsPlayers (
            PlayerId TEXT,
            Award TEXT,
            Year INTEGER,
            LgId TEXT,
            Note TEXT,
            Pos TEXT,
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS Coaches (
            CoachId TEXT,
            Year INTEGER,
            TmId TEXT,
            LgId TEXT,
            Stint INTEGER,
            G INTEGER,
            W INTEGER,
            L INTEGER,
            T INTEGER,
            postG INTEGER,
            postW INTEGER,
            postL INTEGER,
            postT INTEGER,
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS CombinedShutouts (
            Year INTEGER,
            Month INTEGER,
            Day INTEGER,
            TmId TEXT,
            OppId TEXT,
            RP TEXT,
            IDgoalie1 TEXT,
            IDgoalie2 TEXT,
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS Goalies (
    """,
    """
        CREATE TABLE IF NOT EXISTS GoaliesSC (
    """,
    """
        CREATE TABLE IF NOT EXISTS GoaliesShootout (
    """,
    """
        CREATE TABLE IF NOT EXISTS HOF (
    """,
    """
        CREATE TABLE IF NOT EXISTS Master (
    """,
    """
        CREATE TABLE IF NOT EXISTS Scoring (
    """,
    """
        CREATE TABLE IF NOT EXISTS ScoringSC (
    """,
    """
        CREATE TABLE IF NOT EXISTS ScoringShootout (
    """,
    """
        CREATE TABLE IF NOT EXISTS SeriesPost (
    """,
    """
        CREATE TABLE IF NOT EXISTS Teams (
            Year INTEGER,
            LgId TEXT,
            TmId TEXT,
            FranchId TEXT,
            DivId TEXT,
            Rank INTEGER,
            G INTEGER,
            W INTEGER,
            L INTEGER,
            T INTEGER,
            Pts INTEGER,
            Name TEXT,
            PIM INTEGER,
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS TeamsHalf (
    """,
    """
        CREATE TABLE IF NOT EXISTS TeamSplits (
    """,
    """
        CREATE TABLE IF NOT EXISTS TeamsPost (
    """,
    """
        CREATE TABLE IF NOT EXISTS TeamsSC (
    """,
    """
        CREATE TABLE IF NOT EXISTS TeamVsTeam (
    """,
]
