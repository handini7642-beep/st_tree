import streamlit as st

# ====================================================================
# 1. STRUKTUR DATA: NODE UNTUK GENERAL TREE (FILE EXPLORER)
# ====================================================================
class FileNode:
    def __init__(self, nama_item, is_folder=True):
        self.nama = nama_item
        self.is_folder = is_folder  # True untuk Folder, False untuk File
        self.children = []          # List berisi node anak (sub-folder/file)

    def add_child(self, child_node):
        """Menambahkan anak atau cabang baru ke dalam list"""
        self.children.append(child_node)
  
    def dapatkan_tree_string(self, level=0):
        """Mengatur spasi rekursif agar struktur pohon terlihat bertingkat"""
        indentasi = "   " * level
        if level == 0:
            simbol = "💻 "  # Root Utama
        else:
            simbol = "📁 ↳ " if self.is_folder else "📄 ↳ "
            
        hasil = f"{indentasi}{simbol}{self.nama}\n"

        # Looping rekursif untuk mengambil seluruh cabang di bawahnya
        for sub in self.children:
            hasil += sub.dapatkan_tree_string(level + 1)
        return hasil

    def cari_node(self, target_nama):
        """Mencari node spesifik berdasarkan namanya (Case Insensitive)"""
        if self.nama.lower() == target_nama.lower():
            return self
        
        for sub in self.children:
            hasil = sub.cari_node(target_nama)
            if hasil:
                return hasil   
        return None
  
    def cari_jalur(self, target, path=""):
        """Mencari jalur lengkap (breadcrumb) dari Root menuju ke item tertentu"""
        jalur_saat_ini = path + " > " + self.nama if path else self.nama

        if self.nama.lower() == target.lower():
            return jalur_saat_ini
        
        for sub in self.children:
            # MEMPERBAIKI REKURSIF: Memanggil fungsi cari_jalur (bukan cari_kategori)
            hasil = sub.cari_jalur(target, jalur_saat_ini)
            if hasil:
                return hasil     
        return None


# ====================================================================
# 2. KONFIGURASI HALAMAN & ENVIROMENT STREAMLIT
# ====================================================================
st.set_page_config(page_title="Tree File Explorer", page_icon="📂", layout="centered")

st.title("📂 Pembuat Struktur File Explorer")
st.caption("Proyek UAS Struktur Data — Skala: 🌟🌟🌟 Sulit (Konsep Mudah Dipahami)")
st.write("Aplikasi interaktif untuk mensimulasikan struktur data **General Tree**.")

# Inisialisasi session state untuk menyimpan struktur tree agar tidak hilang saat halaman di-refresh
if 'root' not in st.session_state:
    st.session_state.root = None

# JIKA ROOT BELUM DIBUAT: Tampilkan form pembuatan Root utama
if st.session_state.root is None:
    st.info("Sistem belum memiliki direktori utama. Silakan buat terlebih dahulu.")
    nama_root = st.text_input("Masukkan nama direktori utama (Root):", value="Root")

    if st.button("Buat Direktori Utama", type="primary"):
        if nama_root.strip() != "":
            st.session_state.root = FileNode(nama_root.strip(), is_folder=True)
            st.rerun()  # Refresh halaman
        else:
            st.warning("Nama Root tidak boleh kosong!")

# JIKA ROOT SUDAH ADA: Tampilkan menu utama menggunakan sistem Tabs
else:
    root = st.session_state.root

    # Menggunakan sistem 3 Tab modern sesuai dengan gaya codingan kamu
    tab1, tab2, tab3 = st.tabs(["📊 Lihat Struktur Tree", "➕ Tambah Cabang Baru", "📍 Cari Jalur (Breadcrumb)"])

    # --- TAB 1: LIHAT STRUKTUR TREE ---
    with tab1:
        st.subheader("Bagan Hierarki Direktori")
        tree_teks = root.dapatkan_tree_string()
        # Menggunakan st.code agar format indentasi/spasi karakter tetap lurus dan rapi
        st.code(tree_teks, language="text") 

    # --- TAB 2: TAMBAH CABANG BARU ---
    with tab2:
        st.subheader("Tambah Folder atau File Baru")
        induk_nama = st.text_input("Nama Folder induk tempat item akan ditambahkan:", placeholder="Contoh: Root atau Dokumen")
        anak_nama = st.text_input("Nama item baru yang ingin dibuat:", placeholder="Contoh: Tugas_1 atau foto.png")
        
        # Pilihan tipe item menggunakan komponen radio button
        tipe_item = st.radio("Tipe Item Baru:", ["Folder (Direktori)", "File (Arsip)"])

        if st.button("Tambah ke Dalam Tree", type="primary"):
            if induk_nama.strip() and anak_nama.strip():
                # Cari apakah folder induknya ada di dalam Tree
                induk_node = root.cari_node(induk_nama.strip())
                
                if induk_node:
                    if induk_node.is_folder:
                        # Cek apakah nama item baru sudah kembar di bawah induk tersebut
                        nama_kembar = False
                        for anak in induk_node.children:
                            if anak.nama.lower() == anak_nama.strip().lower():
                                nama_kembar = True
                                break
                        
                        if not nama_kembar:
                            # Tentukan status is_folder berdasarkan pilihan radio button
                            pilihan_folder = True if tipe_item == "Folder (Direktori)" else False
                            
                            # Melahirkan Node baru dan memasukkannya ke list children induk
                            induk_node.add_child(FileNode(anak_nama.strip(), is_folder=pilihan_folder))
                            st.success(f"✅ Berhasil menambahkan {tipe_item.split()[0]} '{anak_nama.strip()}' di bawah folder '{induk_node.nama}'!")
                            st.rerun()
                        else:
                            st.error(f"❌ Item dengan nama '{anak_nama.strip()}' sudah ada di dalam folder '{induk_node.nama}'.")
                    else:
                        st.error(f"❌ '{induk_node.nama}' adalah sebuah File, bukan Folder. Kamu tidak bisa menambahkan cabang di bawah File!")
                else:
                    st.error(f"❌ Folder induk '{induk_nama.strip()}' tidak ditemukan! Periksa kembali ejaan huruf besar/kecilnya.")
            else:
                st.warning("⚠️ Harap isi kedua kolom teks di atas sebelum mengklik tombol.")

    # --- TAB 3: CARI JALUR (BREADCRUMB) ---
    with tab3:
        st.subheader("Pencarian Lintasan Lokasi")
        target_cari = st.text_input("Masukkan nama file/folder yang ingin dilacak jalurnya:", placeholder="Contoh: foto.png")

        if st.button("Lacak Jalur Item"):
            if target_cari.strip():
                hasil_jalur = root.cari_jalur(target_cari.strip())
                if hasil_jalur:
                    st.success("✨ Item Berhasil Ditemukan dalam Sistem Tree!")
                    st.info(f"📍 **Jalur Akses (Breadcrumb):** \n`{hasil_jalur}`")
                else:
                    st.error(f"❌ Item '{target_cari.strip()}' tidak ditemukan di bagian cabang mana pun.")
            else:
                st.warning("⚠️ Harap isi nama item yang ingin dicari.")

    # --- TOMBOL RESET SISTEM ---
    st.divider()
    if st.button("🗑️ Reset Sistem (Mulai dari Awal)"):
        st.session_state.root = None
        st.rerun()