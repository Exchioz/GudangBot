class ItemHandler:
    def __init__(self):
        self.barang_data = {
            "keyboard": "Keyboard tersedia di toko kami",
            "mouse": "Mouse sedang kosong"
        }
    
    def handle(self, query: str) -> str:
        """Mengecek informasi barang dalam database."""
        if query in self.barang_data:
            return self.barang_data[query]
        else:
            raise AssertionError("Barang tidak ditemukan")

class CompanyHandler:
    def __init__(self):
        self.perusahaan_data = {
            "CEO": "CEO dari perusahaan adalah Ivan Rajwa",
            "lahir": "Perusahaan didirikan pada tahun 2002"
        }

    def handle(self, query: str) -> str:
        """Mengambil informasi tentang perusahaan."""
        if query in self.perusahaan_data:
            return self.perusahaan_data[query]
        else:
            raise AssertionError("Informasi perusahaan tidak ditemukan")