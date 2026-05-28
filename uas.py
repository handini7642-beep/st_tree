import streamlit as st

# Mengatur konfigurasi halaman agar terlihat luas dan modern
st.set_page_config(page_title="Advanced File Explorer", layout="wide", page_icon="📁")

# ====================================================================
# 1. STRUKTUR DATA: NODE UNTUK GENERAL TREE (ENHANCED)
# ====================================================================
class TreeNode:
    def __init__(self, data, is_folder=True):
        self.data = data
        self.is_folder = is_folder  
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
        """Menampilkan visualisasi pohon teks"""
        if node is None:
            node = self.root
        ikon = "📁 " if node.is_folder else dapatkan_ikon_file(node.data)
        st.code("   " * level + f"└── {ikon}{node.data}", language="")
        for child in node.children:
            self.display_streamlit(child, level + 1)

    def cari_global(self, keyword, node=None, hasil=None):
        """Mencari file/folder di seluruh pohon (DFS)"""
        if node is None:
            node = self.root
            hasil = []
        
        if keyword.lower() in node.data.lower() and node != self.root:
            hasil.append(node)
            
        for child in node.children:
            self.cari_global(keyword, child, hasil)
        return hasil

    def hitung_statistik(self, node=None, stats=None):
        """Menghitung total folder dan file secara rekursif"""
        if node is None:
            node = self.root
            stats = {"folder": 0, "file": 0}
            
        if node != self.root:
            if node.is_folder:
                stats["folder"] += 1
            else:
                stats["file"] += 1
                
        for child in node.children:
            self.hitung_statistik(child, stats)
        return stats


# ====================================================================
# 2. FUNGSI PEMBANTU (UTILITIES)
# ====================================================================
def dapatkan_ikon_file(nama_file):
    """Memberikan ikon dinamis berdasarkan ekstensi file"""
    if "." in nama_file:
        ekstensi = nama_file.split(".")[-1].lower()
        if ekstensi in ["pdf"]: return "📕 "
        if ekstensi in ["txt", "docx", "doc"]: return "📄 "
        if ekstensi in ["jpg", "jpeg", "png", "gif"]: return "🖼️ "
        if ekstensi in ["mp4", "mkv", "avi"]: return "🎬 "
        if ekstensi in ["mp3", "wav"]: return "🎵 "
        if ekstensi in ["zip", "rar"]: return "📦 "
    return "📝 "


def dapatkan_path_list(node):
    """Mengembalikan list of nodes dari Root sampai node saat ini untuk Breadcrumbs"""
    path = []
    sementara = node
    while sementara is not None:
        path.insert(0, sementara)
        sementara = sementara.parent
    return path


# ====================================================================
# 3. INISIALISASI SESSION STATE
# ====================================================================
if "sistem_file" not in st.session_state:
    sistem_file = GeneralTree("Root")
    
    # Seeding data tiruan agar terlihat ramai seperti storage asli
    dokumen = TreeNode("Dokumen Kuliah", is_folder=True)
    foto = TreeNode("Foto_Ekskul", is_folder=True)
    hiburan = TreeNode("Hiburan", is_folder=True)
    
    sistem_file.root.add_child(dokumen)
    sistem_file.root.add_child(foto)
    sistem_file.root.add_child(hiburan)

    dokumen.add_child(TreeNode("Tugas_Struktur_Data.pdf", is_folder=False))
    dokumen.add_child(TreeNode("Catatan_Algoritma.txt", is_folder=False))
    foto.add_child(TreeNode("Pentas_Seni.jpg", is_folder=False))
    hiburan.add_child(TreeNode("Lagu_Favorit.mp3", is_folder=False))
    
    st.session_state.sistem_file = sistem_file
    st.session_state.current_node = sistem_file.root


# ====================================================================
# 4. ANTARMUKA UTAMA (STREAMLIT UI)
# ====================================================================
st.title("🗂️ Next-Gen File Explorer")
st.caption("Simulasi Manajemen Penyimpanan Berbasis Struktur Data General Tree")
st.markdown("---")

# --- SIDEBAR: DASHBOARD STATISTIK & VISUALISASI TREE ---
with st.sidebar:
    st.header("📊 Ringkasan Storage")
    stats = st.session_state.sistem_file.hitung_statistik()
    
    col_stat1, col_stat2 = st.columns(2)
    col_stat1.metric("Total Folder", f"{stats['folder']} 📁")
    col_stat2.metric("Total File", f"{stats['file']} 📄")
    
    st.markdown("---")
    st.header("🔍 Pencarian Global")
    kata_kunci = st.text_input("Cari nama file/folder...", placeholder="Ketik lalu enter...")
    
    if kata_kunci:
        hasil_cari = st.session_state.sistem_file.cari_global(kata_kunci)
        if hasil_cari:
            st.success(f"Ditemukan {len(hasil_cari)} item:")
            for item in hasil_cari:
                tipe_str = "Folder" if item.is_folder else "File"
                if st.button(f"Go to: {item.data} ({tipe_str})", key=f"search_{item.data}_{id(item)}"):
                    st.session_state.current_node = item if item.is_folder else item.parent
                    st.rerun()
        else:
            st.error("Item tidak ditemukan.")
            
    st.markdown("---")
    st.header("🌳 Struktur Pohon")
    with st.expander("Lihat Hierarki Penuh", expanded=False):
        st.session_state.sistem_file.display_streamlit()


# --- AREA UTAMA: BREADCRUMBS NAVIGASI ---
# Membuat sistem navigasi klik jalur seperti di Windows Explorer asli
b_nodes = dapatkan_path_list(st.session_state.current_node)
cols_b = st.columns(len(b_nodes) * 2 - 1)

idx_col = 0
for i, node in enumerate(b_nodes):
    # Tombol untuk setiap folder di dalam jalur path
    if cols_b[idx_col].button(node.data, key=f"breadcrumb_{node.data}_{i}"):
        st.session_state.current_node = node
        st.rerun()
    idx_col += 1
    # Pembatas tanda panah antar folder
    if idx_col < len(cols_b):
        cols_b[idx_col].write("▶️")
        idx_col += 1

st.markdown(" ")

# --- LAYOUT KONTEN UTAMA ---
kolom_files, kolom_aksi = st.columns([2, 1])

with kolom_files:
    st.subheader("📄 Berkas di Folder Ini")
    
    # Tombol Kembali ke Atas
    if st.session_state.current_node.parent is not None:
        if st.button("⬅️ Kembali", use_container_width=True):
            st.session_state.current_node = st.session_state.current_node.parent
            st.rerun()
            
    children_nodes = st.session_state.current_node.children
    if len(children_nodes) == 0:
        st.info("ℹ️ Folder ini kosong. Silahtan tambah folder atau file baru di menu sebelah kanan.")
    else:
        # Menampilkan item dalam bentuk baris tabel yang rapi
        for child in children_nodes:
            ikon = "📁 " if child.is_folder else dapatkan_ikon_file(child.data)
            tipe_label = "Folder" if child.is_folder else "Berkas File"
            
            # Membuat container baris bergaya modern
            with st.container(border=True):
                c1, c2, c3 = st.columns([3, 1, 1])
                c1.markdown(f"### {ikon} {child.data}")
                c2.caption(f"Tipe: {tipe_label}")
                
                with c3:
                    if child.is_folder:
                        if st.button("Buka 📂", key=f"buka_{child.data}", use_container_width=True):
                            st.session_state.current_node = child
                            st.rerun()
                    else:
                        st.button("Unduh 📥", key=f"unduh_{child.data}", use_container_width=True, disabled=True, help="Simulasi unduhan file.")

with kolom_aksi:
    st.subheader("🛠️ Manajemen")
    
    tab_tambah, tab_ubah, tab_hapus = st.tabs(["➕ Tambah", "✏️ Ubah Nama", "🗑️ Hapus"])
    
    # 1. TAB TAMBAH ITEM
    with tab_tambah:
        nama_baru = st.text_input("Nama Item:", key="add_name", placeholder="Contoh: Tugas_Akhir.pdf").strip()
        tipe = st.radio("Jenis Komponen:", ("Folder", "File"), horizontal=True)
        
        if st.button("Buat Baru", type="primary", use_container_width=True):
            if not nama_baru:
                st.error("Nama tidak boleh kosong!")
            elif any(c.data.lower() == nama_baru.lower() for c in st.session_state.current_node.children):
                st.error("Nama sudah digunakan di folder ini!")
            else:
                is_folder_bool = (tipe == "Folder")
                st.session_state.current_node.add_child(TreeNode(nama_baru, is_folder=is_folder_bool))
                st.success(f"Berhasil menambahkan {tipe.lower()} '{nama_baru}'")
                st.rerun()

    # 2. TAB UBAH NAMA (RENAME)
    with tab_ubah:
        if len(st.session_state.current_node.children) == 0:
            st.caption("Tidak ada item untuk diubah namanya.")
        else:
            opsi_ubah = [c.data for c in st.session_state.current_node.children]
            target_ubah = st.selectbox("Pilih item:", opsi_ubah, key="select_rename")
            nama_ganti = st.text_input("Nama Baru:", key="input_rename").strip()
            
            if st.button("Simpan Perubahan", use_container_width=True):
                if not nama_ganti:
                    st.error("Nama baru tidak boleh kosong.")
                elif any(c.data.lower() == nama_ganti.lower() for c in st.session_state.current_node.children):
                    st.error("Nama tersebut sudah terpakai di folder ini.")
                else:
                    for child in st.session_state.current_node.children:
                        if child.data == target_ubah:
                            child.data = nama_ganti
                            st.success("Nama berhasil diubah!")
                            st.rerun()

    # 3. TAB HAPUS ITEM
    with tab_hapus:
        if len(st.session_state.current_node.children) == 0:
            st.caption("Tidak ada item untuk dihapus.")
        else:
            opsi_hapus = [c.data for c in st.session_state.current_node.children]
            target_hapus = st.selectbox("Pilih item yang ingin dibuang:", opsi_hapus, key="select_delete")
            
            if st.button("Hapus Item", type="primary", use_container_width=True):
                for child in st.session_state.current_node.children:
                    if child.data == target_hapus:
                        st.session_state.current_node.remove_child(child)
                        st.warning(f"'{target_hapus}' telah dihapus.")
                        st.rerun()
