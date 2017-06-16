class PSD_DIFF():
    def __init__(self):
        self.header = {}

    def diff_header(self, psd_before, psd_after):
        header_before = psd_before.get_psd_header()
        header_after = psd_after.get_psd_header()
        for field in header_before:
            self.header[field] = {}
            self.header[field]["before"] = header_before[field]
            self.header[field]["after"] = header_after[field]
