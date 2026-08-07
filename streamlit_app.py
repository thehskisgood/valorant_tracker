import streamlit as st
import pandas as pd
import plotly.express as px

from api import (
    get_account,
    get_lifetime,
    get_matches
)

from translations import (
    rank_name,
    agent_name,
    map_name
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


    current = lifetime.get(
        "current",
        {}
    )

    peak = lifetime.get(
        "peak",
        {}
    )


    st.subheader(
        f"👤 {account['name']}#{account['tag']}"
    )


    c1, c2, c3, c4 = st.columns(4)


    with c1:
        st.metric(
            "等級",
            account.get(
                "account_level",
                "-"
            )
        )


    with c2:
        st.metric(
            "目前 Rank",
            rank_name(
                current.get(
                    "tier",
                    {}
                ).get(
                    "name",
                    "-"
                )
            )
        )


    with c3:
        st.metric(
            "RR",
            current.get(
                "rr",
                "-"
            )
        )


    with c4:
        st.metric(
            "最高 Rank",
            rank_name(
                peak.get(
                    "tier",
                    {}
                ).get(
                    "name",
                    "-"
                )
            )
        )


    card = account.get(
        "card",
        {}
    ).get(
        "large"
    )


    if card:
        st.image(
            card,
            width=300
        )


    st.divider()


    total_kills = 0
    total_deaths = 0
    total_assists = 0

    agents = {}


    for match in matches:

        player = next(
            (
                p for p in match["players"]
                if p["puuid"] == account["puuid"]
            ),
            None
        )

        if not player:
            continue


        stats = player["stats"]

        total_kills += stats["kills"]
        total_deaths += stats["deaths"]
        total_assists += stats["assists"]


        agent = player["agent"]["name"]

        agents[agent] = (
            agents.get(agent, 0) + 1
        )


    st.subheader(
        "📊 最近20場統計"
    )


    a, b, c = st.columns(3)


    with a:
        st.metric(
            "擊殺",
            total_kills
        )


    with b:
        st.metric(
            "死亡",
            total_deaths
        )


    with c:

        kd = (
            total_kills / total_deaths
            if total_deaths
            else total_kills
        )

        st.metric(
            "K/D",
            round(kd, 2)
        )



    if agents:

        df = pd.DataFrame(
            {
                "Agent": [
                    agent_name(x)
                    for x in agents.keys()
                ],
                "場數": list(
                    agents.values()
                )
            }
        )


        fig = px.pie(
            df,
            names="Agent",
            values="場數"
        )


        st.subheader(
            "Agent 使用率"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    st.divider()


    st.subheader(
        "⚔ 最近對戰"
    )


    for match in matches:


        player = next(
            (
                p for p in match["players"]
                if p["puuid"] == account["puuid"]
            ),
            None
        )


        if not player:
            continue


        stats = player["stats"]


        title = (
            f"{map_name(match['metadata']['map']['name'])} | "
            f"{agent_name(player['agent']['name'])} | "
            f"{stats['kills']}/{stats['deaths']}/{stats['assists']}"
        )


        with st.expander(title):


            st.write(
                "模式:",
                match["metadata"]["queue"]["name"]
            )


            st.write(
                "時間:",
                match["metadata"]["started_at"]
            )


            st.write(
                "地圖:",
                map_name(
                    match["metadata"]["map"]["name"]
                )
            )


            st.write(
                "特務:",
                agent_name(
                    player["agent"]["name"]
                )
            )


            st.write(
                "KDA:",
                f"{stats['kills']}/{stats['deaths']}/{stats['assists']}"
            )


            st.write(
                "Damage:",
                stats["damage"]["dealt"]
            )


            st.write(
                "爆頭:",
                stats["headshots"]
            )


            st.divider()


            st.write(
                "👥 全部玩家"
            )


            for p in match["players"]:

                s = p["stats"]
    tier_name = (p.get('tier') or {}).get('name', '-')

                st.write(
        f"{p['name']}#{p['tag']} | "
        f"{agent_name(p['agent']['name'])} | "
        f"{s['kills']}/{s['deaths']}/{s['assists']} | "
        f"{rank_name(tier_name)}"
    )