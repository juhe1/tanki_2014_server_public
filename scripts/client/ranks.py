# 2014 ranks and garage https://web.archive.org/web/20140325225751/http://ru.tankiwiki.com/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F

ranks = [{"name":"", "score":0, "reward":0},
         {"name":"", "score":100, "reward":10},
         {"name":"", "score":500, "reward":40},
         {"name":"", "score":1500, "reward":120},
         {"name":"", "score":3700, "reward":230},
         {"name":"", "score":7100, "reward":420},
         {"name":"", "score":12300, "reward":740},
         {"name":"", "score":20000, "reward":950},
         {"name":"", "score":29000, "reward":1400},
         {"name":"", "score":41000, "reward":2000},
         {"name":"", "score":57000, "reward":2500},
         {"name":"", "score":76000, "reward":3100},
         {"name":"", "score":98000, "reward":3900},
         {"name":"", "score":125000, "reward":4600},
         {"name":"", "score":156000, "reward":5600},
         {"name":"", "score":192000, "reward":6600},
         {"name":"", "score":233000, "reward":7900},
         {"name":"", "score":280000, "reward":8900},
         {"name":"", "score":332000, "reward":10000},
         {"name":"", "score":390000, "reward":12000},
         {"name":"", "score":455000, "reward":14000},
         {"name":"", "score":527000, "reward":16000},
         {"name":"", "score":606000, "reward":17000},
         {"name":"", "score":692000, "reward":20000},
         {"name":"", "score":787000, "reward":22000},
         {"name":"", "score":889000, "reward":24000},
         {"name":"", "score":1000000, "reward":28000},
         {"name":"", "score":1122000, "reward":31000},
         {"name":"", "score":1255000, "reward":34000},
         {"name":"", "score":1400000, "reward":37000},
]

def get_rank_by_id(_id):
    return ranks[_id - 1]

def get_rank_id_by_score(score):
    for index, rank in enumerate(ranks):
        if score < rank["score"]:
            return index - 1
