#----------
# import 
#----------

import plistlib

from mojo.extensions import getExtensionDefault, setExtensionDefault
from robofab.interface.all.dialogs import PutFile, GetFile


#----------
# 
#----------

class ExtentionSettingsManager(object):
    """
    Deals with an extention defaults.
    Keep track of the registered keys, can return all settings of an extention as dict
    Can import and export dict presets as xml
    """

    def __init__(self, defaultKeyBase):
        self.defaultKeyBase = defaultKeyBase
        self.keys = set()

    # defaults

    def register_defaults(self, dict):
        defaults = self.prep_dict_with_prefix(dict, self.defaultKeyBase)
        
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
        defaults = self.prep_dict_with_prefix(dict, self.defaultKeyBase)
        for k, v in defaults:
            setExtensionDefault(k, v)
        self.keys.update(dict.keys())


    def get_defaults(self, fallback=None):
        defaults = {}
        for k in self.keys():
            defaults[k] = self.get_default(k, fallback=fallback)
        return defaults


    def get_default(self, key, fallback=None):
        k = self.defaultKeyBase + key
        return getExtensionDefault(k, fallback=fallback)


    # helpers

    def prep_dict_with_prefix(self, dict, prefix):
        defaults = {}
        for k, v in dict.items():
            defaults[prefix + k] = v
        return defaults
 

    # Presets plist

    def dict_to_plist(self, dict):
        return plistlib.writePlistToString(dict)

    def plist_to_dict(self, plist):
        return plistlib.readPlistFromString(plist)


    # file handling

    def write_preset(self, dict, path):
        f = open(path, w)
        f.write(self.dict_to_plist(dict))
        f.close()

    def write_preset_dialogue(self, dict, message="Save Preset File", fileName=None):
        path = PutFile(message=message, fileName=fileName)
        self.write_preset(dict, path)

    def read_preset(self, path):
        f = open(path, r)
        plist = f.read()
        return self.plist_to_dict(plist)

    def read_preset_dialogue(self, message="Select Preset File", title=None, fileTypes=None):
        path = GetFile(message=message, title=title, fileTypes=fileTypes)
        return self.read_preset(path)