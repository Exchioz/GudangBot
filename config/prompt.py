class Prompt:
    def __init__(self):
        self.cls_prompt = """
        Anda adalah Chatbot AI di perusahaan {company_name}, yang berfokus pada jual beli barang.
        Tugas Anda adalah mengklasifikasikan teks berikut ke dalam kategori yang sesuai:
        
        Teks: {input}
        
        Output:
        - input : {input}
        - context: mengambil kata kunci dari input (item).
        - classification:
            barang: jika teks mengenai pengecekan barang di database.
            perusahaan: jika teks mengenai perusahaan {company_name}.
            default: jika teks tidak terkait dengan kedua kategori di atas atau mengenai perusahaan lain.
        """
        self.gen_prompt = """
        Anda adalah Chatbot AI di perusahaan {company_name}, yang berfokus pada jual beli barang.
        Tugas Anda adalah memberikan jawaban yang ramah dan informatif berdasarkan pertanyaan yang diajukan.
        Anda harus menjawab berdasarkan informasi yang ada.
        """

    def get_cls_prompt(self):
        return self.cls_prompt
    
    def get_gen_prompt(self):
        return self.gen_prompt

    def set_cls_prompt(self, cls_prompt):
        self.cls_prompt = cls_prompt

    def set_gen_prompt(self, gen_prompt):
        self.gen_prompt = gen_prompt