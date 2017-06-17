from psd_tools import PSDImage

class PSD():
    def __init__(self):
        self.header_fields = ["number_of_channels", "height", "width", "depth", "color_mode"]
        self.layer_fields = ["name", "blend_mode", "opacity", "visible"]
        self.bbox_fields = ["height", "width", "x1", "x2", "y1", "y2"]

    def load_psd_from_file(self, file_path):
        """load psd from file

        args:
            file_path (str)
        """
        self.psd_file = PSDImage.load(file_path)

    def get_psd_header(self):
        """get psd header

        returns:
            header (dict)
        """
        self.header = {}
        for field in self.header_fields:
            self.header[field] = getattr(self.psd_file.header, field)
        return self.header

    def get_psd_layers(self, layer_id = None):
        """get psd layers

        args:
            layer_id (int)

        returns:
            layers (dict)
        """
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
        """get psd decoded data

        returns:
            decoded_data (psd_tools.reader.reader.ParseResult)
        """
        return self.psd_file.decoded_data

    def get_embedded(self):
        """get psd embedded

        returns:
            embedded (list)
        """
        return self.psd_file.embedded

    def get_single_layer_image(self, layer_id):
        """get psd single layer image

        args:
            layer_id (int)
        
        returns:
            layer (PIL.Image)
        """
        for layer in self.psd_file.layers:
            if layer.layer_id == layer_id:
                return layer.as_PIL()

    def get_merged_image(self):
        """get psd merged image

        returns:
            psd (PIL.Image)
        """
        return self.psd_file.as_PIL()

    def export_single_layer(self, layer_id, file_path):
        """export single layer image

        args:
            layer_id (int)
            file_path (str)
        """
        self.get_single_layer_image(layer_id).save(file_path)

    def export_merged_image(self, file_path):
        """export merged image

        args:
            file_path (str)
        """
        self.get_merged_image().save(file_path)
