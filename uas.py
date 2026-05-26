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
        self.parent = None  # Menyimpan induk untuk memudahkan navigasi tombol "Up/Back"

    def add_child(self, child_node):
        """Menambahkan cabang baru (Insertion)"""
        child_node.parent = self
        self.children.append(child_node)
  
    def cari_node(self, target_nama):
        """Mencari node spesifik berdasarkan nama (Case Insensitive)"""
        if self.nama.lower() == target_nama.lower():
            return self
        
        for sub in self.children:
            hasil = sub.cari_node(target_nama)
            if hasil:
                return hasil   
        return None

    def hitung_total_ukuran(self):
        """Menghitung ukuran folder secara rekursif berdasarkan file di dalamnya"""
        if not self.is_folder:
            return self.ukuran
        total = 0
        for sub in self.children:
            total += sub.hitung_total_ukuran()
        return total


# ====================================================================
# 2. INSIALISASI DRIVE DATA (MIMIC WINDOWS DRIVE)
# ====================================================================
st.set_page_config(page_title="Windows File Explorer", page_icon="💻", layout="wide")

# Mengunci data agar tidak hilang saat user melakukan klik-klik di web
if 'root' not in st.session_state:
    # Membuat Drive Utama (This PC / Local Disk C)
    root = FileNode("Local Disk (C:)", is_folder=True)
    
    # Membuat Folder Bawaan Windows
    documents = FileNode("Documents", is_folder=True)
    pictures = FileNode("Pictures", is_folder=True)
    downloads = FileNode("Downloads", is_folder=True)
    
    root.add_child(documents)
    root.add_child(pictures)
    root.add_child(downloads)
    
    # Mengisi file tiruan di dalam folder
    documents.add_child(FileNode("Tugas_Struktur_Data.pdf", is_folder=False, ukuran_kb=150))
    documents.add_child(FileNode("Catatan_Kuliah.txt", is_folder=False, ukuran_kb=45))
    pictures.add_child(FileNode("Foto_Bersama_Damar.png", is_folder=False, ukuran_kb=820))
    downloads.add_child(FileNode("installer_python.exe", is_folder=False, ukuran_kb=1024))
    
    st.session_state.root = root

# Pointer untuk melacak "Di folder mana posisi user sekarang di Windows"
if 'current_folder' not in st.session_state:
    st.session_state.current_folder = st.session_state.root


# ====================================================================
# 3. FUNGSI PEMBANTU (NAVIGASI)
# ====================================================================
def dapatkan_breadcrumb(node):
    """Membuat teks jalur alamat di bagian atas seperti di Windows"""
    jalur = []
    sementara = node
    while sementara is not None:
        jalur.insert(0, sementara.nama)
        sementara = sementara.parent
    return " 📁 This PC > " + " > ".join(jalur)

def render_sidebar_tree(node, depth=0):
    """Mencetak struktur pohon folder di panel navigasi kiri"""
    indentasi = "    " * depth
    if node.is_folder:
        # Menampilkan nama folder di sidebar sebagai tombol navigasi cepat
        if st.sidebar.button(f"{indentasi}📁 {node.nama}", key=f"side_{node.nama}_{depth}", use_container_width=True):
            st.session_state.current_folder = node
            st.rerun()
        for child in node.children:
            render_sidebar_tree(child, depth + 1)


# ====================================================================
# 4. TAMPILAN ANTARMUKA TAMPILAN WINDOWS EXPLORER
# ====================================================================

# --- BAGIAN A: WINDOWS ADDRESS BAR & NAVIGATION BUTTONS ---
col_back, col_address, col_search = st.columns([1, 8, 3])

with col_back:
    # Tombol panah atas untuk naik ke folder induk (Up One Level)
    if st.session_state.current_folder.parent is not None:
        if st.button("⬆️ Up", use_container_width=True):
            st.session_state.current_folder = st.session_state.current_folder.parent
            st.rerun()
    else:
        st.button("⬆️ Up", disabled=True, use_container_width=True)

with col_address:
    # Menampilkan address bar kotak abu-abu khas Windows
    st.text_input("Address Bar", value=dapatkan_breadcrumb(st.session_state.current_folder), disabled=True, label_visibility="collapsed")

with col_search:
    # Kotak pencarian di pojok kanan atas
    kueri = st.text_input("🔍 Search folder...", placeholder="Search...", label_visibility="collapsed")

st.markdown("---")


# --- BAGIAN B: MEMBAGI LAYAR UTAMA (SIDEBAR KIRI & GRID KANAN) ---
sidebar_kiri, panel_utama = st.columns([3, 9], gap="medium")

# 1. SIDEBAR KIRI (Navigation Pane)
with sidebar_kiri:
    st.markdown("### 🖥️ Navigation Pane")
    if st.sidebar.button("💻 This PC (Go to Root)", use_container_width=True):
        st.session_state.current_folder = st.session_state.root
        st.rerun()
    st.sidebar.markdown("---")
    render_sidebar_tree(st.session_state.root)

# 2. PANEL UTAMA (Folder Contents View - Grid System)
with panel_utama:
    folder_aktif = st.session_state.current_folder
    st.markdown(f"## 📂 {folder_aktif.nama}")
    st.caption(f"Total kapasitas item di folder ini: {folder_aktif.hitung_total_ukuran()} KB")
    st.write(" ")

    # Jika folder kosong
    if not folder_aktif.children:
        st.info("This folder is empty.")
    else:
        # Jika ada kueri pencarian, saring itemnya
        if kueri.strip():
            items_to_show = [c for c in folder_aktif.children if kueri.lower() in c.nama.lower()]
        else:
            items_to_show = folder_aktif.children

        # MEMBUAT TAMPILAN GRID IKON (Khas Windows Large Icons)
        # Kita buat 4 kolom menyamping
        kolom_grid = st.columns(4)
        
        for index, item in enumerate(items_to_show):
            # Bergantian menaruh item di kolom 1, 2, 3, 4
            target_kolom = kolom_grid[index % 4]
            
            with target_kolom:
                # Menggunakan container kotak untuk membungkus ikon berkas
                with st.container(border=True):
                    if item.is_folder:
                        st.write("### 📁")
                        st.markdown(f"**{item.nama}**")
                        st.caption("Folder")
                        # Tombol "Double Click" ceritanya diganti tombol Open
                        if st.button("Open", key=f"open_panel_{item.nama}"):
                            st.session_state.current_folder = item
                            st.rerun()
                    else:
                        st.write("### 📄")
                        st.markdown(f"*{item.nama}*")
                        st.caption(f"File ({item.ukuran} KB)")
                        st.button("Properties", key=f"prop_{item.nama}", disabled=True)


# --- BAGIAN C: CONTEXT MENU DI BAGIAN BAWAH (Untuk Operasi Tambah/Hapus) ---
st.markdown("---")
st.markdown("### 🛠️ Windows Actions (New Folder / New File / Delete)")

tab_new, tab_delete = st.tabs(["✨ New Item", "🗑️ Delete Item"])

with tab_new:
    col_tipe, col_nama, col_size, col_btn = st.columns([2, 4, 2, 2])
    with col_tipe:
        jenis = st.selectbox("Type:", ["Folder", "File"], label_visibility="visible")
    with col_nama:
        nama_baru = st.text_input("Item Name:", placeholder="e.g. Tugas_Akhir", key="new_name")
    with col_size:
        if jenis == "File":
            size_kb = st.number_input("Size (KB):", min_value=1, max_value=5000, value=10)
        else:
            size_kb = 0
    with col_btn:
        st.write(" ") # Penyeimbang spasi vertikal
        st.write(" ") 
        if st.button("➕ Create", type="primary", use_container_width=True):
            if nama_baru.strip():
                # Cek nama kembar
                kembar = any(c.nama.lower() == nama_baru.strip().lower() for c in folder_aktif.children)
                if not kembar:
                    is_f = True if jenis == "Folder" else False
                    folder_aktif.add_child(FileNode(nama_baru.strip(), is_folder=is_f, ukuran_kb=size_kb))
                    st.success(f"Created {jenis} successfully!")
                    st.rerun()
                else:
                    st.error("Name already exists!")
            else:
                st.warning("Name cannot be empty!")

with tab_delete:
    if not folder_aktif.children:
        st.write("No items to delete in this folder.")
    else:
        col_sel, col_del_btn = st.columns([8, 4])
        with col_sel:
            target_hapus = st.selectbox("Select item to delete:", [c.nama for c in folder_aktif.children])
        with col_del_btn:
            st.write(" ")
            st.write(" ")
            if st.button("💥 Delete Permanently", type="secondary", use_container_width=True):
                node_hapus = next((c for c in folder_aktif.children if c.nama == target_hapus), None)
                if node_hapus:
                    folder_aktif.children.remove(node_hapus)
                    st.success(f"Deleted '{target_hapus}' successfully!")
                    st.rerun()
