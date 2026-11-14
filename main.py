import json

with open("aturan.json", "r", encoding="utf-8") as file: knowledge_base = json.load(file)

fakta = knowledge_base["fakta"]
aturan = knowledge_base["aturan"]
kesimpulan = knowledge_base["kesimpulan"]

def input_fakta():
    fakta_awal = []

    print("==============================================")
    print(" SISTEM PAKAR IDENTIFIKASI POTENSI KEKERINGAN")
    print("       AKIBAT FENOMENA EL NINO")
    print("==============================================")
    print("\nJawab pertanyaan berikut dengan y atau t.\n")

    for i, item in enumerate(fakta, start=1):
        while True:
            jawaban = input(
                f"{i}. {item['pertanyaan']} (y/t) > "
            ).lower().strip()

            if jawaban == "y":
                fakta_awal.append(item["id"])
                break
            elif jawaban == "t":
                break
            else:
                print("Masukkan y atau t!")
    return fakta_awal

def cari_nama(kode):
    for item in fakta:
        if item["id"] == kode:
            return item["pertanyaan"].replace("Apakah ", "").replace("?", "")
    if kode in kesimpulan:
        return kesimpulan[kode]
    return kode

def forward_chaining(fakta_awal):
    fakta_aktif = fakta_awal.copy()
    aturan_digunakan = []
    siklus = 1

    print("\nFakta awal:")
    if fakta_awal:
        for kode in fakta_awal:
            print("- " + cari_nama(kode))
    else:
        print("- Tidak ada fakta yang terpenuhi.")

    while True:
        fakta_baru = []

        for aturan_item in aturan:
            kondisi = aturan_item["jika"]
            hasil = aturan_item["maka"]

            if all(item in fakta_aktif for item in kondisi):
                if hasil not in fakta_aktif:
                    fakta_baru.append(hasil)
                    aturan_digunakan.append(aturan_item)

        if fakta_baru:
            for hasil in fakta_baru:
                fakta_aktif.append(hasil)

                aturan_id = next(
                    item["id"] for item in aturan
                    if item["maka"] == hasil
                )
                print(
                    f"\nSiklus {siklus}: {aturan_id} -> "
                    f"{cari_nama(hasil)}"
                )
            siklus += 1
        else:
            print(
                f"\nSiklus {siklus}: "
                "Tidak ada aturan baru, berhenti."
            )
            break
    return fakta_aktif, aturan_digunakan

def tampilkan_alasan(kode, aturan_digunakan, tingkat=0):
    for aturan_item in aturan_digunakan:
        if aturan_item["maka"] == kode:
            kondisi = aturan_item["jika"]
            indentasi = "  " * tingkat

            print(
                f"{indentasi}{cari_nama(kode)} "
                f"<- {aturan_item['id']} "
                f"({', '.join(cari_nama(k) for k in kondisi)})"
            )

            for fakta_kode in kondisi:
                if fakta_kode in kesimpulan:
                    tampilkan_alasan( fakta_kode, aturan_digunakan, tingkat + 1)
            return

def tampilkan_hasil(fakta_aktif, aturan_digunakan):
    print("\n==============================================")
    print("                 KESIMPULAN")
    print("==============================================")

    hasil_ditemukan = []

    for kode in kesimpulan:
        if kode in fakta_aktif:
            hasil_ditemukan.append(kode)
    if hasil_ditemukan:
        for kode in hasil_ditemukan:
            print("- " + kesimpulan[kode])
        print("\nAlasan:")
        for kode in hasil_ditemukan:
            tampilkan_alasan(kode, aturan_digunakan)
    else:
        print("Tidak ditemukan kesimpulan.")
        print("Kondisi yang dimasukkan belum memenuhi aturan.")
    print("\n==============================================")

def main():
    fakta_awal = input_fakta()

    fakta_aktif, aturan_digunakan = forward_chaining(fakta_awal)

    tampilkan_hasil(fakta_aktif, aturan_digunakan)
main()