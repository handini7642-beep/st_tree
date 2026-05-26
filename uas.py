import streamlit as st
from collections import deque

# =========================================================
# PAGE CONFIG
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
# SIDEBAR
# =========================================================
with st.sidebar:

    st.title("🧩 AI Maze Pathfinder")
    st.caption("Breadth First Search")

    st.write("")

    if st.button("🚀 Solve BFS", use_container_width=True):

        hasil_path, hasil_visit = bfs(
            st.session_state.maze
        )

        st.session_state.path = hasil_path
        st.session_state.visited = hasil_visit

        st.rerun()

    if st.button("🔄 Reset Maze", use_container_width=True):

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
Klik kotak untuk membuat atau menghapus tembok
</div>
""", unsafe_allow_html=True)

# =========================================================
# INFO CARD
# =========================================================
c1, c2, c3 = st.columns(3)

with c1:

    status = (
        "✅ Solusi Ditemukan"
        if st.session_state.path
        else "❌ Belum Ada Solusi"
    )

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
# MAZE AREA
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

        # WALL
        if maze[i][j] == 1:
            warna = "#111827"

        # START
        if maze[i][j] == "S":
            warna = "#22c55e"
            text = "S"

        # END
        if maze[i][j] == "E":
            warna = "#ef4444"
            text = "E"

        # VISITED
        if (i, j) in visited:
            warna = "#60a5fa"

        # PATH
        if (i, j) in path:
            warna = "#facc15"

        # AGAR START & END TIDAK TERTIMPA
        if maze[i][j] == "S":
            warna = "#22c55e"

        if maze[i][j] == "E":
            warna = "#ef4444"

        # =====================================================
        # TOMBOL KOTAK
        # =====================================================
        tombol = cols[j].button(
            text if text else " ",
            key=f"{i}-{j}",
            use_container_width=True
        )

        # =====================================================
        # WARNA KOTAK
        # =====================================================
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
        # KLIK KOTAK = TOGGLE TEMBOK
        # =====================================================
        if tombol:

            # START & END TIDAK BISA DIUBAH
            if maze[i][j] not in ["S", "E"]:

                # JIKA JALAN → JADI TEMBOK
                if maze[i][j] == 0:
                    maze[i][j] = 1

                # JIKA TEMBOK → JADI JALAN
                elif maze[i][j] == 1:
                    maze[i][j] = 0

            st.session_state.path = []
            st.session_state.visited = []

            st.rerun()

# =========================================================
# BFS TRAVERSAL
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
AI Maze Pathfinder • BFS Algorithm • Struktur Data ❤️
</center>
""", unsafe_allow_html=True)
