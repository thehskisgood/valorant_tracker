import streamlit as st
import pandas as pd
import plotly.express as px

from api import (
    get_account,
    get_lifetime,
    get_matches,
    get_match_detail
)

from components import (
    player_card,
    match_card
)


st.set_page_config(
    page_title="Valorant Tracker",
    page_icon="🎯",
    layout="wide"
)


st.title("🎯 Valorant Tracker")


region = st.sidebar.selectbox(
    "Region",
    [
        "ap",
        "na",
        "eu",
        "kr",
        "br",
        "latam"
    ]
)


riot_id = st.text_input(
    "Riot ID",
    placeholder="name#tag"
)


if st.button("搜尋"):

    if "#" not in riot_id:
        st.error("格式錯誤")
        st.stop()


    name, tag = riot_id.rsplit("#", 1)


    try:

        account = get_account(
            name,
            tag
        )

        lifetime = get_lifetime(
            name,
            tag,
            region
        )

        matches = get_matches(
            name,
            tag,
            region,
            20
        )


    except Exception as e:

        st.error(
            f"API Error: {e}"
        )

        st.stop()


    st.session_state.account = account
    st.session_state.lifetime = lifetime
    st.session_state.matches = matches


if "account" in st.session_state:


    account = st.session_state.account
    lifetime = st.session_state.lifetime
    matches = st.session_state.matches


    player_card(
        account,
        lifetime
    )


    st.divider()


    st.subheader(
        "📊 最近表現"
    )


    total_kills = 0
    total_deaths = 0
    total_assists = 0

    agents = {}
    maps = {}


    for match in matches:

        player = match["players"][0]

        stats = player["stats"]

        total_kills += stats["kills"]
        total_deaths += stats["deaths"]
        total_assists += stats["assists"]


        agent = player["agent"]["name"]

        agents[agent] = (
            agents.get(agent, 0) + 1
        )


        map_name = match["metadata"]["map"]["name"]

        maps[map_name] = (
            maps.get(map_name, 0) + 1
        )


    c1, c2, c3 = st.columns(3)


    with c1:

        st.metric(
            "總擊殺",
            total_kills
        )


    with c2:

        st.metric(
            "總死亡",
            total_deaths
        )


    with c3:

        kd = (
            total_kills / total_deaths
            if total_deaths
            else total_kills
        )

        st.metric(
            "K/D",
            round(kd, 2)
        )


    st.divider()


    if agents:

        st.subheader(
            "Agent 使用率"
        )


        df_agent = pd.DataFrame(
            {
                "Agent": list(agents.keys()),
                "Games": list(agents.values())
            }
        )


        fig = px.pie(
            df_agent,
            names="Agent",
            values="Games"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    st.divider()


    st.subheader(
        "⚔ 最近20場"
    )


    for match in matches:


        match_id = match["metadata"]["match_id"]


        player = match["players"][0]

        stats = player["stats"]

        title = (
            f"{match['metadata']['map']['name']} "
            f"| {player['agent']['name']} "
            f"| {stats['kills']}/{stats['deaths']}/{stats['assists']}"
        )


        with st.expander(title):


            st.write(
                "載入詳細資料..."
            )


            try:

                detail = get_match_detail(
                    region,
                    match_id
                )


                st.write(
                    "模式:",
                    detail["metadata"]["queue"]["name"]
                )


                st.write(
                    "時間:",
                    detail["metadata"]["started_at"]
                )


                st.write(
                    "玩家"
                )


                for p in detail["players"]:

                    s = p["stats"]


                    st.write(
                        f"{p['name']}#{p['tag']} | "
                        f"{p['agent']['name']} | "
                        f"{s['kills']}/{s['deaths']}/{s['assists']} | "
                        f"{p['tier']['name']}"
                    )


            except Exception as e:

                st.error(
                    str(e)
                )
