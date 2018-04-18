import json

class JsonPrefsUtil:

    def __init__(self, json_string='[]'):
        self.json_data = json.loads(json_string)

    def to_string(self):
        return json.dumps(self.json_data)

    def set_layer_to_visible(self,layer_id):
        for elem in self.json_data:
            if elem['id'] == layer_id:
                return
        new_elem = {'id' : layer_id}
        self.json_data.append(new_elem)

    def set_layer_not_visible(self,layer_id):
        length = len(self.json_data)
        index = length - 1
        for elem in reversed(self.json_data):
            if elem['id'] == layer_id:
                del self.json_data[index]
            index = index - 1

    def contains_layer(self, layer_id):
        for elem in self.json_data:
            if elem['id'] == layer_id:
                return True
        return False