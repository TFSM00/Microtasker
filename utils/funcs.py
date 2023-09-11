from datetime import datetime as dt
def taskTimeAgo(tdd: dict) -> str:
    for col in tdd:
        for task in tdd[col]:
            cardTimeLabel = "Created "
            dateCreated = dt.strptime(tdd[col][task][1], '%Y-%m-%d %H:%M:%S.%f')
            timeAgo = str(dt.now() - dateCreated).split(":")
            if "day" in timeAgo:
                cardTimeLabel += f"{timeAgo.split(',')[0]} ago"
            elif "month" in timeAgo:
                cardTimeLabel += f"{timeAgo.split(',')[0]} and {timeAgo.split(',')[1].strip()} ago"
            else:
                if int(timeAgo[0]) > 0:
                    if int(timeAgo[0]) == 1:
                        cardTimeLabel += "1 hour ago"
                    else:
                        cardTimeLabel += f"{int(timeAgo[0])} hours ago"
                else:
                    if int(timeAgo[1]) > 0:
                        if int(timeAgo[1]) == 1:
                            cardTimeLabel += "1 minute ago"
                        else:
                            cardTimeLabel += f"{int(timeAgo[1])} minutes ago"
                    else:
                        if int(timeAgo[2].split(".")[0]) == 1:
                            cardTimeLabel += "1 second ago"
                        else:
                            cardTimeLabel += f"{int(timeAgo[2].split('.')[0])} seconds ago" 
            tdd[col][task][1] = cardTimeLabel             
    return tdd
    