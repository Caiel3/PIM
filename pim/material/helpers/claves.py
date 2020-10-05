from pathlib import Path
import json
import os

class Claves():
    def __str__(self):
        return 

    def __unicode__(self):
        return 
    BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
    with open(os.path.join(BASE_DIR, '..\secrets.json')) as secrets_file:
        secrets = json.load(secrets_file)

    def get_secret(setting, secrets=secrets):
        """Get secret setting or fail with ImproperlyConfigured"""
        try:
            return secrets[setting]
        except KeyError:
            raise ImproperlyConfigured("Set the {} setting".format(setting))

    