# Aplikasi Pemutar Musik Berbasis Desktop GUI  
Tugas Besar Mata Kuliah Struktur Data

## Kelompok 4

### Anggota Kelompok
- Muhammad Ilham Maulana (103102400018)  
- Muhammad Alfayyad Nezzati Qosim (103102400029)  
- Muhammad Ade Sulistiansyah (103102400045)  

## Deskripsi Aplikasi
Aplikasi Pemutar Musik Berbasis Desktop GUI merupakan aplikasi pemutar audio yang dikembangkan menggunakan bahasa pemrograman Python dengan antarmuka grafis berbasis CustomTkinter. Aplikasi ini dirancang untuk menerapkan konsep struktur data dalam pengelolaan data lagu secara terstruktur dan efisien.

Aplikasi memiliki dua peran utama, yaitu Admin dan User. Admin bertanggung jawab dalam pengelolaan library lagu seperti menambah, mengubah, dan menghapus lagu. Sementara itu, User dapat melakukan pemutaran lagu, pencarian lagu, pengelolaan playlist, melihat riwayat pemutaran, menandai lagu favorit, serta menggunakan fitur navigasi Next dan Previous.

Dalam pengembangannya, aplikasi ini menerapkan beberapa struktur data sesuai kebutuhan fungsional, antara lain Doubly Linked List untuk navigasi lagu, Linked List untuk playlist, Stack untuk riwayat pemutaran, Queue untuk antrean lagu, Set untuk daftar favorit tanpa duplikasi, serta Dictionary untuk login user dan akses data lagu secara cepat. Pemutaran audio didukung oleh library pygame mixer yang mampu memutar file audio berformat MP3.

## Tujuan Pembuatan
1. Menerapkan konsep struktur data ke dalam implementasi aplikasi nyata.
2. Memahami pemilihan struktur data yang tepat untuk kebutuhan sistem.
3. Mengintegrasikan logika struktur data dengan antarmuka pengguna (GUI).
4. Menghubungkan teori struktur data dengan pemrograman berbasis aplikasi.

## Struktur Data yang Digunakan

| Struktur Data | Fungsi |
|--------------|--------|
| Doubly Linked List | Menyimpan library lagu dan mendukung navigasi Next dan Previous |
| Linked List | Menyimpan playlist lagu |
| Stack | Menyimpan riwayat pemutaran lagu (History) |
| Queue | Mengelola antrean pemutaran lagu |
| Set | Menyimpan daftar lagu favorit tanpa duplikasi |
| Dictionary | Login user dan pencarian lagu secara cepat |

## Fitur Aplikasi
- Menambahkan lagu ke library
- Mengedit data lagu
- Menghapus lagu
- Melihat daftar lagu

### Fitur User
- Play, Pause, Next, dan Previous lagu
- Pencarian lagu
- Membuat dan mengelola playlist
- Menandai lagu favorit
- Melihat riwayat pemutaran lagu
- Mengelola antrean lagu (Queue)

---

## Teknologi yang Digunakan
- Bahasa Pemrograman: Python 3  
- GUI Framework: CustomTkinter  
- Audio Engine: Pygame Mixer  
- Penyimpanan Data: File JSON  

## Cara Menjalankan Aplikasi
1. Pastikan Python 3 telah terinstal pada perangkat.
2. Install library yang dibutuhkan:
   ```bash
   pip install pygame customtkinter
3. Jalankan aplikasi dengan perintah:
   ```bash
   python main.py

