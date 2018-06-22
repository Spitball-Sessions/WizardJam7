import datetime, time, sqlite3, json,time, collections, os,DiaryF



class Planner():

    today = str(datetime.date.today())

    # What does user have coming up and when?
    @staticmethod
    def input_upcoming(player):
        planner_entry = collections.namedtuple("Sql_Entry","due_date,due_time,entry,tag,score")


        appointment_entry = input("What would you like to remember?\n")

        date_due = time.strptime(input("What day is that? (MM/DD/YYYY) "),"%m/%d/%Y")

        if len(str(date_due.tm_mon)) == 2 and len(str(date_due.tm_mday)) == 2:
            date_due = (str(date_due.tm_year) + "-" + str(date_due.tm_mon) + "-" + str(date_due.tm_mday))
        elif len(str(date_due.tm_mon))  == 1 and len(str(date_due.tm_mday)) == 2:
            date_due = (str(date_due.tm_year) + "-0" + str(date_due.tm_mon) + "-" + str(date_due.tm_mday))
        elif len(str(date_due.tm_mon))  == 2 and len(str(date_due.tm_mday)) == 1:
            date_due = (str(date_due.tm_year) + "-" + str(date_due.tm_mon) + "-0" + str(date_due.tm_mday))
        else:
            date_due = (str(date_due.tm_year) + "-0" + str(date_due.tm_mon) + "-0" + str(date_due.tm_mday))

        time_due = input("What time? (Optional) ")
        keyword_scoring = Planner.scoring_upcoming(appointment_entry)
        if time_due.isnumeric():
            sql_entry = planner_entry(date_due,time_due,appointment_entry,keyword_scoring[0],keyword_scoring[1])
        else:
            time_due = None
            sql_entry = planner_entry(date_due,time_due,appointment_entry,keyword_scoring[0],keyword_scoring[1])

        Planner.write_upcoming_sql(sql_entry,player)

    @staticmethod
    def scoring_upcoming(text):
        while True:
            with open('Points.List', encoding='utf-8') as score_table:
                points = json.loads(score_table.read())

            for x in range(2): # anything else I do causes excessive looping here. Doesn't seem to cause issues in the other function.
                for k in points.keys():
                    if k in text.lower():
                        tag_scoring = [k, points.get(k)]
                        return tag_scoring
                    elif x == 1:
                        return None,None
                    else:
                        continue

    def write_upcoming_sql(entry_tuple,player):
        planner_entry = sqlite3.connect("Characters.db")
        planner_entry.execute("INSERT INTO PLANNER(PLAYER_ID,DUE_DATE,DUE_TIME,TASK, TAGS, POINTS, STATUS)VALUES(?,?,?,?,?,?,?)",
                              (player.first+player.last, entry_tuple.due_date, entry_tuple.due_time, entry_tuple.entry, entry_tuple.tag, entry_tuple.score, True))
        print("Updated list...")
        planner_entry.commit()
        print("Saved list...")
        planner_entry.close()
        print("List finished.")

    def mark_as_complete(player):
        planner_db = sqlite3.connect("Characters.db")
        planner = planner_db.cursor()
        today = datetime.date.today()
        while True:
            tasks_cursor = planner.execute("SELECT TASK, ROWID FROM PLANNER WHERE DUE_DATE = ? AND PLAYER_ID = ? AND STATUS = 1",(today, player.first + player.last))
            tasks = tasks_cursor.fetchall()
            if tasks is None or tasks == []:
                planner.execute("DELETE FROM PLANNER WHERE STATUS = 0")
                planner_db.commit()
                planner.close()
                return
            else:
                for i in tasks:
                    print("{}.) {}".format(i[1],i[0]))
            print("Which would you like to mark as complete? (By number.)")
            complete_task = input().lower().strip()
            if complete_task == "no" or complete_task == "none" or complete_task == "":
                planner.execute("DELETE FROM PLANNER WHERE STATUS = 0")
                planner_db.commit()
                planner.close()
                print("Completed is deleted...")
                return
            else:
                points_list = []
                points_cursor = planner.execute("SELECT TAGS, TASK, POINTS, PLAYER_ID FROM PLANNER WHERE ROWID = ?",(complete_task))
                points = points_cursor.fetchall()
                for i in points:
                    points_list.append(i)
                if points_list[0][2] != None:
                    pointser = points_list[0][2]*2
                    planner_db.commit()
                    planner.execute("UPDATE PLANNER SET STATUS = 0 WHERE ROWID = ?", (complete_task))
                    planner.execute("INSERT INTO DIARY (PLAYER_ID,RECORD_DATE,TAG,DIARY_ENTRY,SCORE)VALUES(?,?,?,?,?)",
                                           (points_list[0][3],today,points_list[0][0],points_list[0][1],pointser))
                    planner_db.commit()

                else:
                    with open('Points.List', encoding='utf-8') as score_table:
                        points_db = json.loads(score_table.read())
                    while True:
                        for x in range(len(points_db.keys())):
                            for k in points_db.keys():
                                if k in points[0]:
                                    diary_data = points.get(k)
                                    diary_data = diary_data*2

                                    planner.execute("UPDATE PLANNER SET STATUS = 0 WHERE ROWID = ?", (complete_task))
                                    planner.execute(
                                        "INSERT INTO DIARY (PLAYER_ID,RECORD_DATE,TAG,DIARY_ENTRY,SCORE)VALUES(?,?,?,?,?)",
                                        (points_list[0][3],today,points_list[0][0],points_list[0][1],diary_data))
                                    planner_db.commit()
                                    print("Planner updated...")
                                elif x == len(points_db.keys()):
                                    break
                                else:
                                    continue

                        print("Which tag would you like to assign to this entry?")
                        print("Tags are: {}".format(", ".join(points_db.keys())).title())
                        tag = input().lower()
                        if tag in points_db.keys():
                            diary_data = points_db.get(tag)
                            diary_data = diary_data * 2
                            print(points_list[0][3],today,tag,points_list[0][1], diary_data)
                            planner.execute("UPDATE PLANNER SET STATUS = 0 WHERE ROWID = ?", (complete_task))
                            planner_db.execute(
                                "INSERT INTO DIARY (PLAYER_ID,RECORD_DATE,TAG,DIARY_ENTRY,SCORE)VALUES(?,?,?,?,?)",
                                (points_list[0][3],today,tag,points_list[0][1], diary_data))
                            planner_db.commit()
                            break

                        else:
                            diary_data2 = DiaryF.Diary.scoring_values(tag, points_list[0][1])
                            diary_data = diary_data2[1] * 2
                            planner.execute("UPDATE PLANNER SET STATUS = 0 WHERE ROWID = ?", (complete_task))
                            planner_db.execute(
                                "INSERT INTO DIARY (PLAYER_ID,RECORD_DATE,TAG,DIARY_ENTRY,SCORE)VALUES(?,?,?,?,?)",
                                (points_list[0][3],today,tag,points_list[0][1], diary_data))
                            planner_db.commit()
                            break

                        break

    def check_commitments(player):
        week = []
        planner = sqlite3.connect("Characters.db")
        today = datetime.date.today()
        tasks = planner.execute("SELECT TASK, DUE_TIME FROM PLANNER WHERE DUE_DATE = ? AND PLAYER_ID = ? AND STATUS = 1",(today,player.first+player.last))
        print("Today you're supposed to:")
        for i in tasks:
            if i[1] != None:
                print("{} at {}".format(i[0],i[1]))
            else:
                print(i[0])

        for i in range(1,8):
            week.append(str(today + datetime.timedelta(days = i)))

        print("\nAlso, this week, you have to:")
        for i in range(len(week)):
            week_tasks = planner.execute("SELECT TASK, DUE_TIME, DUE_DATE FROM PLANNER WHERE due_date = ? AND PLAYER_ID = ? AND STATUS = 1",(str(week[i]), player.first + player.last))
            for i in week_tasks:
                if i[1] != None:
                    print("{} on {} at {}".format(i[0], i[2], i[1]))
                else:
                    print("{} on {}".format(i[0],i[2]))

        while True:
            lookup_date = input("\n\nIs there any other day you'd like information about? (MM/DD/YYYY or No)\n").lower().strip()

            if lookup_date.isalpha():
                finish = input("Would you like to mark a task as complete? ")
                if finish == "yes" or finish == "y":
                    Planner.mark_as_complete(player)
                    return
                else:
                    planner.close()
                    return

            else:

                lookup = time.strptime(lookup_date, "%m/%d/%Y")

                if len(str(lookup.tm_mon)) == 2 and len(str(lookup.tm_mday)) == 2:
                    lookup = (str(lookup.tm_year) + "-" + str(lookup.tm_mon) + "-" + str(lookup.tm_mday))
                elif len(str(lookup.tm_mon)) == 1 and len(str(lookup.tm_mday)) == 2:
                    lookup = (str(lookup.tm_year) + "-0" + str(lookup.tm_mon) + "-" + str(lookup.tm_mday))
                elif len(str(lookup.tm_mon)) == 2 and len(str(lookup.tm_mday)) == 1:
                    lookup = (str(lookup.tm_year) + "-" + str(lookup.tm_mon) + "-0" + str(lookup.tm_mday))
                else:
                    lookup = (str(lookup.tm_year) + "-0" + str(lookup.tm_mon) + "-0" + str(lookup.tm_mday))

                lookup_tasks = planner.execute("SELECT TASK, DUE_TIME FROM PLANNER WHERE DUE_DATE = ? AND PLAYER_ID = ? AND STATUS = 1",(lookup,player.first+player.last))
                print("On {}, you have to:".format(lookup_date))
                for i in lookup_tasks:
                    if i[1] != None:
                        print("{} at {}".format(i[0], i[1]))
                    else:
                        print(i[0])

    def select_planner_function(player):
        Zzz = os.system('cls' if os.name == 'nt' else 'clear')
        print("In this mode, you can add upcoming dates or check existing info\nand if complete "
              "add them to your diary.")
        while True:
            print("Would you like to 1) Enter upcoming or 2) Get tasks?")
            option = input().strip().lower()
            Zzz = os.system('cls' if os.name == 'nt' else 'clear')
            while option:
                if option in ("enter", "upcoming", "1"):
                    Planner.input_upcoming(player)
                    break
                elif option in ("tasks", "2", "get"):
                    Planner.check_commitments(player)
                    break
                elif option == "quit":
                    quit()
                elif option == "no" or option == "n":
                    return
                else:
                    print("Unrecognized input.")
                    break

            exit_option = input("Would you like to continue with Planner functions? ").lower()
            if exit_option == "y" or exit_option == "yes":
                continue
            else:
                return

    def starting_todo(player):
        planner_db = sqlite3.connect("Characters.db")
        planner = planner_db.cursor()
        today = datetime.date.today()
        tasks = planner.execute("SELECT TASK, DUE_TIME FROM PLANNER WHERE DUE_DATE = ? AND PLAYER_ID = ? AND STATUS = 1",
                                (today, player.first + player.last))
        tasks1 = tasks.fetchall()
        if tasks1 != []:
            print("\nToday you're supposed to:")
            for i in tasks:
                if i[1] != None:
                    print("{} at {}".format(i[0], i[1]))
                else:
                    print(i[0].capitalize())
        else:
            pass

        planner.close()
