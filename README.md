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
| Mie Jebew | Rp 5.000 | digoreng dadakan — **harga belum termasuk bakso** |
| Topping Bakso | Rp 1.000/butir | opsional, di luar harga Mie Jebew (maks. 10 butir) |
| Es Cendol | Rp 8.000 | disajikan dingin |

> Grid katalog desktop memakai 2×2 agar empat kartu tetap seimbang; di mobile menjadi satu kolom.

### Topping bakso (revisi 21 Okt 2026)

Foto Mie Jebew menampilkan bakso, sedangkan harganya Rp 5.000. Supaya pembeli tidak menyimpulkan "Rp 5.000 sudah dapat 3 bakso", dipakai **empat penanda** sekaligus:

1. **Badge harga** bertuliskan `Rp 5.000` dengan baris kecil **TANPA BAKSO** tepat di bawah angka.
2. **Baris topping** di kartu: `Topping Bakso — Opsional · +Rp 1.000/butir, di luar harga Mie Jebew`, lengkap dengan stepper 0–10.
3. **Keranjang** menampilkan bakso sebagai sub-baris indentasi di bawah Mie Jebew (`+ Bakso (topping Mie Jebew) 3 × Rp 1.000 = Rp 3.000`), bukan digabung diam-diam.
4. **Pesan WhatsApp** menaruh bakso sebagai baris `+ Bakso × 3 — Rp 3.000` di bawah Mie Jebew, sehingga penjual melihat rinciannya.

Bot juga ikut: menjawab harga Mie Jebew dengan catatan topping terpisah, dan perintah seperti *"pesan 2 mie jebew 3 bakso"* menambahkan keduanya sekaligus.

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
3. Pembeli mengisi nama, nomor HP, **alamat pengiriman**, memilih cabang, dan catatan opsional.
   Alamat pengiriman **wajib** (minimal 8 karakter) karena dipakai kurir. Pembeli yang ambil sendiri di cabang menulis: *"Ambil sendiri di cabang"*.
4. Tombol **Kirim Pesanan ke WhatsApp** membuka WhatsApp cabang terpilih dengan pesan yang sudah rapi:

```text
*PESANAN DAPUR MBAK YU*
------------------------------
Nama    : Farid
No. HP  : 081234567890
Alamat  : Jl. Melati No. 12, RT 03/RW 05, Jakamulya, Bekasi Selatan (patokan: depan masjid)
Cabang  : Cabang Cikunir (Bekasi Selatan)
------------------------------
*Rincian pesanan:*
• Sambel Pecel × 1 — Rp 23.000
• Es Cendol × 2 — Rp 8.000
------------------------------
*Total   : Rp 39.000*
Catatan : pedas banget, sambel dipisah
Waktu   : 19/10/26, 16.52 WIB
```

> **Penting:** baris `Alamat` berisi alamat **pemesan**, bukan alamat toko. Alamat cabang tidak lagi dimasukkan ke pesan WhatsApp karena penerima pesan itu adalah cabang itu sendiri. Kalau nanti perlu alamat cabang ikut tercetak, tambahkan baris terpisah (`Toko    : ${b.address}`) di `buildMessage()` — jangan menimpa baris `Alamat`.

Validasi yang sudah aktif: nama minimal 2 huruf, nomor HP minimal 9 angka, **alamat pengiriman minimal 8 karakter**, dan tombol kirim nonaktif saat keranjang kosong.

---

## 6. Chatbot (asisten otomatis)

Tombol bulat hijau di kanan bawah (ikon balon percakapan) membuka **Asisten Mbak Yu** — chatbot tanya-jawab yang berjalan **sepenuhnya di browser**. Tidak ada API key, tidak ada server, tidak ada biaya per pesan, dan tidak ada data pembeli yang dikirim ke mana pun.

**Kenapa bukan AI berbayar?** Karena website ini statis: API key yang ditanam di HTML bisa diambil siapa pun lewat *view source*, lalu dipakai atas biaya pemilik. Chatbot aturan (rule-based) tidak punya masalah itu.

**Karakter Mbak Yu:** chatbot memakai maskot wajah berkerudung hijau (mirip label kemasan Sambel Pecel) yang digambar sebagai **SVG inline** — tidak ada file gambar tambahan, tetap tajam di semua ukuran, dan otomatis mengikuti palet merek. Wajahnya muncul di tiga tempat: tombol melayang, header panel sebagai avatar 42 px, dan avatar 30 px di samping setiap balasan beserta indikator "sedang menulis". Tombol melayang diberi titik hijau (aktif) dan lencana balon chat, plus **balon sapaan** yang muncul sekali per sesi setelah 9 detik ("Halo, aku Mbak Yu 👋") — bisa ditutup dan tidak muncul lagi sampai tab ditutup.

**Batas persona:** header menuliskan **"Asisten otomatis"** dan topik `bot` menjelaskan bahwa ini asisten, bukan Mbak Yu orangnya. Karakternya adalah maskot merek, bukan klaim ada manusia yang sedang online.

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
   `Timestamp | Nama Pelanggan | No HP | Alamat Pengiriman | Cabang | Rincian Pesanan | Total Bayar | Catatan`
2. Menu **Extensions → Apps Script**, tempel:

```javascript
function doPost(e) {
  try {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    var d = JSON.parse(e.postData.contents);
    sheet.appendRow([d.timestamp, d.nama_pelanggan, d.no_hp, d.alamat_pengiriman,
                     d.cabang, d.rincian_pesanan, d.total_bayar, d.catatan]);
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

### Status deploy (20 Oktober 2026)

- **GitHub:** sudah terunggah di [github.com/jarangjaka99/dapur-mbak-yu](https://github.com/jarangjaka99/dapur-mbak-yu), branch `main`.
- **Live sekarang (sementara):** <https://jarangjaka99.github.io/dapur-mbak-yu/> — GitHub Pages aktif dari `main`, sudah dicek HTTP 200 dan seluruh aset termuat.
- **Vercel:** **aktif** di <https://dapur-mbak-yu.vercel.app> — proyek `dapur-mbak-yu`, team `jarang-jaka-s-projects`. Deployment produksi pertama: `dpl_6mm2CHcRXkiSm5Dt79xuxFQfBhb8`, status READY, alias otomatis ke domain di atas.
- **Auto-deploy:** repository GitHub sudah **terhubung** ke proyek Vercel (`vercel git connect`). Setiap push ke `main` langsung dideploy produksi. Tidak perlu token di CI lagi.
- **Verifikasi live:** HTTP 200, judul halaman benar, 14 kemunculan "Sambel Pecel", harga "Rp 23.000", chatbot (`__chat`), karakter Mbak Yu, balon sapaan, 2 peta tersemat, dan `img/poster.webp` + `img/tahu-gejrot.webp` + `img/logo-dmy.png` semuanya `200`.
- **Catatan riwayat:** sempat gagal karena (a) jaringan `network tester_5G` memblokir `vercel.com` (TLS reset), lalu (b) token CLI kedaluwarsa (`403 invalidToken`). Setelah Farid pindah ke internet HP, login device-flow berhasil dan deploy berjalan.

## 11. QR & materi promosi

Folder `promo/` berisi berkas siap pakai untuk promosi offline maupun status WhatsApp:

| Berkas | Ukuran | Untuk apa |
|---|---|---|
| `qr-website.png` | 1024×1024 | QR polos (logo di tengah), tempel di banner, brosur, kemasan |
| `qr-website.svg` | vektor | percetakan skala besar (tanpa logo, paling aman untuk cetak) |
| `qr-card-a5.png` / `.pdf` | A5 300 dpi | kartu meja / standee / poster kecil |
| `qr-sticker.png` | 1400×1400 | status WhatsApp, feed IG, stiker |

- **Isi QR:** `https://dapur-mbak-yu.vercel.app`
- **Koreksi galat:** level **H (30%)** — tahan kotor/basah dan tetap terbaca walau ada logo di tengah.
- **Warna:** hijau tua `#0E3B2C` di atas putih (kontras tinggi, aman untuk printer thermal/sepiak).
- **Sudah diuji pindai** dengan decoder jsQR: terbaca benar pada ukuran **1024 px, 240 px, bahkan 160 px** — jadi aman dicetak kecil (stiker 3×3 cm) maupun ditampilkan di layar.
- **Mencetak:** pakai `qr-card-a5.pdf` (vektor teks + QR resolusi penuh) agar tajam. Jangan gunting pita putih di sekitar QR — itu *quiet zone* yang wajib ada.
- **Mengganti alamat:** kalau nanti pakai domain sendiri (mis. `dapurmbakyu.my.id`), buat QR baru dengan alamat itu — QR lama tidak bisa diarahkan ulang.

**Membuat ulang semua materi** (butuh `qrencode` + Python/Pillow):

```bash
python3 promo/buat-qr.py
```

Skripnya ada di `promo/buat-qr.py` — ubah variabel `URL` di baris atas kalau alamat situs berubah, lalu jalankan lagi. Font ada di `promo/fonts/` (tidak di-commit ke git, unduh ulang dari Google Fonts bila perlu).

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
