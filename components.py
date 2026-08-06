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



def find_player(match, puuid):

    for p in match.get("players", []):

        if p.get("puuid") == puuid:
            return p

    return None



def match_card(match, puuid):

    meta = match.get("metadata", {})

    player = find_player(
        match,
        puuid
    )

    if not player:
        return


    stats = player.get(
        "stats",
        {}
    )


    map_raw = (
        meta.get("map", {})
        .get("name", "-")
    )

    mode = (
        meta.get("queue", {})
        .get("name", "-")
    )


    agent_raw = (
        player.get("agent", {})
        .get("name", "-")
    )


    kills = stats.get("kills", 0)
    deaths = stats.get("deaths", 0)
    assists = stats.get("assists", 0)


    title = (
        f"{map_name(map_raw)} | "
        f"{agent_name(agent_raw)} | "
        f"{kills}/{deaths}/{assists}"
    )


    with st.expander(title):

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "模式",
                mode
            )

        with col2:
            st.metric(
                "KDA",
                f"{kills}/{deaths}/{assists}"
            )

        with col3:
            st.metric(
                "Score",
                stats.get(
                    "score",
                    "-"
                )
            )


        st.write(
            "時間:",
            meta.get(
                "started_at",
                "-"
            )
        )


        st.write(
            "Agent:",
            agent_name(agent_raw)
        )


        damage = stats.get(
            "damage",
            {}
        )

        st.write(
            "傷害:",
            f"{damage.get('dealt',0)}"
        )


        st.divider()

        st.write(
            "玩家列表"
        )


        for p in match.get("players", []):

            s = p.get(
                "stats",
                {}
            )

            agent = (
                p.get("agent", {})
                .get("name", "-")
            )

            tier = (
                p.get("tier", {})
                .get("name", "-")
            )


            st.write(
                f"{p.get('name','-')}#"
                f"{p.get('tag','-')} | "
                f"{agent_name(agent)} | "
                f"{s.get('kills',0)}/"
                f"{s.get('deaths',0)}/"
                f"{s.get('assists',0)} | "
                f"{rank_name(tier)}"
            )
