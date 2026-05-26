import streamlit as st

# =========================================================
# CLASS NODE GENERAL TREE
# =========================================================
class FileNode:
    def __init__(self, nama_item, is_folder=True, ukuran_kb=0):
        self.nama = nama_item
        self.is_folder = is_folder
        self.ukuran = ukuran_kb if not is_folder else 0
        self.children = []
        self.parent = None

    # INSERTION NODE
    def add_child(self, child_node):
        child_node.parent = self
        self.children.append(child_node)

    # PATH LENGKAP
    def dapatkan_path_lengkap(self):
        jalur = []
        sementara = self

        while sementara is not None:
            jalur.insert(0, sementara.nama)
            sementara = sementara.parent

        return "/".join(jalur)


# =========================================================
# STREAMLIT CONFIG
# =========================================================
st.set_page_config(
    page_title="Windows File Explorer",
    page_icon="💻",
    layout="wide"
)

# =========================================================
# CSS WINDOWS STYLE
# =========================================================
st.markdown("""
<style>

.stButton button {
    border-radius: 5px;
}

[data-testid="stSidebar"] {
    background-color: #f1f3f4;
}

.block-container {
    padding-top: 1rem;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# INISIALISASI TREE
# =========================================================
if 'root' not in st.session_state:

    root = FileNode("Local Disk (C:)", True)

    documents = FileNode("Documents", True)
    downloads = FileNode("Downloads", True)
    pictures = FileNode("Pictures", True)

    root.add_child(documents)
    root.add_child(downloads)
    root.add_child(pictures)

    # FILE AWAL
    documents.add_child(
        FileNode(
            "Tugas_UAS_Struktur_Data.pdf",
            False,
            150
        )
    )

    documents.add_child(
        FileNode(
            "Catatan_Kuliah.txt",
            False,
            45
        )
    )

    st.session_state.root = root

# FOLDER AKTIF
if 'current_folder' not in st.session_state:
    st.session_state.current_folder = st.session_state.root

# STATE INPUT
if 'nama_baru' not in st.session_state:
    st.session_state.nama_baru = ""

if 'ukuran_baru' not in st.session_state:
    st.session_state.ukuran_baru = 10


# =========================================================
# FUNGSI BREADCRUMB
# =========================================================
def dapatkan_breadcrumb(node):

    jalur = []

    sementara = node

    while sementara is not None:
        jalur.insert(0, sementara.nama)
        sementara = sementara.parent

    return " 💻 This PC > " + " > ".join(jalur)


# =========================================================
# FUNGSI SIDEBAR TREE REKURSIF
# =========================================================
def render_sidebar_tree(node, depth=0):

    indentasi = "    " * depth

    if node.is_folder:

        if st.button(
            f"{indentasi}📁 {node.nama}",
            key=f"side_{node.dapatkan_path_lengkap()}"
        ):

            st.session_state.current_folder = node
            st.rerun()

        for child in node.children:
            render_sidebar_tree(child, depth + 1)


# =========================================================
# HEADER
# =========================================================
st.title("💻 Windows File Explorer Simulator")

st.caption(
    "Implementasi Struktur Data General Tree"
)

st.write("---")

# =========================================================
# TOOLBAR WINDOWS
# =========================================================
st.markdown("### 🛠️ Toolbar")

col1, col2, col3, col4 = st.columns([2,3,2,2])

with col1:

    jenis_item = st.selectbox(
        "Type",
        ["Folder", "File"]
    )

with col2:

    nama_item = st.text_input(
        "Name",
        key="nama_baru"
    )

with col3:

    if jenis_item == "File":

        ukuran_item = st.number_input(
            "Size KB",
            min_value=1,
            max_value=9999,
            key="ukuran_baru"
        )

    else:

        ukuran_item = 0

        st.text_input(
            "Size KB",
            value="-",
            disabled=True
        )

with col4:

    st.write("")

    st.write("")

    if st.button(
        "➕ Create",
        use_container_width=True
    ):

        if nama_item.strip():

            nama_kembar = any(
                c.nama.lower() == nama_item.lower()
                for c in st.session_state.current_folder.children
            )

            if not nama_kembar:

                is_folder = (
                    True
                    if jenis_item == "Folder"
                    else False
                )

                node_baru = FileNode(
                    nama_item.strip(),
                    is_folder,
                    ukuran_item
                )

                st.session_state.current_folder.add_child(node_baru)

                # RESET INPUT
                st.session_state.nama_baru = ""

                st.session_state.ukuran_baru = 10

                st.toast("Item berhasil dibuat!")

                st.rerun()

            else:
                st.error("Nama sudah ada!")

        else:
            st.warning("Nama wajib diisi!")

st.write("---")

# =========================================================
# ADDRESS BAR + SEARCH
# =========================================================
c1, c2, c3 = st.columns([1,8,3])

with c1:

    if st.session_state.current_folder.parent is not None:

        if st.button("⬆️ Up"):

            st.session_state.current_folder = (
                st.session_state.current_folder.parent
            )

            st.rerun()

    else:
        st.button("⬆️ Up", disabled=True)

with c2:

    st.text_input(
        "Address",
        value=dapatkan_breadcrumb(
            st.session_state.current_folder
        ),
        disabled=True,
        label_visibility="collapsed"
    )

with c3:

    search = st.text_input(
        "Search",
        placeholder="Search file...",
        label_visibility="collapsed"
    )

st.write("---")

# =========================================================
# LAYOUT
# =========================================================
sidebar_kiri, konten_kanan = st.columns([3,9])

# =========================================================
# SIDEBAR NAVIGASI
# =========================================================
with sidebar_kiri:

    st.markdown("### 📂 Navigation")

    if st.button(
        "💻 This PC",
        use_container_width=True
    ):

        st.session_state.current_folder = (
            st.session_state.root
        )

        st.rerun()

    st.write("---")

    render_sidebar_tree(
        st.session_state.root
    )

# =========================================================
# KONTEN FILE EXPLORER
# =========================================================
with konten_kanan:

    folder = st.session_state.current_folder

    st.markdown(f"## 📁 {folder.nama}")

    # SEARCH FILTER
    if search.strip():

        daftar_file = [

            item for item in folder.children

            if search.lower()
            in item.nama.lower()

        ]

    else:

        daftar_file = folder.children

    # HEADER
    h1, h2, h3, h4 = st.columns([5,2,2,2])

    with h1:
        st.markdown("**Name**")

    with h2:
        st.markdown("**Type**")

    with h3:
        st.markdown("**Size**")

    with h4:
        st.markdown("**Action**")

    st.write("---")

    # DATA FILE
    if daftar_file:

        for idx, item in enumerate(daftar_file):

            c1, c2, c3, c4 = st.columns([5,2,2,2])

            with c1:

                ikon = (
                    "📁"
                    if item.is_folder
                    else "📄"
                )

                st.write(
                    f"{ikon} {item.nama}"
                )

            with c2:

                if item.is_folder:
                    st.write("Folder")
                else:
                    st.write("File")

            with c3:

                if item.is_folder:
                    st.write("-")
                else:
                    st.write(
                        f"{item.ukuran} KB"
                    )

            with c4:

                if item.is_folder:

                    if st.button(
                        "Open",
                        key=f"open_{item.dapatkan_path_lengkap()}_{idx}"
                    ):

                        st.session_state.current_folder = item

                        st.rerun()

                else:

                    st.button(
                        "View",
                        disabled=True,
                        key=f"view_{item.dapatkan_path_lengkap()}_{idx}"
                    )

            st.write("---")

    else:

        st.info(
            "Folder kosong atau file tidak ditemukan."
        )
