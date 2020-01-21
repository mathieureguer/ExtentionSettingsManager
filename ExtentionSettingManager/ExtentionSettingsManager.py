
import plistlib
from collections import UserDict
from mojo.extensions import getExtensionDefault, setExtensionDefault
# from vanilla.dialogs import PutFile, GetFile


class ExtentionSettingsManager(UserDict):
    """
    Deals with an extention defaults.
    Keep track of the registered keys, can return all settings of an extention as dict
    Can import and export dict presets as xml
    """

    def __init__(self, key_prefix):
        super(ExtentionSettingsManager, self).__init__()
        self.key_prefix = key_prefix

    @property
    def data_with_prefixed_keys(self):
        return self.prep_dict_with_prefix(self.data, self.key_prefix)

    # defaults

    def register_defaults(self):
        defaults = self.prep_dict_with_prefix(dict, self.key_prefix)

        # import registerExtensionsDefaults work-around (ripped off from Tal Lemming)
        try:
            from mojo.extensions import registerExtensionsDefaults
        except ImportError:
            def registerExtensionsDefaults(d):
                for k, v in d.items():
                    e = getExtensionDefault(k, fallback="__fallback__")
                    if e == "__fallback__":
                        setExtensionDefault(k, v)

        registerExtensionsDefaults(defaults)
        self.keys.update(dict.keys())

    def set_defaults(self, dict):
        defaults = self.prep_dict_with_prefix(dict, self.key_prefix)
        for k, v in defaults.items():
            setExtensionDefault(k, v)
        self.keys.update(dict.keys())

    def get_defaults(self, fallback=None):
        defaults = {}
        for k in self.keys:
            defaults[k] = self.get_default(k, fallback=fallback)
        return defaults

    def get_default(self, key, fallback=None):
        k = self.key_prefix + key
        return getExtensionDefault(k, fallback=fallback)

    # helpers

    def prep_dict_with_prefix(self, dict, prefix):
        prefixed_dict = {}
        for k, v in dict.items():
            prefixed_dict[prefix + k] = v
        return prefixed_dict

    # Presets plist

    def dict_to_plist(self, dict):
        return plistlib.writePlistToString(dict)

    def plist_to_dict(self, plist):
        return plistlib.readPlistFromString(plist)

    # file handling

    def write_preset(self, dict, path):
        with open(path, "w+") as f:
            f.write(self.dict_to_plist(dict))

    def read_preset(self, path):
        with open(path, "r") as f:
            plist = f.read()
            return self.plist_to_dict(plist)

    # def write_preset_dialog(self, dict, message="Save Preset File", fileName=None):
    #     path = PutFile(message=message, fileName=fileName)
    #     self.write_preset(dict, path)

    # def read_preset_dialog(self, message="Select Preset File", title=None, fileTypes=None):
    #     path = GetFile(message=message, title=title, fileTypes=fileTypes)
    #     return self.read_preset(path)
