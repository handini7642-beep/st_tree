import streamlit as st
from datetime import datetime

# ====================================================================
# 1. STRUKTUR DATA: NODE UNTUK GENERAL TREE (FILE EXPLORER)
# ====================================================================
class FileNode:
    def __init__(self, nama_item, is_folder=True, ukuran_kb=0, tipe_format="File folder"):
        self.nama = nama_item
        self.is_folder = is_folder  
        self.ukuran = ukuran_kb if not is_folder else 0  
        self.tipe = tipe_format if not is_folder else "File folder"
        self.tgl_modifikasi = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.children = []          
        self.parent = None  # Pointer ke induk untuk navigasi jalan kembali

    def add_child(self, child_node):
        """Menambahkan cabang baru (Insertion)"""
        child_node.parent = self
        self.children.append(child_node)

    def dapatkan_path_lengkap(self):
        """Mendapatkan string jalur unik dari Root sampai Node ini"""
        jalur = []
        sementara = self
        while sementara is not None:
            jalur.insert(0, sementara.nama)
            sementara = sementara.parent
        return "/".join(jalur)


# ====================================================================
# 2. INISIALISASI DATA AWAL (MENIRU REPO FOLDER LAPTOP KAMU)
# ====================================================================
st.set_page_config(page_title="🌸 Aesthetic File Explorer 🦄", page_icon="💖", layout="wide")

# Custom CSS Google Font & Warna Pastel Gen Z (Lilac, Pink & Soft Blue Theme)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600&display=swap');
    
    * {
        font-family: 'Space Grotesk', sans-serif !important;
    }
    .stApp {
        background: linear-gradient(135deg, #fbc5d8 0%, #e6e6fa 100%);
    }
    div[data-testid="stBlock"] {
        background-color: rgba(255, 255, 255, 0.75);
        border-radius: 16px;
        padding: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    h1, h2, h3 {
        color: #6C5CE7 !important;
    }
    .stButton>button {
        background-color: #A29BFE !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #6C5CE7 !important;
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

if 'root' not in st.session_state:
    root = FileNode("Local Disk (C:)", is_folder=True)
    
    # Membuat sub-folder tiruan seperti yang ada di foto laptopmu
    documents = FileNode("Documents", is_folder=True)
    pictures = FileNode("Pictures", is_folder=True)
    downloads = FileNode("Downloads", is_folder=True)
    
    root.add_child(documents)
    root.add_child(pictures)
    root.add_child(downloads)
    
    # Mengisi file tiruan persis di dalam folder Documents kamu
    documents.add_child(FileNode("ALJABAR", is_folder=True))
    documents.add_child(FileNode("BASIS DATA SMT 2", is_folder=True))
    documents.add_child(FileNode("Handini SI 25 P AIS", is_folder=True))
    documents.add_child(FileNode("Handini Struktur Data Pemrograman", is_folder=True))
    documents.add_child(FileNode("PENGANTAR JARINGAN KOMPUTER", is_folder=True))
    documents.add_child(FileNode("Algoritma & Pemrograman.docx", is_folder=False, ukuran_kb=794, tipe_format="Microsoft Word Document"))
    documents.add_child(FileNode("BASIS DATA LAUNDRY KILOAN OLEH 2.docx", is_folder=False, ukuran_kb=9012, tipe_format="Microsoft Word Document"))
    documents.add_child(FileNode("basis data oleh oleh 2.xlsx", is_folder=False, ukuran_kb=13, tipe_format="Microsoft Excel Worksheet"))
    
    st.session_state.root = root

if 'current_folder' not in st.session_state:
    st.session_state.current_folder = st.session_state.root


# ====================================================================
# 3. FUNGSI PEMBANTU NAVIGASI (SUDAH DIPERBAIKI SECARA AMAN)
# ====================================================================
def dapatkan_breadcrumb(node):
    """Membuat susunan alamat teks di Address Bar atas (VERSI AMAN FIX)"""
    jalur = []
    sementara = node
    while sementara is not None:
        jalur.insert(0, sementara.nama)
        sementara = sementara.parent
    return " 📂 This PC > " + " > ".join(jalur)

def render_sidebar_tree(node, depth=0):
    """Mencetak pohon navigasi folder di bilah kiri"""
    indentasi = "    " * depth
    if node.is_folder:
        key_tombol = f"side_{node.dapatkan_path_lengkap()}_{depth}"
        if st.sidebar.button(f"{indentasi}🎀 {node.nama}", key=key_tombol, use_container_width=True):
            st.session_state.current_folder = node
            st.rerun()
        for child in node.children:
            render_sidebar_tree(child, depth + 1)


# ====================================================================
# 4. IMPLEMENTASI ANTARMUKA UTAMA (AESTHETIC WINDOWS DETAILS VIEW)
# ====================================================================

# Banner Utama Lucu
st.markdown("<h1 style='text-align: center; font-size: 40px;'>🦄 Storage Tree Master Y2K ✨</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6C5CE7;'>Aplikasi File Explorer Terlucu & Ter-Aesthetic se-Kampus 🌸</p>", unsafe_allow_html=True)
st.write("---")

# --- PANEL MENU ATAS (RIBBON TOOLBAR BARU) ---
st.markdown("### 🛠️ Cute Ribbon Toolbar")
with st.container():
    col_t1, col_t2, col_t3, col_t4, col_t5 = st.columns([2, 3, 2, 2, 2])
    
    with col_t1:
        jenis_baru = st.selectbox("🌈 Tipe Objek", ["Folder", "File"])
    
    with col_t2:
        if "nama_baru_state" not in st.session_state: st.session_state.nama_baru_state = ""
        nama_baru = st.text_input("📝 Nama Baru", placeholder="Ketik nama di sini...", key="nama_baru_state")
    
    with col_t3:
        if jenis_baru == "File":
            ext_pilihan = st.selectbox("🔮 Ekstensi", [".docx (Word)", ".xlsx (Excel)", ".pdf (Acrobat)", ".png (Gambar)", ".txt (Teks)"])
            if "ukuran_baru_state" not in st.session_state: st.session_state.ukuran_baru_state = 15
            ukuran_baru = st.number_input("💾 Ukuran (KB)", min_value=1, max_value=99999, key="ukuran_baru_state")
        else:
            ext_pilihan = ""
            ukuran_baru = 0
            st.text_input("🔮 Ekstensi", value="Folder", disabled=True)
            
    with col_t4:
        st.markdown("<div style='padding-top: 28px;'></div>", unsafe_allow_html=True)
        if st.button("✨ Create Object", type="primary", use_container_width=True):
            if nama_baru.strip():
                nama_fix = nama_baru.strip() + (ext_pilihan.split()[0] if jenis_baru == "File" else "")
                nama_kembar = any(c.nama.lower() == nama_fix.lower() for c in st.session_state.current_folder.children)
                
                if not nama_kembar:
                    is_f = True if jenis_baru == "Folder" else False
                    tipe_str = "File folder" if is_f else f"Microsoft {ext_pilihan.split()[1][1:-1]} Document"
                    
                    # Tambah data ke tree
                    st.session_state.current_folder.add_child(FileNode(nama_fix, is_folder=is_f, ukuran_kb=ukuran_baru, tipe_format=tipe_str))
                    st.toast(f"🍭 Yeay! Sukses bikin {jenis_baru} baru!", icon='🎉')
                    
                    # MENGHAPUS ISIAN DI KOLOM SECARA OTOMATIS:
                    st.session_state.nama_baru_state = ""
                    st.rerun()
                else:
                    st.error("🧁 Waduh, namanya udah ada yang pakai!")
            else:
                st.warning("🦄 Namanya jangan dikosongin ya!")
                
    with col_t5:
        st.markdown("<div style='padding-top: 28px;'></div>", unsafe_allow_html=True)
        if st.session_state.current_folder.children:
            opsi_hapus = [c.nama for c in st.session_state.current_folder.children]
            target_hapus = st.selectbox("🗑️ Hapus Objek", ["-- Pilih Item --"] + opsi_hapus, label_visibility="collapsed")
            
            if target_hapus != "-- Pilih Item --":
                node_target = next((c for c in st.session_state.current_folder.children if c.nama == target_hapus), None)
                if node_target:
                    st.session_state.current_folder.children.remove(node_target)
                    st.toast(f"Item '{target_hapus}' berhasil dibuang!", icon='🗑️')
                    st.rerun()
        else:
            st.button("🦄 Folder Kosong", disabled=True, use_container_width=True)

st.write(" ")

# --- WINDOWS PATH ADDRESS BAR & SEARCH BAR ---
col_up_btn, col_address_bar, col_search_box = st.columns([1, 8, 3])

with col_up_btn:
    if st.session_state.current_folder.parent is not None:
        if st.button("⬆️ Up", use_container_width=True):
            st.session_state.current_folder = st.session_state.current_folder.parent
            st.rerun()
    else:
        st.button("⬆️ Up", disabled=True, use_container_width=True)

with col_address_bar:
    st.text_input("Address", value=dapatkan_breadcrumb(st.session_state.current_folder), disabled=True, label_visibility="collapsed")

with col_search_box:
    kueri_cari = st.text_input("🔍 Search box", placeholder="Cari berkas di sini...", label_visibility="collapsed")

st.write("---")


# ====================================================================
# 5. PEMBAGIAN PANEL UTAMA (NAVIGATION TREE VS DETAILS TABLE VIEW)
# ====================================================================
panel_navigasi, panel_konten = st.columns([3, 9], gap="large")

with panel_navigasi:
    st.markdown("### 🧸 Navigation Pane")
    if st.button("💻 This PC (Home)", use_container_width=True):
        st.session_state.current_folder = st.session_state.root
        st.rerun()
    st.write("---")
    render_sidebar_tree(st.session_state.root)

with panel_konten:
    folder_sekarang = st.session_state.current_folder
    st.markdown(f"## 🍧 Current Directory: {folder_sekarang.nama}")
    st.write(" ")

    # Filter data berdasarkan isian kolom search bar
    if kueri_cari.strip():
        daftar_tampil = [item for item in folder_sekarang.children if kueri_cari.lower() in item.nama.lower()]
    else:
        daftar_tampil = folder_sekarang.children

    if not daftar_tampil:
        st.info("🍡 Folder ini masih kosong atau item tidak ditemukan.")
    else:
        # === TAMPILAN DETAILS VIEW TABEL PERSIS SEPERTI DI FOTO LAPTOP ===
        col_h_nama, col_h_tgl, col_h_tipe, col_h_ukuran, col_h_aksi = st.columns([4, 3, 3, 2, 2])
        with col_h_nama: st.markdown("**Name** 🔼")
        with col_h_tgl: st.markdown("**Date modified**")
        with col_h_tipe: st.markdown("**Type**")
        with col_h_ukuran: st.markdown("**Size**")
        with col_h_aksi: st.markdown("**Action**")
        st.markdown("<hr style='margin: 5px 0px; border-color: #A29BFE;'>", unsafe_allow_html=True)

        for idx, item in enumerate(daftar_tampil):
            col_nama, col_tgl, col_tipe, col_ukuran, col_aksi = st.columns([4, 3, 3, 2, 2])
            
            # Ikon estetika pastel pembeda folder dan file
            ikon = "🔮" if item.is_folder else "💎"
            
            with col_nama:
                st.write(f"{ikon} {item.nama}")
            with col_tgl:
                st.write(f"<span style='color: #747D8C;'>{item.tgl_modifikasi}</span>", unsafe_allow_html=True)
            with col_tipe:
                st.write(f"<span style='color: #747D8C;'>{item.tipe}</span>", unsafe_allow_html=True)
            with col_ukuran:
                text_ukuran = "-" if item.is_folder else f"{item.ukuran:,} KB"
                st.write(f"<span style='color: #747D8C;'>{text_ukuran}</span>", unsafe_allow_html=True)
            with col_aksi:
                if item.is_folder:
                    if st.button("Open", key=f"tbl_open_{item.dapatkan_path_lengkap()}_{idx}"):
                        st.session_state.current_folder = item
                        st.rerun()
                else:
                    st.button("File", key=f"tbl_file_{item.dapatkan_path_lengkap()}_{idx}", disabled=True)
            
            st.markdown("<hr style='margin: 2px 0px; border-color: #F1F2F6;'>", unsafe_allow_html=True)
