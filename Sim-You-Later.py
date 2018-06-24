import collections, time, os, DiaryF, sqlite3, datetime, PlannerF, Moodlets, textwrap
from player_creation import create_player_Sim, sql_player_add

from Classes import Player, Sim

Sims_Info = collections.namedtuple("Sim_Info",
                                   "first_name, last_name, age, gender, clothing")


def header():
    print("*"*40)
    print("Sim-You-Lation".center(26).center(40,"*"))
    print("*"*40)
    print("Inspired by Three Moves Ahead ep 16\n\n\n".center(40))


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

    list_create.execute("""CREATE TABLE IF NOT EXISTS MOODLETS
    (ITEM         TEXT       NOT NULL,
    TAGS          TEXT       NOT NULL,
    POINTS        INTEGER    NOT NULL);""")

    # print("Tables created without error.")


def char_gen(new_sim):
    '''
    Gets all the information for creating or loading a character.
    :param new_sim: Whether the player is making a new character.
    :return: Returns the player's info.
    '''
    if new_sim == "y" or new_sim == "yes":
        player_character = create_player_Sim(new_sim)
        sql_player_add(player_character)  # adds character to the DB
        print("Welcome, {}".format(player_character.first))
        return player_character
    else:
        player_character = create_player_Sim(new_sim)
        '''This passes to the player creation to avoid multiple 
         sub-modules running in main.  There's probably a cleaner way to do this.'''
        print("Welcome back, {}".format(player_character.first))
        PlannerF.Planner.starting_todo(player_character)
        return player_character


def core_loop(new_sim,player_character):
    '''
    This is where the main game loop occurs.
    if the player is new, it gives them some help, then it sends them to either Diary or Planner functions.
    :param new_sim: whether the character is new - tips only appear once.
    :param player_character: all the player info.
    :return: nothing - can only quit from here.
    '''
    while True:
        tags, moods_c = Moodlets.getting_mood_ideas(new_sim)
        if new_sim == "y" or new_sim == "yes":
            print("\n".join(textwrap.wrap("This is the main screen.  From here, you have 2 choices.  You can make or view diary entries, or "
                  "you can go to your planner/todo list.\n", width=70)))
            time.sleep(.5)
            print("\n".join(textwrap.wrap("The diary is where you will record the events of your day.  Based on how well you do each day, you will "
                  "get scored, and you can win and lose.  You can also view entries from previous days.\n",width=70)))
            time.sleep(.5)
            print("\n".join(textwrap.wrap("The planner is where you can record upcoming events that you want to remember, and check them off once complete.",width=70)))
            time.sleep(2.5)
            print("\n")
        choice = input("\nDo you want to 1) Make / View diary entries or 2) View upcoming plans/tasks? ").lower()
        if choice in ("1", "one","make", "view", "entry", "diary"):
            time.sleep(.2)
            DiaryF.Diary.diary_usage(player_character, tags, moods_c)
            print("Exiting diary functions.")

        elif choice in ("2", "two" "tasks", "upcoming", "plans"):
            time.sleep(.2)
            PlannerF.Planner.select_planner_function(player_character)

        elif choice.isnumeric() is False:
            quit()

        else:
            continue

if __name__ == '__main__':

    def main():
        header()
        sql_create_db()
        new_sim = input("Would you like to Create a New Sim? (Y)es or (N)o? ").lower().strip()
        player_character = char_gen(new_sim)
        core_loop(new_sim,player_character)

    main()