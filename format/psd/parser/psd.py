from psd_tools import PSDImage

class PSD():
    def __init__(self):
        pass

    def load_psd_from_file(self, file_path):
        self.psd_file = PSDImage.load(file_path)

    def get_psd_header(self):
        self.header = {}
        for field in self.psd_file.header._fields:
            self.header[field] = getattr(self.psd_file.header, field)
        return self.header

    def get_psd_layers(self, index = None):
        if index is not None:
            return self.psd_file.layers[index]
        return self.psd_file.layers

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