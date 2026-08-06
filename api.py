import requests
import streamlit as st

BASE = "https://api.henrikdev.xyz"


def headers():
    return {
        "Authorization": st.secrets["HENRIK_API_KEY"]
    }


@st.cache_data(ttl=300)
def get_account(name, tag):
    url = f"{BASE}/valorant/v1/account/{name}/{tag}"
    r = requests.get(url, headers=headers())
    r.raise_for_status()
    return r.json()["data"]


@st.cache_data(ttl=300)
def get_lifetime(name, tag, region):
    url = f"{BASE}/valorant/v1/lifetime/mmr/{region}/{name}/{tag}"
    r = requests.get(url, headers=headers())
    r.raise_for_status()
    return r.json()["data"]


@st.cache_data(ttl=300)
def get_matches(name, tag, region, size=20):
    url = f"{BASE}/valorant/v4/matches/{region}/pc/{name}/{tag}"

    r = requests.get(
        url,
        headers=headers(),
        params={
            "size": size
        }
    )

    r.raise_for_status()

    return r.json()["data"]


@st.cache_data(ttl=600)
def get_match_detail(region, match_id):
    url = f"{BASE}/valorant/v2/match/{region}/{match_id}"

    r = requests.get(
        url,
        headers=headers()
    )

    r.raise_for_status()

    return r.json()["data"]
