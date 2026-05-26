import streamlit as st
from collections import deque
import time
import random

# =========================================================
# CONFIG PAGE
# =========================================================
st.set_page_config(
    page_title="AI Maze Pathfinder",
    page_icon="🧩",
    layout="wide"
)

# =========================================================
# CSS MODERN UI
# =========================================================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #f4f7fb;
}

.block-container {
    padding-top: 1rem;
}

.title {
    font-size: 42px;
    font-weight: 700;
    color: #111827;
}

.subtitle {
    color: #6b7280;
    margin-bottom: 20px;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    margin-bottom: 15px;
}

.cell {
    text-align: center;
    padding: 14px;
    border-radius: 10px;
    font-weight: bold;
    margin: 2px;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SIZE
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

if "mode" not in st.session_state:
    st.session_state.mode = "wall"

if "start_pos" not in st.session_state:
    st.session_state.start_pos = (0, 0)

if "end_pos" not in st.session_state:
    st.session_state.end_pos = (ROWS-1, COLS-1)

# =========================================================
# BFS FUNCTION
# =========================================================
def bfs(maze, start, end):

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

        directions = [
            (0, 1),
            (1, 0),
            (-1, 0),
            (0, -1)
        ]

        for dx, dy in directions:

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
def generate_random_maze():

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

    st.title("🧩 AI Maze Pathfinder")
    st.caption("Breadth First Search")

    st.write("")

    st.markdown("## 🎮 Edit Mode")

    if st.button("⬛ Wall Mode", use_container_width=True):
        st.session_state.mode = "wall"

    if st.button("🟩 Set Start", use_container_width=True):
        st.session_state.mode = "start"

    if st.button("🟥 Set End", use_container_width=True):
        st.session_state.mode = "end"

    st.write("---")

    if st.button("🎲 Random Maze", use_container_width=True):

        st.session_state.maze = generate_random_maze()

        st.session_state.path = []
        st.session_state.visited = []

        st.rerun()

    if st.button("🚀 Solve BFS", use_container_width=True):

        path, visited = bfs(
            st.session_state.maze,
            st.session_state.start_pos,
            st.session_state.end_pos
        )

        st.session_state.path = path
        st.session_state.visited = visited

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
        st.session_state.start_pos = (0, 0)
        st.session_state.end_pos = (ROWS-1, COLS-1)

        st.rerun()

    st.write("---")

    st.markdown("## 📌 Keterangan")

    st.markdown("🟩 Start")
    st.markdown("🟥 End")
    st.markdown("⬛ Wall")
    st.markdown("🟦 Visited")
    st.markdown("🟨 Shortest Path")

# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div class='title'>
🌐 AI Maze Pathfinder
</div>
<div class='subtitle'>
Visualisasi BFS untuk mencari jalur tercepat
</div>
""", unsafe_allow_html=True)

# =========================================================
# INFO CARDS
# =========================================================
c1, c2, c3 = st.columns(3)

with c1:

    status = "✅ Solusi Ditemukan" if st.session_state.path else "❌ Belum Ada Solusi"

    st.markdown(f"""
    <div class='card'>
    <h4>Status</h4>
    <h2>{status}</h2>
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
st.write("## 🧩 Maze Area")

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
            warna = "#60a5fa"

        if (i, j) in path:
            warna = "#facc15"

        if maze[i][j] == "S":
            warna = "#22c55e"

        if maze[i][j] == "E":
            warna = "#ef4444"

        tombol = cols[j].button(
            text if text else " ",
            key=f"{i}-{j}",
            use_container_width=True
        )

        cols[j].markdown(
            f"""
            <div class='cell'
            style='background:{warna};'>
            {text}
            </div>
            """,
            unsafe_allow_html=True
        )

        # =====================================================
        # CLICK EVENT
        # =====================================================
        if tombol:

            mode = st.session_state.mode

            # WALL MODE
            if mode == "wall":

                if maze[i][j] == 0:
                    maze[i][j] = 1

                elif maze[i][j] == 1:
                    maze[i][j] = 0

            # START MODE
            elif mode == "start":

                old_x, old_y = st.session_state.start_pos

                maze[old_x][old_y] = 0

                maze[i][j] = "S"

                st.session_state.start_pos = (i, j)

            # END MODE
            elif mode == "end":

                old_x, old_y = st.session_state.end_pos

                maze[old_x][old_y] = 0

                maze[i][j] = "E"

                st.session_state.end_pos = (i, j)

            st.session_state.path = []
            st.session_state.visited = []

            st.rerun()

# =========================================================
# BFS VISIT ORDER
# =========================================================
st.write("---")

st.markdown("## 📍 BFS Traversal")

if st.session_state.visited:

    traversal = " ➜ ".join(
        [str(node) for node in st.session_state.visited]
    )

    st.markdown(f"""
    <div class='card'>
    {traversal}
    </div>
    """, unsafe_allow_html=True)

else:

    st.info("Traversal BFS belum dijalankan.")

# =========================================================
# FOOTER
# =========================================================
st.write("---")

st.markdown("""
<center>
AI Maze Pathfinder • Struktur Data • BFS Algorithm ❤️
</center>
""", unsafe_allow_html=True)
