class PSD_DIFF():
    def __init__(self):
        self.header = {}
        self.layer = {}

    def diff_header(self, psd_before, psd_after):
        header_before = psd_before.get_psd_header()
        header_after = psd_after.get_psd_header()
        for field in header_before:
            self.header[field] = {}
            self.header[field]["before"] = header_before[field]
            self.header[field]["after"] = header_after[field]

    def diff_layer(self, psd_before, psd_after):
        layers_before = psd_before.get_psd_layers()
        layers_after = psd_after.get_psd_layers()
        layer_ids = set(layers_before.keys() + layers_after.keys())
        for layer_id in layer_ids:
            self.layer[layer_id] = {}
            self.layer[layer_id]["before"] = layers_before[layer_id]
            self.layer[layer_id]["after"] = layers_after[layer_id]
