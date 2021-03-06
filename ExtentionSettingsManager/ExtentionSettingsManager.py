
import plistlib
from collections import UserDict
import vanilla
from mojo.extensions import getExtensionDefault, setExtensionDefault

INPUT_MAP = {
    "direct_get_set": [vanilla.TextEditor, vanilla.EditText, vanilla.TextBox, vanilla.CheckBox, vanilla.ComboBox],
    "index_get_set": [vanilla.PopUpButton],
}


class ExtentionSettingsManager(UserDict):
    """
    Deals with an extention defaults.
    Keep track of the registered keys, can return all settings of an extention as dict
    Can import and export dict presets as xml
    """

    def __init__(self, key_prefix):
        super(ExtentionSettingsManager, self).__init__()
        self.key_prefix = key_prefix

        self._input_map = {}

    # ----------------------------------------
    # extention defaults

    def register_extention_defaults(self):
        # import registerExtensionsDefaults work-around (ripped off from Tal Lemming)
        try:
            from mojo.extensions import registerExtensionsDefaults
        except ImportError:
            def registerExtensionsDefaults(d):
                for k, v in self.data_with_prefix.items():
                    e = getExtensionDefault(k, fallback="__fallback__")
                    if e == "__fallback__":
                        setExtensionDefault(k, v)
        registerExtensionsDefaults(self.data_with_prefix)

    def save_extention_settings(self):
        for key, value in self.data.items():
            self._set_extention_setting(key, value)

    def _set_extention_setting(self, key, value):
        setExtensionDefault(self.key_with_prefix(key), value)

    def load_extention_settings(self, fallback=None):
        defaults = {}
        for key in self.data.keys():
            defaults[key] = self._get_extention_setting(key, fallback=fallback)
        self.data.update(defaults)

    def _get_extention_setting(self, key, fallback=None):
        return getExtensionDefault(self.key_with_prefix(key), fallback=fallback)

    # ----------------------------------------
    # helpers

    @property
    def data_with_prefix(self):
        prefixed_dict = {}
        for k, v in self.data.items():
            prefixed_dict[self.key_with_prefix(k)] = v
        return prefixed_dict

    def key_with_prefix(self, key):
        return self.key_prefix + key

    def data_from_prefix(self, prefixed_dict):
        cleaned_dict = {}
        for key, value in prefixed_dict.items():
            cleaned_dict[self.key_from_prefix(key)] = value
        self.data = cleaned_dict

    def key_from_prefix(self, prefixed_key):
        assert prefixed_key.startswith(self.key_prefix), f"{prefix_key} key does not start with registerted prefix {self.key_prefix}"
        return prefixed_key[len(self.key_prefix):]

    # ----------------------------------------
    # vanilla input helpers

    def register_input(self, key, input_object):
        self._input_map[key] = input_object
        # self[key] = self._get_input_value(input_object)

    def load_settings_from_input(self):
        for key, input_object in self._input_map.items():
            self[key] = self._get_input_value(input_object)

    def set_input_from_default(self):
        for key, input_object in self._input_map.items():
            if key in self.keys():
                self._set_input_value(input_object, self[key])

    def _get_input_value(self, input_object):
        if type(input_object) in INPUT_MAP["direct_get_set"]:
            return input_object.get()
        elif type(input_object) in INPUT_MAP["index_get_set"]:
            return input_object.getitems()[input_object.get()]

    def _set_input_value(self, input_object, value):
        if type(input_object) in INPUT_MAP["direct_get_set"]:
            input_object.set(value)
        elif type(input_object) in INPUT_MAP["index_get_set"]:
            index = input_object.getItems().index(value)
            input_object.set(index)

    # ----------------------------------------
    # Import Export

    def to_plist(self, prefixed=True):
        if prefix_key:
            out_data = self.data_with_prefix
        else:
            out_data = self.data
        return plistlib.writePlistToString(out_data)

    def from_plist(self, plist, prefixed=True):
        raw_data = plistlib.readPlistFromString(plist)
        if prefixed:
            self.data_from_prefix(raw_data)
        else:
            self.data.update(raw_data)

    def write_preset(self, dict, path, prefixed=True):
        with open(path, "w+") as f:
            f.write(self.to_plist(prefixed=prefixed))

    def read_preset(self, path, prefixed=True):
        with open(path, "r") as f:
            plist = f.read()
            self.from_plist(plist, prefixed=prefixed)
