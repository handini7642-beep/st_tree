import streamlit as st

# ====================================================================
# 1. STRUKTUR DATA: NODE UNTUK GENERAL TREE (SESUAI BLUEPRINT)
# ====================================================================
class TreeNode:
    """Node untuk General Tree"""
    def __init__(self, data, is_folder=True):
        self.data = data
        self.is_folder = is_folder  # True untuk Folder, False untuk File
        self.children = []          # List of children nodes
        self.parent = None          # Untuk memudahkan menu "Kembali"

    def add_child(self, child_node):
        child_node.parent = self    # Catat siapa folder induknya
        self.children.append(child_node)

    def __str__(self):
        return self.data if isinstance(self.data, str) else str(self.data)


class GeneralTree:
    """Implementasi General Tree"""
    def __init__(self, root_data):
        self.root = TreeNode(root_data, is_folder=True)

    def display_streamlit(self, node=None, level=0):
        """Menampilkan tree secara hierarkis dalam format teks Streamlit"""
        if node is None:
            node = self.root

        ikon = "📁 " if node.is_folder else "📄 "
        # Menggunakan format code block agar indentasi spasi terlihat rapi
        st.code("   " * level + f"└── {ikon}{node.data}", language="")
        
        for child in node.children:
            self.display_streamlit(child, level + 1)

    def dfs_traversal(self, node=None, visited=None):
        """Depth First Search traversal"""
        if node is None:
            node = self.root
            visited = []

        visited.append(node.data)
        for child in node.children:
            self.dfs_traversal(child, visited)

        return visited


# ====================================================================
# 2. INISIALISASI STATE (STREAMLIT SESSION STATE)
# ====================================================================
# Streamlit butuh session_state agar data tidak ter-reset saat web di-refresh/diklik
if "sistem_file" not in st.session_state:
    # Seeding Data Awal jika belum ada di session
    sistem_file = GeneralTree("Root")
    
    dokumen = TreeNode("Dokumen Kuliah", is_folder=True)
    foto = TreeNode("Foto_Ekskul", is_folder=True)
    sistem_file.root.add_child(dokumen)
    sistem_file.root.add_child(foto)

    dokumen.add_child(TreeNode("Tugas_Struktur_Data.pdf", is_folder=False))
    dokumen.add_child(TreeNode("Catatan_Algoritma.txt", is_folder=False))
    
    st.session_state.sistem_file = sistem_file
    st.session_state.current_node = sistem_file.root


# Fungsi pembantu untuk melacak jalan dari folder saat ini ke atas sampai Root
def dapatkan_path_string(node):
    path = []
    sementara = node
    while sementara is not None:
        path.insert(0, sementara.data)
        sementara = sementara.parent
    return " / ".join(path) + " /"


# ====================================================================
# 3. ANTARMUKA UTAMA (STREAMLIT UI)
# ====================================================================
st.title("📂 Antarmuka File Explorer (General Tree)")
st.write("Aplikasi simulasi struktur data pohon bebas (*General Tree*) untuk manajemen berkas.")

# Menampilkan Lokasi Sekarang
current_path = dapatkan_path_string(st.session_state.current_node)
st.info(f"**📍 LOKASI SEKARANG:** `{current_path}`")

# Membuat layout 2 Kolom untuk membagi Manajemen Berkas dan Visualisasi Tree
kolom_kiri, kolom_kanan = st.columns([1.2, 1])

with kolom_kiri:
    st.subheader("📁 Isi Direktori Saat Ini")
    
    # Tombol Kembali ke Folder Sebelumnya (Hanya muncul jika bukan di Root)
    if st.session_state.current_node.parent is not None:
        if st.button("⬅️ Kembali ke Folder Sebelumnya"):
            st.session_state.current_node = st.session_state.current_node.parent
            st.rerun()
            
    # Tampilkan isi dari folder aktif saat ini
    children_nodes = st.session_state.current_node.children
    if len(children_nodes) == 0:
        st.caption("*(Folder ini kosong)*")
    else:
        for child in children_nodes:
            ikon = "📁 [Folder]" if child.is_folder else "📄 [File]"
            
            col_item, col_aksi = st.columns([3, 1])
            with col_item:
                st.write(f"{ikon} **{child.data}**")
            with col_aksi:
                # Jika item adalah folder, beri tombol untuk Masuk/Buka
                if child.is_folder:
                    if st.button("Buka", key=f"open_{child.data}"):
                        st.session_state.current_node = child
                        st.rerun()

    st.markdown("---")
    
    # Operasi Tambah Baru & Hapus
    st.subheader("🛠️ Operasi Direktori")
    tab1, tab2 = st.tabs(["➕ Buat Baru", "🗑️ Hapus Item"])
    
    with tab1:
        nama_baru = st.text_input("Nama Item Baru:", key="input_nama_baru").strip()
        tipe = st.radio("Tipe Item:", ("Folder", "File"), horizontal=True)
        
        if st.button("Tambah"):
            if nama_baru == "":
                st.error("Nama tidak boleh kosong.")
            else:
                # Validasi nama kembar
                nama_kembar = any(child.data.lower() == nama_baru.lower() for child in st.session_state.current_node.children)
                
                if nama_kembar:
                    st.error(f"Nama '{nama_baru}' sudah digunakan di folder ini.")
                else:
                    is_folder_bool = True if tipe == "Folder" else False
                    st.session_state.current_node.add_child(TreeNode(nama_baru, is_folder=is_folder_bool))
                    st.success(f"Berhasil membuat {tipe.lower()} '{nama_baru}'")
                    st.rerun()
                    
    with tab2:
        if len(st.session_state.current_node.children) == 0:
            st.write("Tidak ada item untuk dihapus.")
        else:
            # Dropdown untuk memilih item yang ingin dihapus
            opsi_hapus = [child.data for child in st.session_state.current_node.children]
            target_hapus = st.selectbox("Pilih item yang ingin dihapus:", opsi_hapus)
            
            if st.button("Hapus Permanen", type="primary"):
                for child in st.session_state.current_node.children:
                    if child.data == target_hapus:
                        st.session_state.current_node.children.remove(child)
                        st.warning(f"'{target_hapus}' berhasil dihapus.")
                        st.rerun()

with kolom_kanan:
    st.subheader("🌳 Visualisasi Pohon & DFS")
    
    with st.expander("👀 Lihat Seluruh Struktur Pohon (Rekursif)", expanded=True):
        st.session_state.sistem_file.display_streamlit()
        
    with st.expander("⏱️ Hasil Penelusuran Algoritma DFS"):
        riwayat_dfs = st.session_state.sistem_file.dfs_traversal()
        st.write(riwayat_dfs)
