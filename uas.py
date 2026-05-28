import streamlit as st

# 1. SET CONFIG & THEME AESTHETIC GEMES
st.set_page_config(page_title="PandaDrive 🐼 - File Explorer", layout="wide", page_icon="🦄")

# Menyuntikkan CSS Kustom untuk Gaya Visual Soft Pastel & Cute Layout
st.markdown("""
    <style>
    /* Mengubah font utama dan background aplikasi menjadi cream/soft pink pastel */
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@500;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Quicksand', sans-serif;
        background-color: #FFF9F9; /* Soft cream pink */
    }
    
    /* Mengubah gaya container/card folder menjadi membulat dan berbayangan lembut */
    div[data-testid="stCard"] {
        background-color: #FFFFFF;
        border-radius: 20px;
        padding: 18px;
        box-shadow: 0 8px 16px rgba(255, 182, 193, 0.2); /* Soft pink shadow */
        border: 2px solid #FFE4E6;
        transition: all 0.3s ease;
    }
    div[data-testid="stCard"]:hover {
        transform: scale(1.02);
        box-shadow: 0 12px 20px rgba(255, 182, 193, 0.4);
        border-color: #FBCFE8;
    }
    
    /* Membuat tombol-tombol bawaan streamlit ber-border membulat */
    .stButton > button {
        border-radius: 15px !important;
        border: none !important;
        transition: all 0.2s ease;
    }
    
    /* Kustomisasi Tab agar lebih lucu */
    button[data-baseweb="tab"] {
        font-weight: 700 !important;
        color: #9333EA !important;
    }
    </style>
""", unsafe_allow_html=True)

# ====================================================================
# 2. STRUKTUR DATA: NODE UNTUK GENERAL TREE
# ====================================================================
class TreeNode:
    def __init__(self, data, is_folder=True, ukuran_mb=0):
        self.data = data
        self.is_folder = is_folder  
        self.ukuran_mb = ukuran_mb if not is_folder else 0 
        self.is_favorite = False    
        self.children = []          
        self.parent = None          

    def add_child(self, child_node):
        child_node.parent = self    
        self.children.append(child_node)

    def remove_child(self, child_node):
        if child_node in self.children:
            self.children.remove(child_node)


class GeneralTree:
    def __init__(self, root_data):
        self.root = TreeNode(root_data, is_folder=True)

    def display_streamlit(self, node=None, level=0):
        if node is None:
            node = self.root
        ikon = "🎀 " if node.is_folder else dapatkan_ikon_file(node.data)
        fav = " 💞" if node.is_favorite else ""
        st.code("   " * level + f"└── {ikon}{node.data}{fav}", language="")
        for child in node.children:
            self.display_streamlit(child, level + 1)

    def cari_global(self, keyword, node=None, hasil=None):
        if node is None:
            node = self.root
            hasil = []
        if keyword.lower() in node.data.lower() and node != self.root:
            hasil.append(node)
        for child in node.children:
            self.cari_global(keyword, child, hasil)
        return hasil

    def dapatkan_semua_favorit(self, node=None, hasil=None):
        if node is None:
            node = self.root
            hasil = []
        if node.is_favorite:
            hasil.append(node)
        for child in node.children:
            self.dapatkan_semua_favorit(child, hasil)
        return hasil

    def hitung_statistik(self, node=None, stats=None):
        if node is None:
            node = self.root
            stats = {"folder": 0, "file": 0, "total_ukuran": 0}
        if node != self.root:
            if node.is_folder:
                stats["folder"] += 1
            else:
                stats["file"] += 1
                stats["total_ukuran"] += node.ukuran_mb
        for child in node.children:
            self.hitung_statistik(child, stats)
        return stats


# ====================================================================
# 3. FUNGSI PEMBANTU (UTILITIES)
# ====================================================================
def dapatkan_ikon_file(nama_file):
    if "." in nama_file:
        ekstensi = nama_file.split(".")[-1].lower()
        if ekstensi in ["pdf"]: return "🌸 "
        if ekstensi in ["txt", "docx", "doc"]: return "🧸 "
        if ekstensi in ["jpg", "jpeg", "png", "gif"]: return "🎨 "
        if ekstensi in ["mp4", "mkv"]: return "🍿 "
        if ekstensi in ["mp3"]: return "🎀 "
        if ekstensi in ["zip", "rar"]: return "🎁 "
    return "🧁 "

def dapatkan_path_list(node):
    path = []
    sementara = node
    while sementara is not None:
        path.insert(0, sementara)
        sementara = sementara.parent
    return path


# ====================================================================
# 4. INISIALISASI SESSION STATE
# ====================================================================
if "sistem_file" not in st.session_state:
    sistem_file = GeneralTree("PandaDrive")
    
    dokumen = TreeNode("Materi Kuliah 🦄", is_folder=True)
    foto = TreeNode("Memori Foto ✨", is_folder=True)
    
    sistem_file.root.add_child(dokumen)
    sistem_file.root.add_child(foto)

    dokumen.add_child(TreeNode("Catatan_Algoritma.txt", is_folder=False, ukuran_mb=2))
    dokumen.add_child(TreeNode("Tugas_Struktur_Data.pdf", is_folder=False, ukuran_mb=15))
    foto.add_child(TreeNode("Foto_Ekskul_Lucu.jpg", is_folder=False, ukuran_mb=22))
    
    st.session_state.sistem_file = sistem_file
    st.session_state.current_node = sistem_file.root


# ====================================================================
# 5. ANTARMUKA UTAMA (STREAMLIT UI)
# ====================================================================

# HEADER BANNER DENGAN GRADASI WARNA PASTEL CUTE
st.markdown("""
    <div style="background: linear-gradient(135deg, #FFDEE9, #B5FFFC); padding: 30px; border-radius: 25px; margin-bottom: 25px; text-align: center; border: 2px solid #FFF;">
        <h1 style='margin:0; font-weight: 700; color: #4A4A4A;'>🐼 PandaDrive Space</h1>
        <p style='margin:8px 0 0 0; color: #6B6B6B; font-size: 15px;'>Kelola file kuliah & memori kamu dengan struktur data General Tree yang gemes!</p>
    </div>
""", unsafe_allow_html=True)

# KONTEN UTAMA: MEMBAGI SIDEBAR DAN DASHBOARD UTAMA
with st.sidebar:
    st.markdown("### 🍧 Kuota Storage-mu")
    stats = st.session_state.sistem_file.hitung_statistik()
    
    maks_kapasitas = 100
    persen_terpakai = min(stats['total_ukuran'] / maks_kapasitas, 1.0)
    
    # Progress bar berwarna soft pink pastel
    st.progress(persen_terpakai)
    st.caption(f"**{stats['total_ukuran']} MB** terpakai dari **{maks_kapasitas} MB**")
    
    col_stat1, col_stat2 = st.columns(2)
    col_stat1.metric("Folder", f"{stats['folder']} 🎀")
    col_stat2.metric("File", f"{stats['file']} 🧁")
    
    st.markdown("---")
    st.markdown("### 🔍 Cari Berkas")
    kata_kunci = st.text_input("Ketik nama file...", placeholder="Cari apa hari ini? 📑")
    
    if kata_kunci:
        hasil_cari = st.session_state.sistem_file.cari_global(kata_kunci)
        if hasil_cari:
            for item in hasil_cari:
                tipe_str = "Folder" if item.is_folder else "File"
                if st.button(f"✨ Intip: {item.data}", key=f"search_{id(item)}", use_container_width=True):
                    st.session_state.current_node = item if item.is_folder else item.parent
                    st.rerun()
        else:
            st.error("Duh, berkasnya ga ketemu 👁️💧👁️")
            
    st.markdown("---")
    st.markdown("### 💞 Akses Cepat Pin")
    list_fav = st.session_state.sistem_file.dapatkan_semua_favorit()
    if not list_fav:
        st.caption("Belum ada file bintang tercinta.")
    else:
        for fav_node in list_fav:
            ikon_fav = "🎀 " if fav_node.is_folder else dapatkan_ikon_file(fav_node.data)
            if st.button(f"{ikon_fav} {fav_node.data}", key=f"fav_{id(fav_node)}", use_container_width=True):
                st.session_state.current_node = fav_node if fav_node.is_folder else fav_node.parent
                st.rerun()


# --- AREA KANAN: BREADCRUMBS (JALUR FOLDER) CUTE ---
b_nodes = dapatkan_path_list(st.session_state.current_node)
cols_b = st.columns(len(b_nodes) * 2 - 1)

idx_col = 0
for i, node in enumerate(b_nodes):
    if cols_b[idx_col].button(node.data, key=f"breadcrumb_{id(node)}"):
        st.session_state.current_node = node
        st.rerun()
    idx_col += 1
    if idx_col < len(cols_b):
        cols_b[idx_col].write(" 🐾 ")
        idx_col += 1

st.markdown(" ")

# LAYOUT HALAMAN ISI BERKAS
kolom_files, kolom_aksi = st.columns([1.8, 1])

with kolom_files:
    st.markdown("### 🍧 Isi Ruang Folder Saat Ini")
    
    if st.session_state.current_node.parent is not None:
        if st.button("⬅️ Naik Satu Tingkat Ke Atas", use_container_width=True):
            st.session_state.current_node = st.session_state.current_node.parent
            st.rerun()
            
    children_nodes = st.session_state.current_node.children
    if len(children_nodes) == 0:
        st.info("Folder ini masih kosong melompong... 🫙")
    else:
        for child in children_nodes:
            ikon = "🎀 " if child.is_folder else dapatkan_ikon_file(child.data)
            label_ukuran = "" if child.is_folder else f"({child.ukuran_mb} MB)"
            fav_status = "💖" if child.is_favorite else "🤍"
            
            # Setiap item dibungkus container card bergaya estetik
            with st.container(border=True):
                c1, c2, c3 = st.columns([3, 1, 1])
                c1.markdown(f"#### {ikon} {child.data} <span style='font-size:12px; color:#A1A1AA;'>{label_ukuran}</span>", unsafe_allow_html=True)
                
                with c2:
                    if st.button(f"{fav_status} Pin", key=f"fav_btn_{id(child)}", use_container_width=True):
                        child.is_favorite = not child.is_favorite
                        st.rerun()
                
                with c3:
                    if child.is_folder:
                        if st.button("Masuk 📂", key=f"buka_{id(child)}", use_container_width=True):
                            st.session_state.current_node = child
                            st.rerun()
                    else:
                        st.button("Unduh 📥", key=f"dl_{id(child)}", use_container_width=True, disabled=True)

with kolom_aksi:
    st.markdown("### 🛠️ Menu Aksi Kotak")
    
    tab_tambah, tab_ubah, tab_hapus, tab_pohon = st.tabs(["🧁 Tambah", "✏️ Ganti Nama", "🗑️ Buang", "🌳 Silsilah Tree"])
    
    with tab_tambah:
        nama_baru = st.text_input("Nama Objek Baru:", key="add_name", placeholder="Ketik nama di sini...").strip()
        tipe = st.radio("Tipe Objek:", ("Folder Baru 🎀", "File Baru 🧁"), horizontal=True)
        
        ukuran_input = 0
        if "File" in tipe:
            ukuran_input = st.number_input("Besar File (MB):", min_value=1, max_value=50, value=2)
            
        if st.button("Tambahkan Sekarang ✨", type="primary", use_container_width=True):
            if not nama_baru:
                st.error("Eits, namanya tidak boleh kosong ya!")
            elif any(c.data.lower() == nama_baru.lower() for c in st.session_state.current_node.children):
                st.error("Waduh, nama objek ini sudah kembar!")
            elif "File" in tipe and (stats['total_ukuran'] + ukuran_input > maks_kapasitas):
                st.error("⚠️ Yahh storage kamu kepenuhan, gagal simpan!")
            else:
                is_folder_bool = ("Folder" in tipe)
                st.session_state.current_node.add_child(TreeNode(nama_baru, is_folder=is_folder_bool, ukuran_mb=ukuran_input))
                st.success(f"Yey! Berhasil bikin berkas baru.")
                st.rerun()

    with tab_ubah:
        if len(st.session_state.current_node.children) == 0:
            st.caption("Ga ada apa-apa di sini.")
        else:
            opsi_ubah = [c.data for c in st.session_state.current_node.children]
            target_ubah = st.selectbox("Pilih yang mau diganti:", opsi_ubah, key="select_rename")
            nama_ganti = st.text_input("Ketik Nama Barunya:", key="input_rename").strip()
            
            if st.button("Simpan Nama Baru ✏️", use_container_width=True):
                if nama_ganti and not any(c.data.lower() == nama_ganti.lower() for c in st.session_state.current_node.children):
                    for child in st.session_state.current_node.children:
                        if child.data == target_ubah:
                            child.data = nama_ganti
                            st.rerun()

    with tab_hapus:
        if len(st.session_state.current_node.children) == 0:
            st.caption("Ga ada objek buat dibuang.")
        else:
            opsi_hapus = [c.data for c in st.session_state.current_node.children]
            target_hapus = st.selectbox("Pilih objek yang mau dibuang:", opsi_hapus, key="select_delete")
            
            if st.button("Buang Permanen 🗑️", type="primary", use_container_width=True):
                for child in st.session_state.current_node.children:
                    if child.data == target_hapus:
                        st.session_state.current_node.remove_child(child)
                        st.rerun()
                        
    with tab_pohon:
        st.caption("Skema Hubungan Induk-Anak (Struktur Pohon):")
        st.session_state.sistem_file.display_streamlit()
