import datetime, time, os, json, sqlite3

class Diary:

    def diary_entry_sql(player, diary_database,tags, moods_c):
        times_appended = 0
        today = datetime.date.today()

        while True:

            if times_appended > 0:
                print("What else would you like to record?")
            else:
                print("All right, {}".format(player.first.capitalize()))
                print("What would you like to record today??")

            entry = input()
            if entry in ("no", "none", "nothing", "n"):
                if moods_c != None:
                    x = input("Did you complete your bonus objective? ").lower()
                    if x == "yes" or x == "y":
                        diary_database.execute(
                            "INSERT INTO DIARY (PLAYER_ID,RECORD_DATE,TAG,DIARY_ENTRY,SCORE)VALUES(?,?,?,?,?)",
                            (player.first + player.last, today, moods_c[1], moods_c[0], int(moods_c[2])*3))
                break
            else:
                diary_tags = Diary.parse_diary_entry_for_tags(entry, tags)
                diary_database.execute("INSERT INTO DIARY (PLAYER_ID,RECORD_DATE,TAG,DIARY_ENTRY,SCORE)VALUES(?,?,?,?,?)",
                                       (player.first+player.last, today, diary_tags[0], entry, diary_tags[1]))
                times_appended += 1

        diary_database.commit()
        print("Diary updated...")
        return

    """def diary_entry(player):
        times_appended = 0
        daily_score = [0]
        while True:

            if times_appended > 0:
                print("What else would you like to record?")
            else:
                print("What would you like to record today??")

            entry = input()
            if entry in ("no", "none", "nothing", "n"):
                break
            else:
                diary_tags = Diary.parse_diary_entry_for_tags(entry,tags, moods_c)
                daily_score.append(diary_tags[1])
                diary_entry = (diary_tags[0] + ": " + entry + " - " + str(diary_tags[1]))
                with open(player.first + "'s.diary", "a") as diary:
                    diary.writelines(diary_entry + "\n")
                times_appended += 1
        with open(player.first + "'s.diary", "a") as diary:
            diary.writelines(
                "\nPlayer score for today:" + "\n" + str(sum(daily_score)) + "\n\n" + "".center(20, "-") + "\n\n")
        return daily_score"""

    def scoring_values(tag_word, points_dictionary):
        diary_scoring_values = {"very bad": -40, "v. bad": -40, "vb": -40, "v b": -40, "very": -40, "1": -40, "2": -25,
                                "3": -10, "4": 10,
                                "bad": -25, "b": -25, "miserable": -25, "meh": -10, "boring": -10, "5": 25, "6": 40,
                                "ok": 10, "fine": 10, "all right": 10, "alright": 10, "good": 25, "fun": 25,
                                "great": 40, "excellent": 40,
                                "best": 40}

        score = input("How would you describe this action?  "
                      "1)Very bad?  2)Bad?  3)Boring? 4)Fine? 5)Good? or 6)Great? ").lower()
        if score in diary_scoring_values.keys():
            score = diary_scoring_values.get(score)
            points_dictionary.update({tag_word: score})
            print("Excellent, I will add \"{}\" with a score of {}".format(tag_word.title(), str(score)))

        with open("Points.List", "w") as score_table:
            json.dump(points_dictionary, score_table)
        diary_data = [tag_word, score]
        return diary_data

    def parse_diary_entry_for_tags(entry, tags):
        while True:
            with open('Points.List', encoding='utf-8') as score_table:
                points = json.loads(score_table.read())
                break

        while True:
            for x in range(len(points.keys())):
                for k in points.keys():
                    if k in entry.lower():
                        print("Keyword \"{}\", worth {} points is in that entry.".format(k, points.get(k)
                                                                            ) + "  Would you prefer to designate a tag? ")
                        proceed = input().lower().strip()
                        if proceed in ("no", "n"):
                            diary_data = [k, points.get(k)]
                            if diary_data[0] in tags:
                                diary_data = [diary_data[0],int(diary_data[1])*2]
                            return diary_data
                        else:
                            print("Which tag would you like to assign to this entry? ")
                            tag = input().lower()
                            if tag in points.keys():
                                diary_data = [tag, points.get(tag)]
                                if diary_data[0] in tags:
                                    diary_data = [diary_data[0], int(diary_data[1]) * 2]
                                return diary_data
                            else:
                                diary_data = Diary.scoring_values(tag, points)
                                return diary_data

                    elif x == len(points.keys()):
                        break
                    else:
                        continue

            check = input("Would you like to mark a keyword, or assign a generic tag? ").lower().strip()
            if check in ("keyword", "key", "yes", "1", "first", "kw"):
                key = input("What would you like to designate as a keyword?\n").strip().lower()
                diary_data = Diary.scoring_values(key, points)
                return diary_data
            else:
                print("Which tag would you like to assign to this entry?")
                print("Tags are: {}".format(", ".join(points.keys())).title())
                tag = input().lower()
                if tag in points.keys():
                    diary_data = [tag, points.get(tag)]
                    if diary_data[0] in tags:
                        diary_data = [diary_data[0], int(diary_data[1]) * 2]
                    return diary_data
                else:
                    diary_data = Diary.scoring_values(tag, points)
                    return diary_data

    def diary_update(player, tags, moods_c):
        today = datetime.date.today()
        diary_database = sqlite3.connect("Characters.db")
        diary = diary_database.cursor()
        Diary.diary_entry_sql(player,diary_database,tags, moods_c)
        score = diary.execute("SELECT SUM(SCORE) FROM DIARY WHERE RECORD_DATE = ?",(today,))
        for i in score:
            scorer = i[0]
            print("Your score for today is " + str(i).lstrip("(").rstrip(",)"))
        tries = 0
        while True:
            print("Are you satisfied with your score?")
            satis = input()
            if satis == "yes" or satis == "y":
                print("That's excellent!")
                time.sleep(.75)
                Zzz = os.system('cls' if os.name == 'nt' else 'clear')
                print("A Winner".center(20).center(30,"*"))
                time.sleep(1)
                print("You Are!".center(20).center(30,"*"))
                time.sleep(2.4)
                diary_database.close()
                Zzz = os.system('cls' if os.name == 'nt' else 'clear')
                print("But tomorrow is a chance for you to get an even better score!")
                time.sleep(3)
                quit()
            else:
                if tries == 0:
                    print("Oh.  I'm sorry to hear that.  Let me give you 50 bonus points.")
                    time.sleep(1.25)
                    scorer = scorer + 50
                    Zzz = os.system('cls' if os.name == 'nt' else 'clear')
                    print("Now your score is " + str(scorer))
                    diary_database.execute(
                        "INSERT INTO DIARY (PLAYER_ID,RECORD_DATE,TAG,DIARY_ENTRY,SCORE)VALUES(?,?,?,?,?)",
                        (player.first + player.last, today, "bonus", "I had a bad day today", 50))
                    diary_database.commit()
                    tries = 1
                    continue
                else:
                    print("I'm sorry to hear that.")
                    time.sleep(.6)
                    Zzz = os.system('cls' if os.name == 'nt' else 'clear')
                    print("Well, then, it looks like today you've lost.")
                    time.sleep(1.75)
                    Zzz = os.system('cls' if os.name == 'nt' else 'clear')
                    print("But tomorrow is another day!")
                    time.sleep(2)
                    diary_database.close()
                    return

    def diary_retrieval(player_character):
        score = []
        diary_database = sqlite3.connect("Characters.db")
        days_elapsed = int(input("How many days of entries would you like? "))
        tags = input("Show with tags? (Y/N) ").lower().strip()
        Zzz = os.system('cls' if os.name == 'nt' else 'clear')
        for i in range(days_elapsed):
            dateX = datetime.date.today() - datetime.timedelta(days=i)
            entries = diary_database.execute(
                "SELECT TAG, DIARY_ENTRY, SCORE FROM DIARY WHERE RECORD_DATE = ? AND PLAYER_ID = ?",
                (dateX, player_character.first + player_character.last))
            print(str(dateX.month) + "/" + str(dateX.day) + "/" + str(dateX.year) + ": ")
            if tags == "yes" or tags == "y":
                for i in entries:
                    print(i[0] + ": " + i[1].capitalize())
                    score.append(i[2])
            else:
                for i in entries:
                    print(i[1].capitalize())
                    score.append(i[2])
            print("Score:" + str(sum(score)))
            score.clear()
            print("\n")
        diary_database.close()
        return

    def diary_usage(player_character,tags, moods_c):
        Zzz = os.system('cls' if os.name == 'nt' else 'clear')
        print("In this mode, you can write about the things you did today, "
              "read entries from previous days, and get your scores.\n")
        while True:
            print("Would you like to 1) Enter diary info, or 2) Get previous log? ")
            log_option = input()
            while log_option:
                if log_option in ("enter","diary", "enter diary info","1"):
                    time.sleep(.2)
                    Zzz = os.system('cls' if os.name == 'nt' else 'clear')
                    Diary.diary_update(player_character,tags, moods_c)
                    break
                elif log_option in ("log","previous","2", "get previous log"):
                    Diary.diary_retrieval(player_character)
                    break
                elif log_option == "quit":
                    quit()
                elif log_option == "no" or log_option == "n":
                    return
                else:
                    print("Unrecognized input.")
                    break


            exit_option = input("Would you like to continue with Diary functions? ").lower()
            if exit_option == "y" or exit_option == "yes":
                continue
            elif exit_option == "quit":
                quit()
            else:
                return

 # obsolete
                '''
                    if os.path.isfile(player_character.first + "'s.diary") == True:
                        total = int(input("How many logs would you like? "))
                        with open(player_character.first + "'s.diary", "r") as diary:
                            diary_log = diary.read()
                            diary_log = diary_log.split("--------------------\n\n")
                            diary_log_count = int(len(diary_log) - 1)

                        if total > diary_log_count:
                            diary_recall = diary_log[0:len(diary_log)-1]
                            for i in reversed(diary_recall):
                                print(i)
                        else:
                            Z = (diary_log_count + 2) - (2 + total)
                            diary_recall = diary_log[Z:len(diary_log)-1]
                            for i in reversed(diary_recall):
                                print(i)
                        break
                    else:
                        print("There is no diary to read from.  Please make one.")
                        log_option = "1"
                        break
                else:
                    log_option = input("Please try that again. ")
                    continue'''
