import collections, time, os, DiaryF, sqlite3, datetime, PlannerF
from player_creation import create_player_Sim, sql_player_add
from Classes import Player, Sim

Sims_Info = collections.namedtuple("Sim_Info",
                                   "first_name, last_name, age, gender, clothing")


def header():
    print("*"*40)
    print("Human Simulatiizer".center(26).center(40,"*"))
    print("*"*40)
    print("Inspired by Three Moves Ahead ep 16\n\n\n".center(40))


    # Moodlets:
    # Isolate some things to suggest the user does.

    # Propose 4 random suggestions.

    # If the user does one, give user bonus points.

    # Add to journal

def sql_create_db():
    list_create = sqlite3.connect("Characters.db")

    list_create.execute("""CREATE TABLE IF NOT EXISTS SIMS
    (ID INT    PRIMARY KEY    NOT NULL,
    FIRST_NAME        TEXT    NOT NULL,
    LAST_NAME         TEXT    NOT NULL,
    AGE               INTEGER NOT NULL,
    GENDER            TEXT    NOT NULL,
    CAREER            TEXT    NOT NULL,
    CLOTHING          TEXT    NOT NULL,
    ASPIRATION        TEXT    NOT NULL);""")

    list_create.execute("""CREATE TABLE IF NOT EXISTS PLANNER
    (DUE_DATE     TEXT          NOT NULL,
    DUE_TIME      TEXT          NULL,
    PLAYER_ID     TEXT          NOT NULL,
    TAGS          TEXT          NULL,
    TASK          TEXT          NOT NULL,
    POINTS        INTEGER       NULL,
    STATUS        TEXT          NULL);""")

    list_create.execute("""CREATE TABLE IF NOT EXISTS DIARY
    (RECORD_DATE       TEXT     NOT NULL,
     PLAYER_ID         TEXT     NOT NULL,
     TAG               TEXT     NOT NULL,
     DIARY_ENTRY       TEXT     NOT NULL,
     SCORE             INT      NULL);""")

    # print("Tables created without error.")

if __name__ == '__main__':

    def main():
        header()
        sql_create_db()

        new__sim = input("Would you like to Create a New Sim? (Y)es or (N)o? ").lower()
        if new__sim == "y" or new__sim == "yes":
            player_character = create_player_Sim(new__sim)
            sql_player_add(player_character)
            print("Welcome, {}".format(player_character.first))
        else:
            player_character = create_player_Sim(new__sim)
            print("\nWelcome back, {}".format(player_character.first))
            PlannerF.Planner.starting_todo(player_character)

        while True:
            choice = input("\nDo you want to 1) Make / View diary entry or 2) View day planner? ").lower()
            if choice in ("1", "make", "view","entry","diary"):
                time.sleep(.2)

                DiaryF.Diary.diary_usage(player_character)
                print("Exiting diary functions.")
            elif choice in ("2","tasks","upcoming","planner"):
                time.sleep(.2)
                PlannerF.Planner.select_planner_function(player_character)

            elif choice.isnumeric() is False:
                quit()

            else:
                continue
    main()