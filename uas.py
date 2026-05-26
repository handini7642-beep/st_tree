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
        self.parent = None  

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
# 2. FUNGSI PEMBANTU UNTUK MENCARI NODE BERDASARKAN PATH STR
# ====================================================================
def cari_node_lewat_path(root_node, path_str):
    if root_node.dapatkan_path_lengkap() == path_str:
        return root_node
    
    for child in root_node.children:
        if child.is_folder:
            hasil = cari_node_lewat_path(child, path_str)
            if hasil:
                return hasil
    return None


# ====================================================================
# 3. INISIALISASI DRIVE DATA (MIMIC WINDOWS DRIVE)
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

# Ambil data root dari state untuk digunakan di sepanjang kode
root_master = st.session_state.root

# Melacak posisi folder aktif menggunakan Path String agar stabil saat rerun
if 'current_folder_path' not in st.session_state:
    st.session_state.current_folder_path = root_master.dapatkan_path_lengkap()

# Ambil objek folder aktif saat ini berdasarkan path tracking
folder_sekarang = cari_node_lewat_path(root_master, st.session_state.current_folder_path)
if not folder_sekarang: # Jaga-jaga jika path tidak ditemukan, kembalikan ke root
    folder_sekarang = root_master
    st.session_state.current_folder_path = root_master.dapatkan_path_lengkap()


# ====================================================================
# 4. FUNGSI REKURSIF UNTUK SIDEBAR NAVIGATION
# ====================================================================
def render_sidebar_tree(node, depth=0):
    """Mencetak struktur pohon di sidebar kiri dengan rapi"""
    indentasi = "    " * depth
    if node.is_folder:
        key_tombol = f"side_{node.dapatkan_path_lengkap()}_{depth}"
        
        # Tampilkan nama folder di sidebar menggunakan st.sidebar secara konsisten
        if st.sidebar.button(f"{indentasi}📁 {node.nama}", key=key_tombol, use_container_width=True):
            st.session_state.current_folder_path = node.dapatkan_path_lengkap()
            st.rerun()
            
        for child in node.children:
            render_sidebar_tree(child, depth + 1)


# ====================================================================
# 5. IMPLEMENTASI ANTARMUKA UTAMA (WINDOWS STYLE UI)
# ====================================================================

st.title("💻 Windows File Explorer Simulator")
st.caption("Aplikasi Kelompok UAS Struktur Data — Implementasi Struktur Data General Tree")
st.write("---")

# --- BAGIAN A: WINDOWS TOOLBAR (SINKRONISASI PEMBUATAN & PENGHAPUSAN) ---
st.markdown("### 🛠️ Windows Ribbon Toolbar")
with st.container(border=True):
    col_t1, col_t2, col_t3, col_t4 = st.columns([2, 4, 2, 2])
    
    with col_t1:
        jenis_baru = st.selectbox("New Item Type", ["Folder", "File"], key="jenis_baru_key")
    
    with col_t2:
        # Input nama menggunakan key state standar agar mudah dikontrol
        nama_baru = st.text_input("Name", placeholder="Ketik nama...", key="input_nama_baru")
    
    with col_t3:
        if jenis_baru == "File":
            ukuran_baru = st.number_input("Size (KB)", min_value=1, max_value=5000, value=10, key="input_ukuran_baru")
        else:
            ukuran_baru = 0
            st.text_input("Size (KB)", value="-", disabled=True, key="input_ukuran_disabled")
            
    with col_t4:
        st.markdown("<div style='padding-top: 28px;'></div>", unsafe_allow_html=True)
        if st.button("➕ Create New", type="primary", use_container_width=True):
            if nama_baru.strip():
                # Cek duplikasi nama di folder aktif saat ini
                nama_kembar = any(c.nama.lower() == nama_baru.strip().lower() for c in folder_sekarang.children)
                
                if not nama_kembar:
                    is_f = True if jenis_baru == "Folder" else False
                    # Tambahkan node baru ke dalam anak folder aktif
                    folder_sekarang.add_child(FileNode(nama_baru.strip(), is_folder=is_f, ukuran_kb=ukuran_baru))
                    
                    # Trik membersihkan form input: Hapus state key agar input teks kosong kembali
                    st.session_state.input_nama_baru = ""
                    st.success(f"Sukses membuat {jenis_baru}!")
                    st.rerun()
                else:
                    st.error("Nama sudah ada!")
            else:
                st.warning("Nama wajib diisi!")

st.write(" ")

# --- BAGIAN B: WINDOWS ADDRESS BAR & BOX PENCARIAN (SEARCH) ---
col_up_btn, col_address_bar, col_search_box = st.columns([1, 8, 3])

with col_up_btn:
    # Tombol panah kembali ke atas (Up Level)
    if folder_sekarang.parent is not None:
        if st.button("⬆️ Up", use_container_width=True):
            st.session_state.current_folder_path = folder_sekarang.parent.dapatkan_path_lengkap()
            st.rerun()
    else:
        st.button("⬆️ Up", disabled=True, use_container_width=True)

with col_address_bar:
    # Menampilkan jalur folder secara dinamis (Contoh: This PC -> Local Disk (C:) -> Documents)
    jalur_list = []
    temp = folder_sekarang
    while temp is not None:
        jalur_list.insert(0, temp.nama)
        temp = temp.parent
    breadcrumb_str = " 💻 This PC  ➔  " + "  ➔  ".join(jalur_list)
    st.text_input("Address", value=breadcrumb_str, disabled=True, label_visibility="collapsed")

with col_search_box:
    # Kotak Pencarian Aktif (Diberikan key spesifik agar reaktif saat diketik)
    kueri_cari = st.text_input("🔍 Search", placeholder="Search in this folder...", label_visibility="collapsed", key="search_query")

st.write("---")


# --- BAGIAN C: PEMBAGIAN PANEL UTAMA (SIDEBAR KIRI & ISI KANAN) ---

# 1. Mengisi Panel Navigasi di Sidebar Kiri Resmi Streamlit
st.sidebar.markdown("### 🖥️ Navigation Pane")
if st.sidebar.button("💻 This PC (Go to Root)", use_container_width=True):
    st.session_state.current_folder_path = root_master.dapatkan_path_lengkap()
    st.rerun()
st.sidebar.markdown("---")

# Memanggil fungsi rekursif untuk merender seluruh isi folder secara bertingkat di sidebar
render_sidebar_tree(root_master)


# 2. Tampilan Isi Folder di Sebelah Kanan (Panel Utama)
st.markdown(f"## 📂 {folder_sekarang.nama}")

# Logika filter pencarian berdasarkan teks input user
if kueri_cari.strip():
    daftar_tampil = [item for item in folder_sekarang.children if kueri_cari.lower() in item.nama.lower()]
else:
    daftar_tampil = folder_sekarang.children

if not daftar_tampil:
    st.info("Folder ini kosong atau item tidak ditemukan.")
else:
    # Mengatur sistem grid 3 kolom menyamping di panel utama
    kolom_grid = st.columns(3)
    
    for urutan, objek in enumerate(daftar_tampil):
        pilihan_kolom = kolom_grid[urutan % 3]
        
        with pilihan_kolom:
            with st.container(border=True):
                col_icon, col_action = st.columns([1, 4])
                
                with col_icon:
                    if objek.is_folder:
                        st.write("### 📁")
                    else:
                        st.write("### 📄")
                        
                with col_action:
                    st.markdown(f"**{objek.nama}**")
                    if objek.is_folder:
                        st.caption("Folder")
                        # Tombol navigasi masuk ke dalam folder
                        if st.button("Open", key=f"main_open_{objek.nama}_{urutan}", use_container_width=True):
                            st.session_state.current_folder_path = objek.dapatkan_path_lengkap()
                            st.rerun()
                    else:
                        st.caption(f"File ({objek.ukuran} KB)")
                    
                    # Ditambahkan tombol hapus item langsung di masing-masing item (Windows Action yang ideal)
                    if st.button("🗑️ Delete", key=f"main_del_{objek.nama}_{urutan}", use_container_width=True, type="secondary"):
                        folder_sekarang.children.remove(objek)
                        st.success(f"{objek.nama} berhasil dihapus!")
                        st.rerun()
