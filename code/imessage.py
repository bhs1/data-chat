import sqlite3
import pandas as pd

#############################################
# Run this file to generate data/messages.txt
##############################################

def get_imessages():
    conn = sqlite3.connect("/Users/bensolis-cohen/Library/Messages/chat.db")
    cur = conn.cursor()
    cur.execute(" select name from sqlite_master where type = 'table' ")

    messages = pd.read_sql_query(
        """SELECT ROWID, text, handle_id, date
    FROM message T1 
    INNER JOIN chat_message_join T2 
        ON T2.chat_id=25
        AND T1.ROWID=T2.message_id 
    ORDER BY T1.date desc""",
        conn,
    )
    conn.close()
    return messages


HANDLE_DICTIONARY = {0: "Ben", 25: "Scott", 19: "Greg"}

counters = {
    "none_rows": 0,
    "total_rows": 0,
}


def load_database(messages_df):
    with open(
        "/Users/bensolis-cohen/Projects/Chat with my data/data/messages.txt", "w"
    ) as file:
        for index in range(len(messages_df) - 1, -1, -1):
            row = messages_df.iloc[index]
            raw_row = row["text"]
            counters["total_rows"] += 1
            # TODO(bensc): Seems chat.db has some NULL values. Would love to fix this but seems impossible.
            if raw_row is None:
                counters["none_rows"] += 1
                continue
            file.write(f"{HANDLE_DICTIONARY[row['handle_id']]} says: {raw_row}\n")


load_database(get_imessages())
print(counters)
