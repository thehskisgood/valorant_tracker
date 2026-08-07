RANK_TRANSLATION = {
    "Unrated": "未定位",
    "Iron 1": "鐵牌 1",
    "Iron 2": "鐵牌 2",
    "Iron 3": "鐵牌 3",
    "Bronze 1": "銅牌 1",
    "Bronze 2": "銅牌 2",
    "Bronze 3": "銅牌 3",
    "Silver 1": "銀牌 1",
    "Silver 2": "銀牌 2",
    "Silver 3": "銀牌 3",
    "Gold 1": "金牌 1",
    "Gold 2": "金牌 2",
    "Gold 3": "金牌 3",
    "Platinum 1": "白金 1",
    "Platinum 2": "白金 2",
    "Platinum 3": "白金 3",
    "Diamond 1": "鑽石 1",
    "Diamond 2": "鑽石 2",
    "Diamond 3": "鑽石 3",
    "Ascendant 1": "超凡入聖 1",
    "Ascendant 2": "超凡入聖 2",
    "Ascendant 3": "超凡入聖 3",
    "Immortal 1": "神話 1",
    "Immortal 2": "神話 2",
    "Immortal 3": "神話 3",
    "Radiant": "幅能戰魂"
}


AGENT_TRANSLATION = {
    "Jett": "婕提",
    "Phoenix": "菲尼克斯",
    "Brimstone": "布史東",
    "Sage": "聖祈",
    "Sova": "蘇法",
    "Raze": "芮茲",
    "Omen": "歐門",
    "Viper": "薇蝮",
    "Cypher": "瑟符",
    "Killjoy": "愷宙",
    "Breach": "叛奇",
    "Skye": "絲凱",
    "Astra": "亞星卓",
    "KAY/O": "KAY/O",
    "Chamber": "錢博爾",
    "Fade": "菲德",
    "Yoru": "夜戮",
    "Neon": "妮虹",
    "Harbor": "哈泊",
    "Gekko": "蓋克",
    "Reyna": "蕾娜",
    "Deadlock": "蒂羅",
    "Vyse": "薇絲",
    "Clove": "珂樂芙",
    "Iso": "離索",
    "Tejo": "戴侯",
    "Waylay": "維蕾",
    "Veto": "維托",
    "Miks" : "米克什"
}


MAP_TRANSLATION = {
    "Ascent": "義境空島",
    "Bind": "劫境之地",
    "Haven": "遺落境地",
    "Split": "雙塔迷城",
    "Icebox": "極地寒港",
    "Breeze": "熱帶樂園",
    "Fracture": "天漠之峽",
    "Pearl": "深海明珠",
    "Lotus": "蓮華古城",
    "Sunset": "日落之城",
    "Abyss": "深窟幽境",
    "Corrode": "晶蝕之地",
    "Summit" : "頂峰亭閣",
    "Skirmish A" : "火線交鋒A",
    "Skirmish B" : "火線交鋒B",
    "Skirmish C" : "火線交鋒C",
    "Skirmish D" : "火線交鋒D",
    "Skirmish E" : "火線交鋒E",
}


MODE_TRANSLATION = {
    "Competitive": "競技競技",
    "Unrated": "一般模式",
    "Spike Rush": "幅能搶攻戰",
    "Deathmatch": "死鬥模式",
    "Team Deathmatch": "團隊死鬥",
    "Escalation": "超激進戰",
    "Replication": "複製亂戰",
    "Custom Game": "自訂遊戲",
}


def rank_name(rank):
    return RANK_TRANSLATION.get(rank, rank)


def agent_name(agent):
    return AGENT_TRANSLATION.get(agent, agent)


def map_name(map_name):
    return MAP_TRANSLATION.get(map_name, map_name)

def mode_name(mode):
    return MODE_TRANSLATION.get(mode, mode)
