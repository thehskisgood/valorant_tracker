import streamlit as st
import requests

# ====== 頁面設定 ======
st.set_page_config(page_title="Valorant 戰績查詢", page_icon="🎯", layout="centered")

BASE = "https://api.henrikdev.xyz"

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
        st.error(f"格式錯誤：{riot_id}（要是 名稱#TAG）")
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

    rank = mmr.get("current_data", {}).get("currenttierpatched", "未定位")
    rr = mmr.get("current_data", {}).get("ranking_in_tier", "—")

    peak = mmr.get("highest_rank") or mmr.get("peak") or {}
    peak_name = (
        peak.get("patched_tier")
        or (peak.get("tier", {}) or {}).get("name")
        or "未知"
    )

    # 渲染玩家基本資訊卡片
    st.subheader(f"👤 {account['name']}#{account['tag']} (等級 {account['account_level']})")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("目前段位", rank)
    col2.metric("目前 RR", str(rr))
    col3.metric("歷史最高段位", peak_name)

    total_kills = total_deaths = total_assists = 0
    total_hs = total_bs = total_ls = 0
    total_damage = 0
    total_rounds = 0
    match_count = 0

    match_logs = []

    for m in matches:
        players_field = m.get("players", [])
        if isinstance(players_field, dict):
            player_list = players_field.get("all_players", [])
        else:
            player_list = players_field

        me = None
        for p in player_list:
            if p.get("puuid") == account.get("puuid"):
                me = p
                break
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
        map_name = meta.get("map", {}).get("name", "?")
        agent_name = me.get("agent", {}).get("name", "?")

        match_logs.append({
            "地圖": map_name,
            "特務": agent_name,
            "戰績 (K/D/A)": f"{kills} / {deaths} / {assists}",
            "回合數": rounds
        })

        total_kills += kills
        total_deaths += deaths
        total_assists += assists
        total_hs += hs
        total_bs += bs
        total_ls += ls
        total_damage += damage
        total_rounds += rounds
        match_count += 1

    # 顯示近期對戰表格
    if match_logs:
        st.write("**近期對戰紀錄：**")
        st.table(match_logs)

    # 統計數據計算與顯示
    if match_count > 0:
        avg_k = total_kills / match_count
        avg_d = total_deaths / match_count
        avg_a = total_assists / match_count
        kda = (total_kills / total_deaths) if total_deaths > 0 else float(total_kills)
        shot_total = total_hs + total_bs + total_ls
        hs_rate = (total_hs / shot_total * 100) if shot_total > 0 else 0
        adr = (total_damage / total_rounds) if total_rounds > 0 else 0

        st.markdown("#### 綜合表現數據")
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric("平均 KDA", f"{avg_k:.1f}/{avg_d:.1f}/{avg_a:.1f}", f"KD: {kda:.2f}")
        m_col2.metric("爆頭率", f"{hs_rate:.1f}%")
        m_col3.metric("ADR (每回合傷害)", f"{adr:.1f}" if total_rounds > 0 else "無法計算")
    else:
        st.info("沒有可統計的對戰資料")
    
    st.divider()

# ====== 網頁 UI 介面 ======
st.title("🎯 Valorant 戰績快速查詢")

# 側邊欄：設定 API Key 與 伺服器
with st.sidebar:
    st.header("⚙️ 設定")
    
    # 嘗試從 Streamlit Secrets 讀取預設 API Key，如果沒有就留空讓使用者輸入
    default_api_key = st.secrets.get("HENRIK_API_KEY", "")

    
    api_key_input = st.text_input("API Key", value=default_api_key, type="password")
    region_input = st.selectbox("地區 (Region)", ["ap", "na", "eu", "kr", "latam", "br"], index=0)

# 主要輸入區
input_text = st.text_area(
    "輸入 Riot ID（一行一個，格式：名稱#TAG）：",
    placeholder="Player1#TW1\nPlayer2#1234",
    height=120
)

if st.button("開始查詢", type="primary"):
    if not api_key_input:
        st.error("請先在側邊欄輸入有效的 API Key！")
    elif not input_text.strip():
        st.warning("請先輸入至少一個 Riot ID！")
    else:
        riot_ids = [line.strip() for line in input_text.split("\n") if line.strip()]
        st.success(f"開始查詢 {len(riot_ids)} 位玩家...")
        
        headers = get_headers(api_key_input)
        
        for rid in riot_ids:
            scout(rid, region_input, headers)
