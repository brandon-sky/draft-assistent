import streamlit as st
import pandas as pd


OFF_PATH = "data/offense.csv"
DEF_PATH = "data/defense.csv"

offense_positions = ["QB", "RB", "WR", "TE", "K"]
defense_positions = ["DL", "LB", "DB"]


@st.cache()
def initialize_cache():
    st.session_state.picked_players = [
        "Josh Allen",
        "Christian McCaffrey",
        "Tyreek Hill",
        "Mark Andrews",
        "Najee Harris",
        "Alvin Kamara",
        "Jonathan Taylor",
        "Lamar Jackson",
        "Saquon Barkley",
        "Javonte Williams",
        "George Kittle",
        "Austin Ekeler",
        "Leonard Fournette",
        "CeeDee Lamb",
        "D'Andre Swift",
        "Justin Herbert",
        "Ja'Marr Chase",
        "Kyle Pitts",
        "Micah Parsons",
        "Joe Mixon",
        "Stefon Diggs",
        "Aaron Donald",
        "T.J. Watt",
        "Dalvin Cook",
        "Davante Adams",
        "Justin Jefferson",
        "Cooper Kupp",
    ]
    st.session_state.my_team = [
        "Derrick Henry",
        "Nick Chubb",
        "Roquan Smith",
        "Patrick Mahomes II",
    ]


def get_data(path: str) -> pd.DataFrame:
    translator = {
        "RK": "rank",
        "PLAYER NAME": "name",
        "CLEAN_POS": "position",
        "BYE WEEK": "bye",
    }

    data = pd.read_csv(
        path, sep=";", usecols=["RK", "PLAYER NAME", "CLEAN_POS", "BYE WEEK"]
    )
    data.rename(columns=translator, inplace=True)
    return data


def get_available_players(data: pd.DataFrame) -> pd.DataFrame:

    mask_not_picked = ~data.name.isin(st.session_state.picked_players)
    mask_not_my_team = ~data.name.isin(st.session_state.my_team)

    return data[mask_not_picked & mask_not_my_team].sort_values("rank").copy()


def remove_player(names: list[str]) -> None:
    with st.form(key="Remove Player from Board"):

        available_players = list(set(names) - set(st.session_state.picked_players))

        player = st.selectbox(label="Picked Player", options=available_players)

        if st.form_submit_button(label="Remove Player"):
            st.session_state.picked_players.append(player)
            st.experimental_rerun()

    return


def undo_remove_player() -> None:
    with st.form(key="Undo Picked Player"):

        player = st.selectbox(
            label="Undo Picked Player", options=st.session_state.picked_players
        )

        if st.form_submit_button(label="Remove Player"):
            st.session_state.picked_players.remove(player)
            st.experimental_rerun()

    return


def pick_player(round: int, data: pd.DataFrame, pos: str):
    if len(st.session_state.my_team) >= round:
        st.success(f"#{round} Pick: {st.session_state.my_team[round-1]}")
    else:
        with st.form(key=f"{round}. Pick"):
            options = data[data.position == pos].sort_values("rank").head(15).name
            pick = st.selectbox(label=f"{round}. Pick", options=options)
            if st.form_submit_button(f"Pick {round}. Round"):
                st.session_state.my_team.append(pick)
                st.experimental_rerun()


def main() -> None:
    initialize_cache()

    st.header("Draft Assistent")

    offense = get_data(path=OFF_PATH)
    defense = get_data(path=DEF_PATH)

    display_draft, col1, col2 = st.columns([1, 2, 2])

    with display_draft:
        st.success("Super Smash Bros.")
        st.write(st.session_state.my_team)
        st.warning("Draft Log")
        st.write(st.session_state.picked_players[:-16:-1])

    ##############################################################
    ###### Remove Players
    ##############################################################
    with col1:
        st.subheader("Remove Players from Board")
        names = offense.name.to_list() + defense.name.to_list()
        remove_player(names=names)

        st.subheader("Offense")
        selected_pos_off = st.selectbox("Offense Position", options=offense_positions)
        available_off_players = get_available_players(offense)
        st.dataframe(
            data=available_off_players[
                available_off_players.position == selected_pos_off
            ]
        )
    with col2:
        st.subheader("Undo")
        undo_remove_player()

        st.subheader("Offense")
        selected_pos_def = st.selectbox("Defense Position", options=defense_positions)
        available_def_players = get_available_players(defense)
        st.dataframe(
            data=available_def_players[
                available_def_players.position == selected_pos_def
            ]
        )

    ##############################################################
    ###### Draft Board
    ##############################################################
    st.header("Draft Board")
    with st.expander("Draft Board", expanded=False):
        pick_player(round=1, data=available_off_players, pos="RB")
        pick_player(round=2, data=available_off_players, pos="RB")
        pick_player(round=3, data=available_def_players, pos="LB")
        pick_player(round=4, data=available_off_players, pos="QB")
        pick_player(round=5, data=available_off_players, pos="WR")
        pick_player(round=6, data=available_def_players, pos="LB")
        pick_player(round=7, data=available_off_players, pos="RB")
        pick_player(round=8, data=available_def_players, pos="LB")
        pick_player(round=9, data=available_off_players, pos="WR")
        pick_player(round=10, data=available_off_players, pos="RB")
        pick_player(round=11, data=available_def_players, pos="DL")
        pick_player(round=12, data=available_def_players, pos="DB")
        pick_player(round=13, data=available_def_players, pos="LB")
        pick_player(round=14, data=available_def_players, pos="DB")
        pick_player(round=15, data=available_def_players, pos="DL")
        pick_player(round=16, data=available_off_players, pos="TE")
        pick_player(round=17, data=available_off_players, pos="K")
        pick_player(round=18, data=available_off_players, pos="WR")
        pick_player(round=19, data=available_off_players, pos="RB")
        pick_player(round=20, data=available_off_players, pos="RB")
        pick_player(round=21, data=available_off_players, pos="LB")

    return


if __name__ == "__main__":
    main()
