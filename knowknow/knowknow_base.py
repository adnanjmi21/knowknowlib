from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt

from knowknow import utility


class Constants:
    DEFAULT_KEYS = ['fj.fy', 'fy', 'c', 'c.fy']
    data_files = {
        'sociology-wos': 'https://files.osf.io/v1/resources/9vx4y/providers/osfstorage/'
                         '5eded795c67d30014e1f3714/?zip='
    }


class KnowKnow:
    def __init__(self, NB_DIR=None, BASEDIR=None):
        self.NB_DIR = NB_DIR
        self.BASEDIR = BASEDIR

        self.variable_dir = Path(self.BASEDIR, 'variables')

    def save_figure(self, name):
        outdir = self.NB_DIR.joinpath("figures")
        if not outdir.exists():
            outdir.mkdir()
        print("Saving to '%s'" % outdir)
        plt.savefig(str(outdir.joinpath("%s.png" % name)), bbox_inches="tight")

    def get_cnt_keys(self, name):
        avail = self.variable_dir.glob("%s ___ *" % name)
        avail = [x.name for x in avail]
        avail = [x.split("___")[1].strip() for x in avail]
        return avail

    def get_cnt(self, name, keys=None):
        # TODO: add caching
        if keys is None:
            keys = Constants.DEFAULT_KEYS

        cnt = {}

        for k in keys:
            varname = "%s ___ %s" % (name, k)

            # print(k)
            this_cnt = defaultdict(int, utility.named_tupelize(dict(load_variable(varname)), k))
            cnt[k] = this_cnt

        avail = self.get_cnt_keys(name)

        print("Loaded keys: %s" % cnt.keys())
        print("Available keys: %s" % avail)
        return cnt

    def load_variable(self, name):
        import pickle

        nsp = name.split("/")
        if len(nsp) == 1:  # fallback to old ways
            nsp = name.split(".")
            collection = nsp[0]
            varname = ".".join(nsp[1:])
            name = "/".join([collection, varname])
        elif len(nsp) == 2:
            collection, varname = nsp
        else:
            raise Exception("idk how to parse this... help")

        if not self.variable_dir.joinpath(collection).exists():
            print("collection", collection, "does not exist...")
            print("attempting to load from OSF")

            if collection not in Constants.data_files:
                raise Exception("no data file logged for '%s'" % collection)

            zip_dest = Path(self.BASEDIR, "variables", "%s.zip" % collection)
            if not zip_dest.exists():
                self.download_file(Constants.data_files[collection], zip_dest)

            print("Extracting...", str(zip_dest))
            import zipfile
            with zipfile.ZipFile(str(zip_dest), 'r') as zip_ref:
                zip_ref.extractall(str(zip_dest.parent.joinpath(collection)))

        try:
            return pickle.load(self.variable_dir.joinpath(name).open('rb'))
        except FileNotFoundError:
            raise utility.VariableNotFound(name)


