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

    def diff_layer_pixel(self, layer_image_before, layer_image_after):
        layer_image_data_before = layer_image_before.load()
        layer_image_data_after = layer_image_after.load()
        pixel_index = 1
        pixel_diff = {}
        width, height = layer_image_before.size
        for y in xrange(height):
            for x in xrange(width):
                if layer_image_data_before[x, y] != layer_image_data_after[x, y]:
                    pixel_diff[str(pixel_index)] = {}
                    pixel_diff[str(pixel_index)]["before"] = list(layer_image_data_before[x, y])
                    pixel_diff[str(pixel_index)]["after"] = list(layer_image_data_after[x, y])
                pixel_index += 1
        return pixel_diff

    def diff_layer_parameters(self, layer_parameter_before, layer_parameter_after):
        parameter_diff = {}
        for parameter in layer_parameter_before.keys():
            parameter_diff[parameter] = {}
            parameter_diff[parameter]["before"] = layer_parameter_before[parameter]
            parameter_diff[parameter]["after"] = layer_parameter_after[parameter]
        return parameter_diff

    def diff_layers(self, psd_before, psd_after):
        layers_parameter_before = psd_before.get_psd_layers()
        layers_parameter_after = psd_after.get_psd_layers()
        layer_ids = set(layers_parameter_before.keys() + layers_parameter_after.keys())
        for layer_id in layer_ids:
            self.layer[layer_id] = {}
            self.layer[layer_id]["parameter"] = self.diff_layer_parameters(layers_parameter_before[layer_id], layers_parameter_after[layer_id])
            try:
                layer_image_before = psd_before.get_single_layer_image(int(layer_id))
                layer_image_after = psd_after.get_single_layer_image(int(layer_id))
                self.layer[layer_id]["pixel"] = self.diff_layer_pixel(layer_image_before, layer_image_after)
            except:
                self.layer[layer_id]["pixel"] = "Empty Layer."
       