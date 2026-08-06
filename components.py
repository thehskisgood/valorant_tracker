import streamlit as st
from translations import rank_name, agent_name, map_name


def player_card(account, lifetime):

    current = lifetime.get("current", {})
    peak = lifetime.get("peak", {})

    st.subheader(
        f"👤 {account['name']}#{account['tag']}"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "等級",
            account.get("account_level", "-")
        )

    with col2:
        st.metric(
            "目前 Rank",
            rank_name(
                current.get("tier", {}).get("name", "-")
            )
        )

    with col3:
        st.metric(
            "RR",
            current.get("rr", "-")
        )

    st.write(
        "最高段位:",
        rank_name(
            peak.get("tier", {}).get("name", "-")
        )
    )

    card = account.get("card", {}).get("large")

    if card:
        st.image(card, width=250)


def match_card(match):

    meta = match["metadata"]
    stats = match["players"][0]["stats"]

    map_raw = meta["map"]["name"]
    mode = meta["queue"]["name"]

    player = match["players"][0]

    agent = player["agent"]["name"]

    kills = stats["kills"]
    deaths = stats["deaths"]
    assists = stats["assists"]

    with st.expander(
        f"{map_name(map_raw)} | {agent_name(agent)} | {kills}/{deaths}/{assists}"
    ):

        st.write(
            "模式:",
            mode
        )

        st.write(
            "時間:",
            meta["started_at"]
        )

        st.write(
            "Agent:",
            agent_name(agent)
        )

        st.write(
            "KDA:",
            f"{kills}/{deaths}/{assists}"
        )

        st.write(
            "Score:",
            stats["score"]
        )

        st.write(
            "傷害:",
            stats["damage"]["dealt"]
        )

        st.divider()

        st.write("玩家列表")

        for p in match["players"]:

            s = p["stats"]

            st.write(
                f"{p['name']}#{p['tag']} | "
                f"{agent_name(p['agent']['name'])} | "
                f"{s['kills']}/{s['deaths']}/{s['assists']} | "
                f"{rank_name(p['tier']['name'])}"
            )
