import streamlit as st
from collections import deque

# =====================================================
# KONFIGURASI HALAMAN
# =====================================================
st.set_page_config(
    page_title="Maze Solver BFS",
    page_icon="🧩",
    layout="wide"
)

# =====================================================
# CSS MODERN GEN Z CLEAN
# =====================================================
st.markdown("""
<style>

.stApp {
    background-color: #f5f7fb;
}

.block-container {
    padding-top: 1rem;
}

div[data-testid="stSidebar"] {
    background-color: #ffffff;
}

.stButton button {
    border-radius: 12px;
    border: none;
    background-color: #4F8CFF;
    color: white;
    transition: 0.3s;
}

.stButton button:hover {
    background-color: #2563eb;
    transform: scale(1.03);
}

.maze-box {
    width: 45px;
    height: 45px;
    border-radius: 8px;
    margin: 2px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-weight: bold;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# INISIALISASI MAZE
# =====================================================
ROWS = 10
COLS = 10

if "maze" not in st.session_state:

    maze = [["empty" for _ in range(COLS)] for _ in range(ROWS)]

    maze[0][0] = "start"
    maze[9][9] = "end"

    st.session_state.maze = maze

if "path" not in st.session_state:
    st.session_state.path = []

# =====================================================
# BFS FUNCTION
# =====================================================
def bfs(maze, start, end):

    queue = deque()
    queue.append((start, [start]))

    visited = set()

    while queue:

        (x, y), path = queue.popleft()

        if (x, y) == end:
            return path

        if (x, y) in visited:
            continue

        visited.add((x, y))

        directions = [
            (0, 1),
            (1, 0),
            (-1, 0),
            (0, -1)
        ]

        for dx, dy in directions:

            nx, ny = x + dx, y + dy

            if (
                0 <= nx < ROWS and
                0 <= ny < COLS and
                maze[nx][ny] != "wall" and
                (nx, ny) not in visited
            ):

                queue.append(
                    ((nx, ny), path + [(nx, ny)])
                )

    return []

# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:

    st.title("🧩 Maze Solver")

    st.markdown("""
    ### Cara Pakai:
    1. Klik kotak untuk membuat tembok
    2. Hijau = Start
    3. Merah = End
    4. Klik Solve BFS
    """)

    if st.button("🚀 Solve BFS"):

        maze = st.session_state.maze

        start = (0, 0)
        end = (9, 9)

        hasil = bfs(maze, start, end)

        st.session_state.path = hasil

    if st.button("🔄 Reset Maze"):

        maze = [["empty" for _ in range(COLS)] for _ in range(ROWS)]

        maze[0][0] = "start"
        maze[9][9] = "end"

        st.session_state.maze = maze
        st.session_state.path = []

        st.rerun()

# =====================================================
# HEADER
# =====================================================
st.title("🌐 Maze Solver BFS")
st.caption("Simulasi Breadth First Search pada Maze")

st.write("---")

# =====================================================
# TAMPILAN MAZE
# =====================================================
maze = st.session_state.maze
path = st.session_state.path

for i in range(ROWS):

    cols = st.columns(COLS)

    for j in range(COLS):

        cell = maze[i][j]

        warna = "#dbeafe"
        text = ""

        if cell == "wall":
            warna = "#111827"

        elif cell == "start":
            warna = "#22c55e"
            text = "S"

        elif cell == "end":
            warna = "#ef4444"
            text = "E"

        if (i, j) in path and cell not in ["start", "end"]:
            warna = "#facc15"

        tombol = cols[j].button(
            text if text else " ",
            key=f"{i}-{j}",
            use_container_width=True
        )

        cols[j].markdown(
            f"""
            <style>
            div[data-testid="stButton"] button[kind="secondary"] {{
                background-color: {warna};
                height: 45px;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

        # KLIK UNTUK MEMBUAT TEMBOK
        if tombol:

            if maze[i][j] == "empty":
                maze[i][j] = "wall"

            elif maze[i][j] == "wall":
                maze[i][j] = "empty"

            st.session_state.path = []

            st.rerun()

# =====================================================
# INFO HASIL
# =====================================================
st.write("---")

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "📍 Panjang Jalur",
        len(path)
    )

with col2:

    if path:
        st.success("Jalur ditemukan!")
    else:
        st.warning("Belum ada jalur ditemukan.")
