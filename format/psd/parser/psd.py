from psd_tools import PSDImage

class PSD():
    def __init__(self):
        self.header_fields = ["number_of_channels", "height", "width", "depth", "color_mode"]
        self.layer_fields = ["name", "blend_mode", "opacity", "visible"]
        self.bbox_fields = ["height", "width", "x1", "x2", "y1", "y2"]

    def load_psd_from_file(self, file_path):
        self.psd_file = PSDImage.load(file_path)

    def get_psd_header(self):
        self.header = {}
        for field in self.header_fields:
            self.header[field] = getattr(self.psd_file.header, field)
        return self.header

    def get_psd_layers(self, layer_id = None):
        self.layers = {}
        for layer in self.psd_file.layers:
            l_id = str(layer.layer_id)
            self.layers[l_id] = {}
            for field in self.layer_fields:
                self.layers[l_id][field] = getattr(layer, field)
            bbox = {}
            for field in self.bbox_fields:
                bbox[field] = getattr(layer.bbox, field)
            self.layers[l_id]["bbox"] = bbox
        if layer_id is not None:
            return self.layers[str(layer_id)]
        return self.layers

    def get_decoded_data(self):
        return self.psd_file.decoded_data

    def get_embedded(self):
        return self.psd_file.embedded

    def export_single_layer(self, index, file_path):
        layer_image = self.psd_file.layers[index].as_PIL()
        layer_image.save(file_path)

    def export_merged_image(self, file_path):
        merged_image = self.psd_file.as_PIL()
        merged_image.save(file_path)