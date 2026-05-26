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
        child_node.parent = self
        self.children.append(child_node)
  
    def cari_node(self, target_nama):
        if self.nama.lower() == target_nama.lower():
            return self
        for sub in self.children:
            hasil = sub.cari_node(target_nama)
            if hasil:
                return hasil   
        return None

    def hitung_total_ukuran(self):
        if not self.is_folder:
            return self.ukuran
        total = 0
        for sub in self.children:
            total += sub.hitung_total_ukuran()
        return total


# ====================================================================
# 2. INSIALISASI DRIVE DATA & CONFIG
# ====================================================================
st.set_page_config(page_title="File Explorer", page_icon="💻", layout="wide")

# --- CUSTOM CSS UNTUK STYLE ALA WINDOWS DEKTOP ---
st.markdown("""
    <style>
        /* Mengatur warna background utama & font modern */
        .stApp {
            background-color: #f3f3f3;
        }
        
        /* Gaya bar alamat (Address Bar) */
        .address-bar {
            background-color: #ffffff;
            border: 1px solid #d1d1d1;
            padding: 6px 12px;
            border-radius: 4px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 14px;
            color: #333333;
            display: flex;
            align-items: center;
        }
        
        /* Mengatur style teks agar tidak terlalu mencolok di grid */
        .file-label {
            font-family: 'Segoe UI', sans-serif;
            font-size: 13px;
            font-weight: 500;
            text-align: center;
            margin-top: 5px;
            text-overflow: ellipsis;
            overflow: hidden;
            white-space: nowrap;
        }
        
        /* Mengurangi margin bawaan streamlit agar layout lebih padat/compact */
        .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 1rem !important;
        }
    </style>
""", unsafe_allow_html=True)

# Inisialisasi Root Data
if 'root' not in st.session_state:
    root = FileNode("Local Disk (C:)", is_folder=True)
    
    documents = FileNode("Documents", is_folder=True)
    pictures = FileNode("Pictures", is_folder=True)
    downloads = FileNode("Downloads", is_folder=True)
    
    root.add_child(documents)
    root.add_child(pictures)
    root.add_child(downloads)
    
    documents.add_child(FileNode("Tugas_Struktur_Data.pdf", is_folder=False, ukuran_kb=150))
    documents.add_child(FileNode("Catatan_Kuliah.txt", is_folder=False, ukuran_kb=45))
    pictures.add_child(FileNode("Foto_Bersama_Damar.png", is_folder=False, ukuran_kb=820))
    downloads.add_child(FileNode("installer_python.exe", is_folder=False, ukuran_kb=1024))
    
    st.session_state.root = root

if 'current_folder' not in st.session_state:
    st.session_state.current_folder = st.session_state.root


# ====================================================================
# 3. FUNGSI PEMBANTU (NAVIGASI)
# ====================================================================
def dapatkan_breadcrumb(node):
    jalur = []
    sementara = node
    while sementara is not None:
        jalur.insert(0, sementara.nama)
        sementara = sementara.parent
    return " This PC > " + " > ".join(jalur)

def render_sidebar_tree(node, depth=0):
    """Mencetak struktur pohon di Sidebar bawaan dengan rapi"""
    indentasi = "    " * depth
    if node.is_folder:
        # Tombol navigasi kiri menggunakan minimal style agar mirip list direktori asli
        if st.sidebar.button(f"{indentasi}📁 {node.nama}", key=f"side_{node.nama}_{depth}", use_container_width=True):
            st.session_state.current_folder = node
            st.rerun()
        for child in node.children:
            render_sidebar_tree(child, depth + 1)


# ====================================================================
# 4. TAMPILAN ANTARMUKA (WINDOWS INTERFACE)
# ====================================================================

# --- REORGANISASI SIDEBAR ASLI ---
with st.sidebar:
    st.markdown("### 🖥️ Navigation Pane")
    if st.button("💻 This PC", use_container_width=True, type="secondary"):
        st.session_state.current_folder = st.session_state.root
        st.rerun()
    st.markdown("---")
    render_sidebar_tree(st.session_state.root)

# --- BAGIAN UTAMA: TOOLBAR & ADDRESS BAR ---
# Membuat layout bar atas yang sejajar dan fungsional
col_back, col_address, col_search = st.columns([1.2, 7.8, 3])

with col_back:
    if st.session_state.current_folder.parent is not None:
        if st.button("⬅️ Back", use_container_width=True):
            st.session_state.current_folder = st.session_state.current_folder.parent
            st.rerun()
    else:
        st.button("⬅️ Back", disabled=True, use_container_width=True)

with col_address:
    # Menggunakan HTML injection untuk membuat kotak alamat abu-abu khas Windows
    st.markdown(
        f'<div class="address-bar">📍 {dapatkan_breadcrumb(st.session_state.current_folder)}</div>', 
        unsafe_allow_html=True
    )

with col_search:
    kueri = st.text_input("Search", placeholder="🔍 Search in current folder...", label_visibility="collapsed")

st.markdown("---")

# --- CONTAINER KONTEN UTAMA ---
folder_aktif = st.session_state.current_folder

# Bar Status Informasi Folder
col_info_nama, col_info_size = st.columns([8, 4])
with col_info_nama:
    st.markdown(f"### 📂 {folder_aktif.nama}")
with col_info_size:
    total_mb = folder_aktif.hitung_total_ukuran() / 1024
    st.markdown(f"<p style='text-align: right; color: gray; font-size: 14px; margin-top:10px;'>Size: {folder_aktif.hitung_total_ukuran()} KB (~{total_mb:.2f} MB)</p>", unsafe_allow_html=True)

# Membaca daftar file/folder
if not folder_aktif.children:
    st.info("Folder ini kosong.")
else:
    if kueri.strip():
        items_to_show = [c for c in folder_aktif.children if kueri.lower() in c.nama.lower()]
    else:
        items_to_show = folder_aktif.children

    # TAMPILAN GRID IKON (Ditingkatkan agar simetris & interaktif)
    # 5 Kolom agar muat lebih banyak item layaknya resolusi monitor PC
    kolom_grid = st.columns(5)
    
    for index, item in enumerate(items_to_show):
        target_kolom = kolom_grid[index % 5]
        
        with target_kolom:
            # Menggunakan komponen container border bawaan Streamlit versi baru sebagai 'Card'
            with st.container(border=True):
                if item.is_folder:
                    # Menyelaraskan konten di tengah kontainer berkas
                    st.markdown("<p style='text-align: center; font-size: 40px; margin-bottom: 0px;'>📁</p>", unsafe_allow_html=True)
                    st.markdown(f'<div class="file-label">{item.nama}</div>', unsafe_allow_html=True)
                    st.markdown("<p style='text-align: center; color: gray; font-size: 11px;'>File Folder</p>", unsafe_allow_html=True)
                    
                    # Tombol aksi dibuat penuh mengikuti lebar grid box
                    if st.button("Open", key=f"btn_{item.nama}_{index}", use_container_width=True, type="primary"):
                        st.session_state.current_folder = item
                        st.rerun()
                else:
                    # Penentuan warna/ekstensi ikon biar lebih detail
                    icon_file = "📄"
                    if item.nama.endswith('.pdf'): icon_file = "📕"
                    elif item.nama.endswith('.png') or item.nama.endswith('.jpg'): icon_file = "🖼️"
                    elif item.nama.endswith('.exe'): icon_file = "⚙️"
                    
                    st.markdown(f"<p style='text-align: center; font-size: 40px; margin-bottom: 0px;'>{icon_file}</p>", unsafe_allow_html=True)
                    st.markdown(f'<div class="file-label">{item.nama}</div>', unsafe_allow_html=True)
                    st.markdown(f"<p style='text-align: center; color: gray; font-size: 11px;'>{item.ukuran} KB</p>", unsafe_allow_html=True)
                    
                    # Tombol info untuk file biasa
                    if st.button("Details", key=f"btn_{item.nama}_{index}", use_container_width=True):
                        st.toast(f"ℹ️ {item.nama} ({item.ukuran} KB)", icon="📝")

# --- OPERASI MANAJEMEN BERKAS (CONTEXT MENU DI BAWAH) ---
st.markdown("<br><br>", unsafe_allow_html=True)
expander_aksi = st.expander("🛠️ Folder Tools (New Item / Delete Item)", expanded=False)

with expander_aksi:
    tab_new, tab_delete = st.tabs(["✨ Create New", "🗑️ Delete Content"])
    
    with tab_new:
        col_tipe, col_nama, col_size, col_btn = st.columns([2, 4, 2, 2])
        with col_tipe:
            jenis = st.selectbox("Item Type:", ["Folder", "File"], key="add_type")
        with col_nama:
            nama_baru = st.text_input("Name:", placeholder="Input item name...", key="new_name")
        with col_size:
            if jenis == "File":
                size_kb = st.number_input("Size (KB):", min_value=1, max_value=50000, value=100)
            else:
                size_kb = 0
        with col_btn:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Create", type="primary", use_container_width=True):
                if nama_baru.strip():
                    kembar = any(c.nama.lower() == nama_baru.strip().lower() for c in folder_aktif.children)
                    if not kembar:
                        is_f = True if jenis == "Folder" else False
                        folder_aktif.add_child(FileNode(nama_baru.strip(), is_folder=is_f, ukuran_kb=size_kb))
                        st.success(f"Berhasil membuat {jenis}!")
                        st.rerun()
                    else:
                        st.error("Nama sudah digunakan di folder ini!")
                else:
                    st.warning("Nama tidak boleh kosong!")

    with tab_delete:
        if not folder_aktif.children:
            st.write("Tidak ada item yang dapat dihapus.")
        else:
            col_sel, col_del_btn = st.columns([8, 4])
            with col_sel:
                target_hapus = st.selectbox("Pilih item yang ingin dihapus:", [c.nama for c in folder_aktif.children])
            with col_del_btn:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🗑️ Delete Permanently", type="secondary", use_container_width=True):
                    node_hapus = next((c for c in folder_aktif.children if c.nama == target_hapus), None)
                    if node_hapus:
                        folder_aktif.children.remove(node_hapus)
                        st.success(f"'{target_hapus}' berhasil dihapus!")
                        st.rerun()
