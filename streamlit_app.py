import streamlit as st
import requests

# ====== 頁面設定 ======
st.set_page_config(page_title="Valorant 戰績查詢", page_icon="🎯", layout="centered")

BASE = "https://api.henrikdev.xyz"

# ====== 中文翻譯對照表 (台服官方譯名) ======
TIER_TRANSLATION = {
    "Unranked": "未定位",
    "Iron 1": "鐵牌 1", "Iron 2": "鐵牌 2", "Iron 3": "鐵牌 3",
    "Bronze 1": "銅牌 1", "Bronze 2": "銅牌 2", "Bronze 3": "銅牌 3",
    "Silver 1": "銀牌 1", "Silver 2": "銀牌 2", "Silver 3": "銀牌 3",
    "Gold 1": "金牌 1", "Gold 2": "金牌 2", "Gold 3": "金牌 3",
    "Platinum 1": "白金 1", "Platinum 2": "白金 2", "Platinum 3": "白金 3",
    "Diamond 1": "鑽石 1", "Diamond 2": "鑽石 2", "Diamond 3": "鑽石 3",
    "Ascendant 1": "超凡入聖 1", "Ascendant 2": "超凡入聖 2", "Ascendant 3": "超凡入聖 3",
    "Immortal 1": "神話 1", "Immortal 2": "神話 2", "Immortal 3": "神話 3",
    "Radiant": "輻能戰士"
}

AGENT_TRANSLATION = {
    "Jett": "婕提", "Phoenix": "菲尼克斯", "Brimstone": "布史東", "Sage": "聖祈",
    "Sova": "蘇法", "Raze": "芮茲", "Omen": "歐門", "Viper": "薇蝮",
    "Cypher": "瑟符", "Killjoy": "愷宙", "Breach": "叛奇", "Skye": "絲凱",
    "Astra": "亞星卓", "KAY/O": "ＫＡＹ／Ｏ", "Chamber": "錢博爾", "Fade": "菲德",
    "Yoru": "夜戮", "Neon": "妮虹", "Harbor": "哈泊", "Gekko": "蓋克",
    "Reyna": "蕾娜", "Deadlock": "蒂羅", "Vyse": "薇絲", "Clove": "珂樂芙",
    "Iso": "離索", "Tejo": "戴侯", "Miks": "米克什", "Veto": "維托", "Waylay": "維蕾"
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
    "Summit": "頂峰亭閣"
}

# ====== API 邏輯函式 ======
def get_headers(api_key):
    return {"Authorization": api_key}

def get_account(name, tag, headers):
    url = f"{BASE}/valorant/v1/account/{name}/{tag}"
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()["data"]

def get_mmr(name, tag, region, headers):
    url = f"{BASE}/valorant/v2/mmr/{region}/{name}/{tag}"
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()["data"]

def get_matches(name, tag, region, headers, size=5):
    url = f"{BASE}/valorant/v4/matches/{region}/pc/{name}/{tag}"
    r = requests.get(url, headers=headers, params={"size": size})
    r.raise_for_status()
    return r.json()["data"]

def scout(riot_id, region, headers):
    if "#" not in riot_id:
        st.error(f"格式錯誤：{riot_id}（格式要是 名稱#TAG）")
        return

    name, tag = riot_id.rsplit("#", 1)

    try:
        account = get_account(name, tag, headers)
        mmr = get_mmr(name, tag, region, headers)
        matches = get_matches(name, tag, region, headers)
    except requests.exceptions.HTTPError as e:
        st.error(f"查詢失敗 [{riot_id}]：{e}")
        return
    except Exception as e:
        st.error(f"發生錯誤 [{riot_id}]：{e}")
        return

    # 段位翻譯
    raw_rank = mmr.get("current_data", {}).get("currenttierpatched", "Unranked")
    rank = TIER_TRANSLATION.get(raw_rank, raw_rank)
    rr = mmr.get("current_data", {}).get("ranking_in_tier", "—")

    peak = mmr.get("highest_rank") or mmr.get("peak") or {}
    raw_peak = peak.get("patched_tier") or (peak.get("tier", {}) or {}).get("name") or "Unranked"
    peak_name = TIER_TRANSLATION.get(raw_peak, raw_peak)

    # 顯示玩家個人資訊
    st.subheader(f"👤 {account['name']}#{account['tag']} (等級 {account['account_level']})")
    
    col_card, col_img = st.columns([3, 1])
    with col_card:
        c1, c2, c3 = st.columns(3)
        c1.metric("目前段位", rank)
        c2.metric("目前 RR", str(rr))
        c3.metric("歷史最高", peak_name)
    
    # 玩家卡片背景圖 (若 API 有回傳小圖則顯示)
    card_img = account.get("card", {}).get("small")
    if card_img:
        with col_img:
            st.image(card_img, width=70)

    total_kills = total_deaths = total_assists = 0
    total_hs = total_bs = total_ls = 0
    total_damage = 0
    total_rounds = 0
    match_count = 0

    st.write("### ⚔️ 近期對戰紀錄")

    for m in matches:
        players_field = m.get("players", [])
        player_list = players_field.get("all_players", []) if isinstance(players_field, dict) else players_field

        me = next((p for p in player_list if p.get("puuid") == account.get("puuid")), None)
        if not me:
            continue

        stats = me.get("stats", {})
        kills = stats.get("kills", 0) or 0
        deaths = stats.get("deaths", 0) or 0
        assists = stats.get("assists", 0) or 0
        hs = stats.get("headshots", 0) or 0
        bs = stats.get("bodyshots", 0) or 0
        ls = stats.get("legshots", 0) or 0
        damage = (stats.get("damage") or {}).get("dealt", 0) or 0

        rounds = len(m.get("rounds", []) or [])
        meta = m.get("metadata", {})
        
        # 地圖與特務翻譯
        raw_map = meta.get("map", {}).get("name", "Unknown")
        map_zh = MAP_TRANSLATION.get(raw_map, raw_map)
        
        agent_obj = me.get("agent", {})
        raw_agent = agent_obj.get("name", "Unknown")
        agent_zh = AGENT_TRANSLATION.get(raw_agent, raw_agent)
        agent_icon = agent_obj.get("images", {}).get("small")

        # 渲染單場戰績
        with st.container():
            col_icon, col_info, col_kda = st.columns([1, 3, 2])
            
            with col_icon:
                if agent_icon:
                    st.image(agent_icon, width=45)
                else:
                    st.write("🎮")

            with col_info:
                st.markdown(f"**{map_zh}** (`{raw_map}`)")
                st.caption(f"使用特務：{agent_zh} ({raw_agent}) | 回合數：{rounds}")

            with col_kda:
                st.markdown(f"**{kills} / {deaths} / {assists}**")
                kd = (kills / deaths) if deaths > 0 else kills
                st.caption(f"K/D: {kd:.2f}")

            st.divider()

        total_kills += kills
        total_deaths += deaths
        total_assists += assists
        total_hs += hs
        total_bs += bs
        total_ls += ls
        total_damage += damage
        total_rounds += rounds
        match_count += 1

    # 近期表現統計數據
    if match_count > 0:
        avg_k = total_kills / match_count
        avg_d = total_deaths / match_count
        avg_a = total_assists / match_count
        kda = (total_kills / total_deaths) if total_deaths > 0 else float(total_kills)
        shot_total = total_hs + total_bs + total_ls
        hs_rate = (total_hs / shot_total * 100) if shot_total > 0 else 0
        adr = (total_damage / total_rounds) if total_rounds > 0 else 0

        st.markdown("#### 📊 近期綜合數據")
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric("平均 KDA", f"{avg_k:.1f}/{avg_d:.1f}/{avg_a:.1f}", f"KD: {kda:.2f}")
        m_col2.metric("爆頭率", f"{hs_rate:.1f}%")
        m_col3.metric("ADR (每回合傷害)", f"{adr:.1f}" if total_rounds > 0 else "無法計算")
    else:
        st.info("沒有可統計的對戰資料")

# ====== 網頁 UI 介面 ======
st.title("🎯 Valorant 戰績查詢")

with st.sidebar:
    st.header("⚙️ 設定")
    # 從 Streamlit Cloud Secrets 後台讀取 Key，不寫死在程式碼中
    default_api_key = st.secrets.get("HENRIK_API_KEY", "")
    api_key_input = st.text_input("API Key", value=default_api_key, type="password")
    region_input = st.selectbox("地區 (Region)", ["ap", "na", "eu", "kr", "latam", "br"], index=0)

input_text = st.text_area("輸入 Riot ID（一行一個，格式：名稱#TAG）：", placeholder="Player1#TW1", height=100)

if st.button("開始查詢", type="primary"):
    if not api_key_input:
        st.error("請先在側邊欄輸入 API Key 或設定 Streamlit Secrets！")
    elif not input_text.strip():
        st.warning("請先輸入至少一個 Riot ID！")
    else:
        riot_ids = [line.strip() for line in input_text.split("\n") if line.strip()]
        headers = get_headers(api_key_input)
        for rid in riot_ids:
            scout(rid, region_input, headers)
