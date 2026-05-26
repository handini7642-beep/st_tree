import streamlit as st
from collections import deque
import random

# =========================================================
# CONFIG
# =========================================================
st.set_page_config(
    page_title="Maze Solver BFS",
    page_icon="🧩",
    layout="wide"
)

# =========================================================
# CSS MODERN UI
# =========================================================
st.markdown("""
<style>

body {
    background-color: #f5f7fb;
}

.stApp {
    background-color: #f5f7fb;
}

.block-container {
    padding-top: 1rem;
}

.title {
    font-size: 40px;
    font-weight: bold;
    color: #111827;
}

.subtitle {
    color: #6b7280;
    margin-bottom: 20px;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    margin-bottom: 15px;
}

.maze-box {
    text-align: center;
    padding: 12px;
    border-radius: 8px;
    font-weight: bold;
    color: white;
    margin: 2px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SIZE MAZE
# =========================================================
ROWS = 10
COLS = 10

# =========================================================
# SESSION STATE
# =========================================================
if "maze" not in st.session_state:

    maze = []

    for i in range(ROWS):

        row = []

        for j in range(COLS):

            row.append(0)

        maze.append(row)

    maze[0][0] = "S"
    maze[ROWS-1][COLS-1] = "E"

    st.session_state.maze = maze

if "path" not in st.session_state:
    st.session_state.path = []

if "visited" not in st.session_state:
    st.session_state.visited = []

# =========================================================
# BFS FUNCTION
# =========================================================
def bfs(maze):

    start = (0, 0)
    end = (ROWS - 1, COLS - 1)

    queue = deque()
    queue.append((start, [start]))

    visited = set()
    visit_order = []

    while queue:

        (x, y), path = queue.popleft()

        if (x, y) in visited:
            continue

        visited.add((x, y))
        visit_order.append((x, y))

        if (x, y) == end:
            return path, visit_order

        arah = [
            (0, 1),
            (1, 0),
            (-1, 0),
            (0, -1)
        ]

        for dx, dy in arah:

            nx = x + dx
            ny = y + dy

            if (
                0 <= nx < ROWS and
                0 <= ny < COLS and
                maze[nx][ny] != 1 and
                (nx, ny) not in visited
            ):

                queue.append(
                    ((nx, ny), path + [(nx, ny)])
                )

    return [], visit_order

# =========================================================
# RANDOM MAZE
# =========================================================
def random_maze():

    maze = []

    for i in range(ROWS):

        row = []

        for j in range(COLS):

            if random.random() < 0.25:
                row.append(1)
            else:
                row.append(0)

        maze.append(row)

    maze[0][0] = "S"
    maze[ROWS-1][COLS-1] = "E"

    return maze

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:

    st.title("🧩 Maze Solver")
    st.caption("BFS Algorithm")

    st.write("")

    if st.button("🎲 Buat Maze Acak", use_container_width=True):

        st.session_state.maze = random_maze()

        st.session_state.path = []
        st.session_state.visited = []

        st.rerun()

    if st.button("🚀 Solve BFS", use_container_width=True):

        hasil_path, hasil_visit = bfs(
            st.session_state.maze
        )

        st.session_state.path = hasil_path
        st.session_state.visited = hasil_visit

        st.rerun()

    if st.button("🔄 Reset", use_container_width=True):

        maze = []

        for i in range(ROWS):

            row = []

            for j in range(COLS):

                row.append(0)

            maze.append(row)

        maze[0][0] = "S"
        maze[ROWS-1][COLS-1] = "E"

        st.session_state.maze = maze
        st.session_state.path = []
        st.session_state.visited = []

        st.rerun()

    st.write("---")

    st.markdown("### Keterangan")

    st.markdown("🟩 Start")
    st.markdown("🟥 End")
    st.markdown("⬛ Tembok")
    st.markdown("🟦 Dikunjungi")
    st.markdown("🟨 Jalur")

# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div class='title'>
🌐 Maze Solver (BFS)
</div>
<div class='subtitle'>
Mencari jalur tercepat menggunakan algoritma BFS
</div>
""", unsafe_allow_html=True)

# =========================================================
# INFO CARDS
# =========================================================
c1, c2, c3 = st.columns(3)

with c1:

    st.markdown(f"""
    <div class='card'>
    <h4>Status</h4>
    <h2>
    {"✅ Solusi Ditemukan" if st.session_state.path else "❌ Belum Ada Solusi"}
    </h2>
    </div>
    """, unsafe_allow_html=True)

with c2:

    st.markdown(f"""
    <div class='card'>
    <h4>Panjang Jalur</h4>
    <h1>{len(st.session_state.path)}</h1>
    </div>
    """, unsafe_allow_html=True)

with c3:

    st.markdown(f"""
    <div class='card'>
    <h4>Node Dikunjungi</h4>
    <h1>{len(st.session_state.visited)}</h1>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# MAZE DISPLAY
# =========================================================
st.write("## Maze")

maze = st.session_state.maze
path = st.session_state.path
visited = st.session_state.visited

for i in range(ROWS):

    cols = st.columns(COLS)

    for j in range(COLS):

        warna = "#ffffff"
        text = ""

        if maze[i][j] == 1:
            warna = "#111827"

        if maze[i][j] == "S":
            warna = "#22c55e"
            text = "S"

        if maze[i][j] == "E":
            warna = "#ef4444"
            text = "E"

        if (i, j) in visited:
            warna = "#93c5fd"

        if (i, j) in path:
            warna = "#facc15"

        if maze[i][j] == "S":
            warna = "#22c55e"

        if maze[i][j] == "E":
            warna = "#ef4444"

        cols[j].markdown(
            f"""
            <div class='maze-box'
            style='background:{warna};'>
            {text}
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================================================
# FOOTER
# =========================================================
st.write("---")

st.markdown("""
<center>
Maze Solver BFS • Struktur Data • Streamlit ❤️
</center>
""", unsafe_allow_html=True)
