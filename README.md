# Dapur Mbak Yu — Landing Page & Pemesanan WhatsApp

Website penjualan statis (satu halaman) untuk **Dapur Mbak Yu**: Sambel Pecel, Es Cendol, dan Mie Jebew.
Tanpa backend, tanpa database. Pesanan disusun otomatis menjadi pesan WhatsApp ke cabang pilihan pembeli.

**Berkas inti:** `index.html` (HTML + CSS + JS jadi satu), folder `img/` untuk foto.
**Total ukuran:** ± 600 KB (foto sudah dikompres WebP, logo dioptimalkan).

---

## 1. Isi paket

```text
dapur-mbak-yu/
├── index.html      # seluruh halaman: markup, CSS, logika keranjang/checkout, dan chatbot
├── README.md       # dokumen ini
└── img/
    ├── poster.webp        # poster menu (hero)
    ├── logo-dmy.png       # logo transparan (nav, footer, favicon)
    ├── sambel-pecel.webp  # foto produk
    ├── es-cendol.webp     # foto produk (watermark pihak lain sudah dipotong)
    └── mie-jebew.webp     # foto produk (diambil dari poster, banner harga dipotong)
```

**Cara melihat:** klik dua kali `index.html`, atau `python3 -m http.server` di folder ini lalu buka `http://localhost:8000`.

---

## 2. Menu & harga (sumber: flyer resmi)

| Menu | Harga | Catatan |
|---|---|---|
| Sambel Pecel | Rp 23.000 | pilihan sedang / pedas banget |
| Tahu Gejrot | Rp 10.000 | kuah disiram saat dipesan |
| Mie Jebew | Rp 5.000 | digoreng dadakan |
| Es Cendol | Rp 8.000 | disajikan dingin |

> Tambahan bakso (yang ada di flyer) **tidak dijual** di website ini sesuai instruksi pemilik.
> Grid katalog desktop memakai 2×2 agar empat kartu tetap seimbang; di mobile menjadi satu kolom.

---

## 3. Nomor WhatsApp cabang

| Cabang | Nomor tampil | Format `wa.me` | Alamat lengkap | Titik peta |
|---|---|---|---|---|
| Cikunir (Bekasi Selatan) | 0855-8017-393 | `628558017393` | Jl. Rambutan RT 9/11, Cluster Vicsha A8, Kampung Jaha, Cikunir, Jatiasih | `-6.2821702, 106.9559453` |
| Harapan Jaya (Bekasi Utara) | 0811-8588-305 | `628118588305` | Perumahan Harapan Jaya II, Blok F 28, RT 07 RW 019, Jl. Sungai Kampar | `-6.2187035, 106.9912715` |

Alamat ini muncul di **empat tempat**: kartu pilihan cabang pada form, kartu cabang di bagian Lokasi, pesan WhatsApp, dan `CONFIG` di `index.html`. Ubah `CONFIG` lalu samakan ketiga teks tampilan agar tidak berbeda.
Peta di kartu cabang memakai Google Maps embed berbasis koordinat (`output=embed`) sehingga tidak butuh API key.

Nomor ini muncul di 5 tempat: tombol nav, dua kartu cabang, footer, tombol mengambang, dan tujuan checkout.
Kalau salah satu nomor berubah, ubah **semua** kemunculannya (cari `628558017393` lalu `628118588305` di `index.html`).

---

## 4. Mengubah menu / harga

Buka `index.html`, cari `const MENU = [` (sekitar baris 700). Setiap produk satu objek:

```js
{
  id: "sambel-pecel",          // dipakai sebagai kunci keranjang (jangan ada spasi)
  name: "Sambel Pecel",        // nama yang tampil
  price: 23000,                // angka rupiah, tanpa titik
  unit: "kemasan",
  image: "img/sambel-pecel.webp",
  alt: "deskripsi foto untuk pembaca layar",
  badge: "Paling Dicari",      // label di sudut foto
  badgeClass: "badge",         // badge | badge green | badge yellow
  desc: "kalimat penjualan singkat",
  note: "Tersedia sedang / pedas banget",
  noteIcon: "chili"            // chili | cup | fire
}
```

Harga kartu, subtotal, total, dan teks WhatsApp semuanya dihitung dari `price` — tidak ada angka yang ditulis dua kali.
Untuk mengganti foto: taruh file baru di `img/`, lalu ubah `image`.

### Mengubah nomor WA / alamat cabang

Cari `const CONFIG = {` di bagian atas `<script>`. Setiap cabang punya `name`, `short`, `whatsapp` (format 62…), dan `address`.
Teks pesan WhatsApp otomatis memakai data ini.

---

## 5. Alur pesanan

1. Pembeli menekan **Tambah** pada kartu menu (bisa diubah dengan − / + di kartu maupun di ringkasan keranjang).
2. Ringkasan keranjang menghitung subtotal per baris dan total, dengan catatan **belum termasuk ongkir**.
3. Pembeli mengisi nama, nomor HP, memilih cabang, dan catatan opsional.
4. Tombol **Kirim Pesanan ke WhatsApp** membuka WhatsApp cabang terpilih dengan pesan yang sudah rapi:

```text
*PESANAN DAPUR MBAK YU*
------------------------------
Nama    : Farid
No. HP  : 081234567890
Cabang  : Cabang Cikunir (Bekasi Selatan)
Alamat  : Jl. Raya Cikunir, Jakamulya, Bekasi Selatan
------------------------------
*Rincian pesanan:*
• Sambel Pecel × 1 — Rp 23.000
• Es Cendol × 2 — Rp 8.000
------------------------------
*Total   : Rp 39.000*
Catatan : pedas banget, sambel dipisah
Waktu   : 19/10/26, 16.52 WIB
```

Validasi yang sudah aktif: nama minimal 2 huruf, nomor HP minimal 9 angka, dan tombol kirim nonaktif saat keranjang kosong.

---

## 6. Chatbot (asisten otomatis)

Tombol bulat hijau di kanan bawah (ikon balon percakapan) membuka **Asisten Mbak Yu** — chatbot tanya-jawab yang berjalan **sepenuhnya di browser**. Tidak ada API key, tidak ada server, tidak ada biaya per pesan, dan tidak ada data pembeli yang dikirim ke mana pun.

**Kenapa bukan AI berbayar?** Karena website ini statis: API key yang ditanam di HTML bisa diambil siapa pun lewat *view source*, lalu dipakai atas biaya pemilik. Chatbot aturan (rule-based) tidak punya masalah itu.

**Cara kerjanya:** pertanyaan dinormalisasi (huruf kecil, tanda baca dibuang) → dicocokkan dengan daftar kata kunci tiap topik memakai pencocokan **awalan kata** (jadi "ongkirnya" tetap kena "ongkir") → topik dengan skor tertinggi menjawab. Kalau tidak ada yang cocok, bot mengaku belum paham dan menawarkan WhatsApp.

**Topik yang sudah ditangani (20):** sapaan, menu & harga, harga per produk, level pedas, halal, pengawet & masa simpan, ongkir/pengiriman luar kota, jam buka, alamat & peta dua cabang, pembayaran, minimal order, cara pesan, tambah ke keranjang dari dalam chat, promo, reseller/grosir, pesanan acara/katering, alergi & bahan, ukuran porsi, status pesanan/komplain, "kamu bot?", dan terima kasih.

**Ikut data website:** daftar harga, alamat, nomor WhatsApp, dan tautan peta diambil langsung dari `MENU` dan `CONFIG` — kalau harga diubah di satu tempat, jawaban bot ikut berubah. Bot juga bisa menambahkan pesanan ke keranjang: tulis misalnya *"pesan 2 es cendol"*.

**Menambah topik baru:** cari `var KB = [` di dalam `<script>` terakhir, lalu tambahkan objek:

```js
{
  id: "nama_topik", prio: 3,
  keys: ["kata kunci", "frasa lain", "sinonim"],
  reply: function (t) {
    return {
      text: "Jawaban dalam HTML ringan, boleh pakai <b>tebal</b>.",
      actions: [{ type: "wa", label: "Tanya via WhatsApp" }],
      chips: ["Lihat menu", "Ongkir"]
    };
  }
}
```

`prio` lebih besar = menang saat skor seri. Jenis `actions`: `wa` (buka WhatsApp), `maps` (buka peta cabang), `cart` (tambah produk ke keranjang, butuh `id` produk), `scroll` (gulir ke form pesanan).

**Batas kejujuran:** bot tidak mengarang. Untuk hal yang tidak ada di data (stok, ukuran gram kemasan, status pesanan, harga reseller), ia mengatakan belum tahu lalu mengarahkan ke WhatsApp. Kalau nanti jam buka dikonfirmasi berbeda, ubah di dua tempat: kartu cabang **dan** jawaban topik `jam`.

**Pintu uji:** di konsol browser, `__chat.ask("ongkir berapa")` mengembalikan jawaban tanpa mengetik manual.

## 7. Rekap pesanan ke Google Sheets (opsional)

Website tetap jalan tanpa ini. Kalau ingin setiap pesanan tercatat otomatis:

1. Buat Google Sheets dengan kolom baris 1:
   `Timestamp | Nama Pelanggan | No HP | Cabang | Rincian Pesanan | Total Bayar | Catatan`
2. Menu **Extensions → Apps Script**, tempel:

```javascript
function doPost(e) {
  try {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    var d = JSON.parse(e.postData.contents);
    sheet.appendRow([d.timestamp, d.nama_pelanggan, d.no_hp, d.cabang,
                     d.rincian_pesanan, d.total_bayar, d.catatan]);
    return ContentService.createTextOutput(JSON.stringify({status:"success"}))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({status:"error", message:err.toString()}))
      .setMimeType(ContentService.MimeType.JSON);
  }
}
```

3. **Deploy → New deployment → Web app**, *Execute as*: Me, *Who has access*: **Anyone**. Salin URL yang berakhiran `/exec`.
4. Tempel ke `GOOGLE_SCRIPT_URL` di `CONFIG` dalam `index.html`.

Pengiriman rekap berjalan `no-cors` dan tidak pernah menghalangi pembeli membuka WhatsApp.

---

## 8. Cara mengunggah (hosting gratis)

Semua opsi di bawah gratis dan otomatis memberi HTTPS:

- **Netlify Drop** — buka `app.netlify.com/drop`, tarik foldernya. Selesai.
- **Cloudflare Pages** — *Create project → Direct upload*, unggah folder.
- **Vercel** — `vercel --prod` dari folder ini (butuh CLI dan login).
- **GitHub Pages** — unggah ke repo, aktifkan *Settings → Pages → branch main*.
- **cPanel hosting** — unggah isi folder ke `public_html` lewat File Manager.

Karena hanya HTML/CSS/JS statis, tidak ada server yang perlu dirawat atau ditambal.

---

## 9. Catatan operasional

- **Jam buka tidak ditampilkan:** atas permintaan pemilik (20 Okt 2026), jam buka dihapus dari kartu cabang dan dari jawaban chatbot. Bot menjawab jujur bahwa jam belum dicantumkan lalu mengarahkan ke WhatsApp. Kalau nanti jamnya sudah pasti, tambahkan kembali di `.bcard .meta` **dan** di topik `jam` pada chatbot.
- **Nomor WhatsApp tidak ditampilkan di footer:** bagian "Hubungi Kami" hanya menampilkan label "WhatsApp Cabang Cikunir/Harapan Jaya" tanpa digit nomor, tetapi tautannya tetap membuka chat yang benar. Nomor masih terlihat di kartu pilihan cabang pada formulir pesanan dan di jawaban chatbot.
- Teks FAQ (ongkir, ketahanan sambel, minimal order, pembayaran) perlu dicek pemilik — isinya wajar, tetapi bukan hasil wawancara.
- Foto Es Cendol berasal dari materi yang dikirim; watermark merek lain sudah dipotong. Sebaiknya diganti foto produksi sendiri saat tersedia.
- Semua tombol WhatsApp diuji membuka nomor yang benar (`628558017393` dan `628118588305`), keranjang diuji sampai total, dan halaman diuji pada lebar 390 px, 768 px, dan 1366 px tanpa error JavaScript.

---

## 10. Hasil pengujian terakhir

**74 pemeriksaan otomatis** (Chromium headless): **34 untuk halaman + 40 untuk chatbot**, semuanya lulus, 0 error JavaScript.

Halaman:
- semua gambar termuat (6/6) termasuk foto Tahu Gejrot;
- total keranjang benar: 3 menu = Rp 36.000, 4 menu = Rp 46.000, dan Rp 31.000 setelah satu item dikurangi;
- validasi nama kosong, nomor HP pendek, dan keranjang kosong;
- checkout Cabang Cikunir → `phone=628558017393`, Cabang Harapan Jaya → `phone=628118588305`;
- isi pesan memuat nama, cabang, rincian item, total, dan catatan;
- alamat baru muncul di form, kartu cabang, dan pesan WhatsApp; dua peta tersemat memakai koordinat benar;
- tidak ada nomor placeholder lama maupun harga 22K yang tersisa;
- menu mobile membuka/menutup dengan benar, tanpa scroll horizontal pada 390 px;
- footer tidak tertutup bar keranjang.

Chatbot:
- panel terbuka dari tombol melayang **dan** tautan footer, sapaan awal muncul, chip saran tampil;
- 28 pertanyaan uji dijawab sesuai topik (harga per produk, menu, pedas, halal, masa simpan, ongkir, pengiriman luar kota, jam, alamat dua cabang, pembayaran, minimal order, cara pesan, promo, reseller, pesanan acara, alergi, ukuran porsi, status pesanan, "kamu bot", terima kasih);
- pertanyaan ngawur dijawab jujur "belum yakin" + tawaran WhatsApp, bukan jawaban karangan;
- bot bisa menambah pesanan: "pesan 2 es cendol" → keranjang berisi 2 × Rp 8.000 = Rp 16.000;
- tombol WhatsApp pada jawaban memakai nomor cabang yang aktif; Escape menutup panel;
- panel muat di layar 390 px tanpa scroll horizontal.
