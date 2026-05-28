import streamlit as st

# 1. SET CONFIG & THEME SOFT PASTEL GEMES
st.set_page_config(page_title="CloudySpace - Cute File Explorer", layout="wide", page_icon="☁️")

# Menyuntikkan CSS Kustom dengan Palet Warna Pastel Modern & Lucu
st.markdown("""
    <style>
    /* Background utama warna cream super soft */
    .stApp {
        background-color: #FAF8F6;
    }
    
    /* Mengubah gaya container/card folder menjadi bulat-bulat lucu dengan shadow soft */
    div[data-testid="stCard"] {
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 18px;
        box-shadow: 0 8px 16px rgba(149, 157, 165, 0.05);
        border: 2px solid #F1EFEA;
        transition: all 0.3s ease;
    }
    div[data-testid="stCard"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 20px rgba(149, 157, 165, 0.1);
        border-color: #FFDEE9;
    }
    
    /* Custom style untuk judul tab agar lebih rapi */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #FFFFFF;
        border: 1px solid #EAECEE;
        border-radius: 20px;
        padding: 6px 16px;
        font-weight: 600;
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
        fav = " 💕" if node.is_favorite else ""
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
        if ekstensi in ["pdf"]: return "🌸 "  # Tugas / PDF jadi bunga pink soft
        if ekstensi in ["txt", "docx", "doc"]: return "📑 "
        if ekstensi in ["jpg", "jpeg", "png", "gif"]: return "🎨 " # Foto jadi palet seni lucu
        if ekstensi in ["mp4", "mkv"]: return "🍿 "
        if ekstensi in ["mp3"]: return "🧸 "
        if ekstensi in ["zip", "rar"]: return "🎁 "
    return "✏️ "

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
    sistem
