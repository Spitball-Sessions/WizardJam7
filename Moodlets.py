import sqlite3,random, json

def adding_user_created_mood_ideas(entry_t):
    sql = sqlite3.connect("Characters.db")
    cursor = sql.cursor()
    if entry_t.tag != None and entry_t.score in (10,25,40):
        cursor.execute("INSERT INTO MOODLETS(ITEM, TAGS,POINTS)VALUES(?,?,?)",(entry_t.entry,entry_t.tag,entry_t.score))
        return
    else:
        return

def getting_mood_ideas(new_sim):
    sql = sqlite3.connect("Characters.db")
    cursor = sql.cursor()
    ideas = []
    cursor.execute("SELECT TAGS,ITEM,POINTS FROM MOODLETS")
    moods = cursor.fetchall()
    with open('Points.List', encoding='utf-8') as score_table:
        ideas_dict = json.loads(score_table.read())

    for k,v in ideas_dict.items():
        if v in (10,25,40):
            ideas.append(k)

    try:
        tags = random.sample(ideas,3)
    except ValueError:
        tags = []
    if new_sim != "yes" or new_sim != y:
        print("\nToday, for double points, you should try to accomplish something from one of these tags:\n"
          "                               {}".format(", ".join(tags).title()))
    try:
        moods_c = random.choice(moods)
        print("Or, do \"{}\" again, for {} points".format(moods_c[1],str(moods_c[2]*3)))
    except IndexError:
        return tags,None
    return tags, moods_c