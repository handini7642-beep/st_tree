import streamlit as st

# 1. SET CONFIG & THEME CLEAN AESTHETIC
st.set_page_config(page_title="Storage Space - General Tree", layout="wide", page_icon="☁️")

# Menyuntikkan CSS Kustom untuk Background Soft & Desain Minimalis Modern
st.markdown("""
    <style>
    /* Background utama menggunakan warna Soft Sage / Warm Gray yang sangat teduh */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #F4F6F4; 
    }
    
    /* Mengubah sidebar agar senada */
    [data-testid="stSidebar"] {
        background-color: #EAEFEA;
    }
    
    /* Mengubah gaya container/card menjadi minimalis dengan border tipis */
    div[data-testid="stCard"] {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
        border: 1px solid #E2E8F0;
        transition: all 0.25s ease-in-out;
    }
    div[data-testid="stCard"]:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border-color: #CBD5E1;
    }
    
    /* Tombol dengan sudut membulat modern (bukan lingkaran alay) */
    .stButton > button {
        border-radius: 8px !important;
        transition: all 0.2s;
    }
    
    /* Desain teks judul */
    .main-title {
        font-size: 28px;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 5px;
    }
    .sub-title {
        font-size: 14px;
        color: #64748B;
        margin-bottom: 25px;
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
        ikon = "📁 " if node.is_folder else dapatkan_ikon_file(node.data)
        fav = " ⭐" if node.is_favorite else ""
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
        if ekstensi in ["pdf"]: return "📄 "
        if ekstensi in ["txt", "docx", "doc"]: return "📝 "
        if ekstensi in ["jpg", "jpeg", "png"]: return "🖼️ "
        if ekstensi in ["mp4", "mkv"]: return "🎬 "
        if ekstensi in ["zip", "rar"]: return "📦 "
    return "📄 "

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
    sistem_file = GeneralTree("Root")
    
    dokumen = TreeNode("Dokumen Kuliah", is_folder=True)
    foto = TreeNode("Foto_Ekskul", is_folder=True)
    
    sistem_file.root.add_child(dokumen)
    sistem_file.root.add_child(foto)

    dokumen.add_child(TreeNode("Catatan_Algoritma.txt", is_folder=False, ukuran_mb=2))
    dokumen.add_child(TreeNode("Tugas_Struktur_Data.pdf", is_folder=False, ukuran_mb=15))
    foto.add_child(TreeNode("Dokumentasi_PMR.jpg", is_folder=False, ukuran_mb=12))
    
    st.session_state.sistem_file = sistem_file
    st.session_state.current_node = sistem_file.root


# ====================================================================
# 5. ANTARMUKA UTAMA (STREAMLIT UI)
# ====================================================================

# HEADER MINIMALIS & CLEAN
st.markdown('<p class="main-title">☁️ Workspace Drive</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">File Management System Explorer — General Tree Implementation</p>', unsafe_allow_html=True)

# SIDEBAR PANEL
with st.sidebar:
    st.markdown("### 📊 Kapasitas Drive")
    stats = st.session_state.sistem_file.hitung_statistik()
    
    maks_kapasitas = 100
    persen_terpakai = min(stats['total_ukuran'] / maks_kapasitas, 1.0)
    
    st.progress(persen_terpakai)
    st.caption(f"**{stats['total_ukuran']} MB** digunakan dari **{maks_kapasitas} MB**")
    
    col_stat1, col_stat2 = st.columns(2)
    col_stat1.metric("Folder", f"{stats['folder']}")
    col_stat2.metric("File", f"{stats['file']}")
    
    st.markdown("---")
    st.markdown("### 🔍 Pencarian")
    kata_kunci = st.text_input("Cari nama file/folder...", placeholder="Ketik kata kunci...")
    
    if kata_kunci:
        hasil_cari = st.session_state.sistem_file.cari_global(kata_kunci)
        if hasil_cari:
            for item in hasil_cari:
                tipe_str = "Folder" if item.is_folder else "File"
                if st.button(f"👉 Buka: {item.data}", key=f"search_{id(item)}", use_container_width=True):
                    st.session_state.current_node = item if item.is_folder else item.parent
                    st.rerun()
        else:
            st.error("Item tidak ditemukan.")
            
    st.markdown("---")
    st.markdown("### ⭐ Akses Cepat")
    list_fav = st.session_state.sistem_file.dapatkan_semua_favorit()
    if not list_fav:
        st.caption("Belum ada item yang ditandai bintang.")
    else:
        for fav_node in list_fav:
            ikon_fav = "📁 " if fav_node.is_folder else dapatkan_ikon_file(fav_node.data)
            if st.button(f"{ikon_fav} {fav_node.data}", key=f"fav_{id(fav_node)}", use_container_width=True):
                st.session_state.current_node = fav_node if fav_node.is_folder else fav_node.parent
                st.rerun()


# --- BREADCRUMBS NAVIGASI JALUR ---
b_nodes = dapatkan_path_list(st.session_state.current_node)
cols_b = st.columns(len(b_nodes) * 2 - 1)

idx_col = 0
for i, node in enumerate(b_nodes):
    if cols_b[idx_col].button(node.data, key=f"breadcrumb_{id(node)}"):
        st.session_state.current_node = node
        st.rerun()
    idx_col += 1
    if idx_col < len(cols_b):
        cols_b[idx_col].write(" / ")
        idx_col += 1

st.markdown(" ")

# LAYOUT UTAMA
kolom_files, kolom_aksi = st.columns([2, 1])

with kolom_files:
    st.markdown("### 📁 Direktori Aktif")
    
    if st.session_state.current_node.parent is not None:
        if st.button("⬅️ Kembali ke Folder Atas", use_container_width=True):
            st.session_state.current_node = st.session_state.current_node.parent
            st.rerun()
            
    children_nodes = st.session_state.current_node.children
    if len(children_nodes) == 0:
        st.info("Folder ini kosong.")
    else:
        for child in children_nodes:
            ikon = "📁 " if child.is_folder else dapatkan_ikon_file(child.data)
            label_ukuran = "" if child.is_folder else f"({child.ukuran_mb} MB)"
            fav_status = "⭐" if child.is_favorite else "☆"
            
            # Card kontainer bergaya minimalis putih bersih
            with st.container(border=True):
                c1, c2, c3 = st.columns([3, 1, 1])
                c1.markdown(f"#### {ikon} {child.data} <span style='font-size:12px; color:#94A3B8;'>{label_ukuran}</span>", unsafe_allow_html=True)
                
                with c2:
                    if st.button(f"{fav_status} Favorit", key=f"fav_btn_{id(child)}", use_container_width=True):
                        child.is_favorite = not child.is_favorite
                        st.rerun()
                
                with c3:
                    if child.is_folder:
                        if st.button("Buka 📂", key=f"buka_{id(child)}", use_container_width=True):
                            st.session_state.current_node = child
                            st.rerun()
                    else:
                        st.button("Unduh 📥", key=f"dl_{id(child)}", use_container_width=True, disabled=True)

with kolom_aksi:
    st.markdown("### 🛠️ Panel Operasi")
    
    tab_tambah, tab_ubah, tab_hapus, tab_pohon = st.tabs(["➕ Tambah", "✏️ Rename", "🗑️ Hapus", "🌳 Tree Scheme"])
    
    with tab_tambah:
        nama_baru = st.text_input("Nama Item Baru:", key="add_name").strip()
        tipe = st.radio("Jenis Item:", ("Folder", "File"), horizontal=True)
        
        ukuran_input = 0
        if tipe == "File":
            ukuran_input = st.number_input("Ukuran File (MB):", min_value=1, max_value=50, value=2)
            
        if st.button("Buat Baru", type="primary", use_container_width=True):
            if not nama_baru:
                st.error("Nama tidak boleh kosong.")
            elif any(c.data.lower() == nama_baru.lower() for c in st.session_state.current_node.children):
                st.error("Nama sudah digunakan di folder ini.")
            elif tipe == "File" and (stats['total_ukuran'] + ukuran_input > maks_kapasitas):
                st.error("Penyimpanan tidak cukup.")
            else:
                is_folder_bool = (tipe == "Folder")
                st.session_state.current_node.add_child(TreeNode(nama_baru, is_folder=is_folder_bool, ukuran_mb=ukuran_input))
                st.success(f"Berhasil membuat {tipe.lower()} '{nama_baru}'")
                st.rerun()

    with tab_ubah:
        if len(st.session_state.current_node.children) == 0:
            st.caption("Tidak ada item.")
        else:
            opsi_ubah = [c.data for c in st.session_state.current_node.children]
            target_ubah = st.selectbox("Pilih Item:", opsi_ubah, key="select_rename")
            nama_ganti = st.text_input("Nama Baru:", key="input_rename").strip()
            
            if st.button("Simpan Nama", use_container_width=True):
                if nama_ganti and not any(c.data.lower() == nama_ganti.lower() for c in st.session_state.current_node.children):
                    for child in st.session_state.current_node.children:
                        if child.data == target_ubah:
                            child.data = nama_ganti
                            st.rerun()

    with tab_hapus:
        if len(st.session_state.current_node.children) == 0:
            st.caption("Tidak ada item.")
        else:
            opsi_hapus = [c.data for c in st.session_state.current_node.children]
            target_hapus = st.selectbox("Pilih Item yang Dihapus:", opsi_hapus, key="select_delete")
            
            if st.button("Hapus Permanen", type="primary", use_container_width=True):
                for child in st.session_state.current_node.children:
                    if child.data == target_hapus:
                        st.session_state.current_node.remove_child(child)
                        st.rerun()
                        
    with tab_pohon:
        st.write("Struktur Hierarki Logika Tree:")
        st.session_state.sistem_file.display_streamlit()
