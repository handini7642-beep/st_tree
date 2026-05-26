import streamlit as st

# ====================================================================
# 1. STRUKTUR DATA: NODE UNTUK GENERAL TREE (FILE EXPLORER)
# ====================================================================
class FileNode:
    def __init__(self, nama_item, is_folder=True, ukuran_kb=0):
        self.nama = nama_item
        self.is_folder = is_folder  
        self.ukuran = ukuran_kb if not is_folder else 0  
        self.children = []          
        self.parent = None  # Pointer ke induk untuk navigasi

    def add_child(self, child_node):
        """Menambahkan cabang baru (Insertion)"""
        child_node.parent = self
        self.children.append(child_node)
  
    def dapatkan_path_lengkap(self):
        """Mendapatkan string jalur unik dari Root sampai Node ini untuk ID Key"""
        jalur = []
        sementara = self
        while sementara is not None:
            jalur.insert(0, sementara.nama)
            sementara = sementara.parent
        return "/".join(jalur)


# ====================================================================
# 2. INISIALISASI DRIVE DATA (MIMIC WINDOWS DRIVE)
# ====================================================================
st.set_page_config(page_title="Windows File Explorer", page_icon="💻", layout="wide")

# Mengunci data di session_state agar struktur tree tidak ter-reset
if 'root' not in st.session_state:
    root = FileNode("Local Disk (C:)", is_folder=True)
    
    # Membuat Folder Bawaan
    documents = FileNode("Documents", is_folder=True)
    pictures = FileNode("Pictures", is_folder=True)
    downloads = FileNode("Downloads", is_folder=True)
    
    root.add_child(documents)
    root.add_child(pictures)
    root.add_child(downloads)
    
    # Mengisi file bawaan awal
    documents.add_child(FileNode("Tugas_Struktur_Data.pdf", is_folder=False, ukuran_kb=150))
    documents.add_child(FileNode("Catatan_Kuliah.txt", is_folder=False, ukuran_kb=45))
    
    st.session_state.root = root

# Pointer posisi folder aktif saat ini
if 'current_folder' not in st.session_state:
    st.session_state.current_folder = st.session_state.root


# ====================================================================
# 3. FUNGSI PEMBANTU NAVIGASI SIDEBAR (REKURSIF COCOK UNTUK UAS)
# ====================================================================
def dapatkan_breadcrumb(node):
    """Membuat susunan alamat teks di Address Bar atas"""
    jalur = []
    sementara = node
    while sementara is not None:
        jalur.insert(0, sementara.nama)
        sementara = sementara.parent
    return " 💻 This PC  ➔  " + "  ➔  ".join(jalur)

def render_sidebar_tree(node, depth=0):
    """Mencetak struktur pohon di sidebar kiri dengan Key Tombol yang Unik"""
    indentasi = "    " * depth
    if node.is_folder:
        # Membuat key unik gabungan dari path lengkap agar tombol bisa diklik normal
        key_tombol = f"btn_side_{node.dapatkan_path_lengkap()}_{depth}"
        
        if st.sidebar.button(f"{indentasi}📁 {node.nama}", key=key_tombol, use_container_width=True):
            st.session_state.current_folder = node
            st.rerun()
            
        for child in node.children:
            render_sidebar_tree(child, depth + 1)


# ====================================================================
# 4. IMPLEMENTASI ANTARMUKA UTAMA (WINDOWS STYLE UI)
# ====================================================================

st.title("💻 Windows File Explorer Simulator")
st.caption("Aplikasi Kelompok UAS Struktur Data — Implementasi Struktur Data General Tree")
st.write("---")

# --- BAGIAN A: WINDOWS TOOLBAR (TAMPILAN BARU UNTUK NEW ITEM & DELETE) ---
st.markdown("### 🛠️ Windows Ribbon Toolbar")
with st.container(border=True):
    col_t1, col_t2, col_t3, col_t4, col_t5 = st.columns([2, 3, 2, 2, 2])
    
    with col_t1:
        jenis_baru = st.selectbox("New Item Type", ["Folder", "File"], label_visibility="visible")
    
    with col_t2:
        # Menggunakan key session_state langsung agar teks bisa dihapus otomatis setelah create
        if "nama_baru_state" not in st.session_state:
            st.session_state.nama_baru_state = ""
        nama_baru = st.text_input("Name", placeholder="Ketik nama...", key="nama_baru_state")
    
    with col_t3:
        if jenis_baru == "File":
            if "ukuran_baru_state" not in st.session_state:
                st.session_state.ukuran_baru_state = 10
            ukuran_baru = st.number_input("Size (KB)", min_value=1, max_value=5000, key="ukuran_baru_state")
        else:
            ukuran_baru = 0
            st.text_input("Size (KB)", value="-", disabled=True)
            
    with col_t4:
        st.markdown("<div style='padding-top: 28px;'></div>", unsafe_allow_html=True)
        if st.button("➕ Create New", type="primary", use_container_width=True):
            if nama_baru.strip():
                # Cek duplikasi nama berkas
                nama_kembar = any(c.nama.lower() == nama_baru.strip().lower() for c in st.session_state.current_folder.children)
                
                if not nama_kembar:
                    is_f = True if jenis_baru == "Folder" else False
                    st.session_state.current_folder.add_child(FileNode(nama_baru.strip(), is_folder=is_f, ukuran_kb=ukuran_baru))
                    st.success(f"Sukses membuat {jenis_baru}!")
                    
                    # AKSI MENGHAPUS TULISAN DI KOLOM INPUT JIKA SUKSES:
                    st.session_state.nama_baru_state = ""
                    if jenis_baru == "File":
                        st.session_state.ukuran_baru_state = 10
                        
                    st.rerun()  # Refresh halaman agar data langsung muncul di HP & Laptop
                else:
                    st.error("Nama sudah ada!")
            else:
                st.warning("Nama wajib diisi!")
                
    with col_t5:
        st.markdown("<div style='padding-top: 28px;'></div>", unsafe_allow_html=True)
        if st.session_state.current_folder.children:
            # Menu drop-down untuk menghapus file secara instan dari toolbar
            opsi_hapus = [c.nama for c in st.session_state.current_folder.children]
            target_hapus = st.selectbox("Delete Item", ["-- Select Item --"] + opsi_hapus, label_visibility="collapsed")
            
            if target_hapus != "-- Select Item --":
                node_target = next((c for c in st.session_state.current_folder.children if c.nama == target_hapus), None)
                if node_target:
                    st.session_state.current_folder.children.remove(node_target)
                    st.rerun()
        else:
            st.button("🗑️ Empty Folder", disabled=True, use_container_width=True)

st.write(" ")

# --- BAGIAN B: WINDOWS ADDRESS BAR & BOX PENCARIAN (SEARCH) ---
col_up_btn, col_address_bar, col_search_box = st.columns([1, 8, 3])

with col_up_btn:
    # Tombol panah kembali ke atas (Up Level)
    if st.session_state.current_folder.parent is not None:
        if st.button("⬆️ Up", use_container_width=True):
            st.session_state.current_folder = st.session_state.current_folder.parent
            st.rerun()
    else:
        st.button("⬆️ Up", disabled=True, use_container_width=True)

with col_address_bar:
    # Menampilkan jalur folder saat ini secara dinamis
    st.text_input("Address", value=dapatkan_breadcrumb(st.session_state.current_folder), disabled=True, label_visibility="collapsed")

with col_search_box:
    # Kotak Pencarian Aktif
    kueri_cari = st.text_input("🔍 Search", placeholder="Search in this folder...", label_visibility="collapsed")

st.write("---")


# --- BAGIAN C: PEMBAGIAN PANEL UTAMA (SIDEBAR KIRI & ISI KANAN) ---
panel_navigasi, panel_konten = st.columns([3, 9], gap="large")

# 1. Tampilan Pengendali di Sidebar Kiri (Navigation Pane)
with panel_navigasi:
    st.markdown("### 🖥️ Navigation Pane")
    if st.sidebar.button("💻 This PC (Go to Root)", use_container_width=True):
        st.session_state.current_folder = st.session_state.root
        st.rerun()
    st.sidebar.markdown("---")
    
    # Memanggil algoritma pohon rekursif untuk mencetak isi navigasi samping
    render_sidebar_tree(st.session_state.root)

# 2. Tampilan Isi Folder di Sebelah Kanan (Main Contents Grid View)
with panel_konten:
    folder_sekarang = st.session_state.current_folder
    st.markdown(f"## 📂 {folder_sekarang.nama}")
    
    # Menyaring item berdasarkan kotak kata kunci Search Bar
    if kueri_cari.strip():
        daftar_tampil = [item for item in folder_sekarang.children if kueri_cari.lower() in item.nama.lower()]
    else:
        daftar_tampil = folder_sekarang.children

    if not daftar_tampil:
        st.info("Folder ini kosong atau item tidak ditemukan.")
    else:
        # Mengatur sistem grid 3 kolom menyamping agar muat di layar HP dan laptop
        kolom_grid = st.columns(3)
        
        for urutan, objek in enumerate(daftar_tampil):
            pilihan_kolom = kolom_grid[urutan % 3]
            
            with pilihan_kolom:
                with st.container(border=True):
                    if objek.is_folder:
                        st.markdown("### 📁")
                        st.markdown(f"**{objek.nama}**")
                        st.caption("Folder")
                        # Tombol buka folder di panel utama
                        if st.button("Open Folder", key=f"main_open_{objek.nama}_{urutan}"):
                            st.session_state.current_folder = objek
                            st.rerun()
                    else:
                        st.markdown("### 📄")
                        st.markdown(f"**{objek.nama}**")
                        st.caption(f"File ({objek.ukuran} KB)")
                        st.button("Properties", key=f"main_prop_{objek.nama}_{urutan}", disabled=True)
