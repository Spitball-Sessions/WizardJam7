import collections, time, ast, os, json, sqlite3, random
from Classes import Player


Sims_Info = collections.namedtuple("Sim_Info",
                                   "first_name, last_name, age, gender, career")

Player_Info = collections.namedtuple("Player_info",
                                     "first_name, last_name, age, gender, career, clothing, ambition")


career_options = ("Creative", "Scholarly", "Legal", "Trade", "Technological", "Caring", "Governmental", "Student")

ambition_options = ("Wealth", "Fame", "Family", "Popularity", "Success", "Creation", "Contentment")


def help_reader():

    with open('attributes.help', encoding='utf-8') as ad:
        ambitions_help= json.loads(ad.read())
        careers_help = ambitions_help[1]
        ambitions_help = ambitions_help[0]

    return ambitions_help,careers_help


def valid_input(text, outfit, career_choice, player_ambition):
    while True:
        if text.isalpha():
            while outfit:
                if text in ("casual", "formal", "night", "party", "swim"):
                    break
                else:
                    text = input("Sorry, that's not a valid choice. What outfit? ").lower().strip()
                    continue
            while career_choice:
                if text in career_options:
                    break
                else:
                    text = input("That's not a valid choice. Please enter that again. ").title().strip()
                    continue
            while player_ambition:
                if text in ambition_options:
                    break
                else:
                    text = input("That's not a valid choice. Please enter that again. ").title().strip()
            break

    return text


def create_Sim_Info_tuple(first, last, age, gender, career):
    sim_info = Sims_Info(first, last, age, gender, career)
    return sim_info


def get_player_ambitions(name):
    ambitions_help, careers_help = help_reader()
    print("All right, nice to meet you {}".format(name))
    time.sleep(1.25)
    Zzz = os.system('cls' if os.name == 'nt' else 'clear')
    print("Now we need to establish your Sims' goals and ambitions.")
    print("\nWhich of these career tracks does your Sim want to pursue? Or type \"info\" and track for details.")
    print(", ".join(career_options))
    while True:
        player_career = input().title().strip()
        if player_career[0:4] == "Info":
            if player_career[5:].strip()in career_options:
                print(careers_help.get(player_career[5:].strip()))
                print("Now, which track would you like?")
                continue
            else:
                print("Sorry, please request info about a valid track.")
                continue
        else:
            player_career = valid_input(player_career, False, True, False)
            break
    print("\nExcellent! Now, let's discuss your ambitions!")
    time.sleep(.8)
    print("\n" + ", ".join(ambition_options))
    print("Which of these would your Sim like to pursue?  Or type \"\info\" and ambition for details.")
    while True:
        player_ambition = input().title().strip()
        if player_ambition[0:4] == "Info":
            if player_ambition[5:].strip()in ambition_options:
                print(ambitions_help.get(player_ambition[5:].strip()))
                print("Now, which track would you like?")
                continue
            else:
                print("Sorry, please request info about a valid track.")
                continue
        else:
            player_ambition = valid_input(player_ambition, False, False, True)
            break
    return player_career, player_ambition


def get_player_info():
    print("Hello.")
    while True:
        name = input("What is your Sim's first and last name?\n").title()
        if name[0:].__contains__(" ") == True:   # True
            name = name.split(" ")
            break
        else:
            continue
    print("Nice to meet you, {}.".format(name[0]))
    time.sleep(.8)
    inp = input("Are you human, dancer, or robot? ").lower().strip()
    if inp == "robot":
        strig = ["01001001 00100000", "01101100 01101111", "01110110 01100101",
                  "00100000 01111001", "01101111 01110101", "00101100 00100000",
                  "01110010 01101111", "01100010 01101111", "01110100 00101110"]
        print("\n".join(strig))
    elif inp == "dancer":
        print("But the real question is...  are you Hunter or are you Killer?")
    while True:
        age = input("What is your Sim's age? ").strip()
        if age.isnumeric():
            break
        else:
            continue

    gender = input("And their gender? ").strip().lower()
    gender = valid_input(gender, False, False, False)
    clothing = input("Which outfit would you like your Sim to wear?  Casual, formal, night, party, or swim?\n").lower().rstrip()
    clothing = valid_input(clothing, True, False, False)
    time.sleep(.25)
    Zzz = os.system('cls' if os.name == 'nt' else 'clear')
    x ="Awesome, you're wearing your {}wear.  It's a text-based game though,so you're going to have to imagine how you look.".format(
        clothing)
    print(x)
    print("Probably either pretty attractive or pretty goofy.")
    time.sleep(4)
    player_career, player_ambition = get_player_ambitions(name[0])
    sims_info = create_Sim_Info_tuple(name[0], name[1], age, gender, player_career)

    player_info = (*sims_info,clothing,player_ambition)

#    with open("player_data","w+") as doc:
 #       doc.writelines("Player Info:\n" + ",".join(player_info))

    return player_info


def sql_player_add(pc):
    player_update = sqlite3.connect("Characters.db")

    player_update.execute("INSERT INTO SIMS(ID,FIRST_NAME,LAST_NAME,AGE,GENDER,CAREER,CLOTHING,ASPIRATION) VALUES(?,?,?,?,?,?,?,?)",(pc.first+pc.last,pc.first,pc.last,pc.age,pc.gender,pc.career,pc.clothing,pc.ambition))

    player_update.commit()
    print("updated player info successfully.")

    player_update.close()


def load_player():
    try:
        with open('player_data',"r") as doc:
            line = doc.readlines()

        player_info = line[1].split(",")
        player_info = (
        player_info[0], player_info[1], player_info[2], player_info[3], player_info[4], player_info[5], player_info[6])

    except FileNotFoundError:
        print("Save not found.  Please create new Sim.")
        player_info = None

    return player_info


def load_player_sql():
    conn = sqlite3.connect("Characters.db")
    # print("Opened DB successfully.")

    while True:
        try:
            load_id = input("What is your Sim's name? ").title().split(" ")
            load_id = load_id[0]+load_id[1]
            break
        except IndexError:
            print("I need 2 names.")
            continue
    player_data = conn.execute("SELECT * from SIMS where ID = ?",(load_id,))

    for player_items in player_data:
        player_info = (player_items[1], player_items[2], player_items[3], player_items[4], player_items[5], player_items[6],
            player_items[7])

    try:
        return player_info
    except UnboundLocalError:
        return None


def create_player_Sim(X):
    loading_screens = ("Chlorinating Car Pools","Partitioning Social Network","Prelaminating Drywall Inventory","Blurring Reality Lines",
                       "Reticulating 3-Dimensional Splines","Preparing Captive Simulators","Capacitating Genetic Modifiers",
                       "Destabilizing Orbital Payloads","Sequencing Cinematic Specifiers","Branching Family Trees","Manipulating Modal Memory")
    help_reader()
    player_info = None
    while True:
        if X == "yes" or X == "y":
            player_info = get_player_info()
            player = Player(player_info[0], player_info[1], player_info[2], player_info[3], player_info[4], player_info[5],
                            player_info[6])
            Zzz = os.system('cls' if os.name == 'nt' else 'clear')
            print("Hello, {}".format(player_info[0]))
            return player
        else:
            player_info = load_player_sql()
            if player_info != None:
                Zzz = os.system('cls' if os.name == 'nt' else 'clear')
                print("\n"*25 + random.choice(loading_screens) + "...")
                player = Player(player_info[0], player_info[1], player_info[2], player_info[3], player_info[4],
                                player_info[5], player_info[6])
                time.sleep(1.25)
                Zzz = os.system('cls' if os.name == 'nt' else 'clear')
                return player
            else:
                print("Sorry, that name doesn't exist.  Create?")
                X = input()
                continue
