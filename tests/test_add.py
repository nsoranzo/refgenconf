
""" Tests for RefGenConf.add. These tests depend on successful completion of tests is test_1pull_asset.py """

import pytest
import mock
from refgenconf import RefGenConf


class TestAdd:
    @pytest.mark.parametrize(["pth", "gname", "aname", "tname"],
                             [("bogus/path/file.txt", "rCRSd", "fasta", "default"),
                              ("bogus/path/file.txt", "rCRSd", "fasta", "default")])
    def test_nonexistent_file(self, cfg_file, pth, gname, aname, tname):
        rgc = RefGenConf(filepath=cfg_file)
        with pytest.raises(OSError):
            rgc.add(pth, gname, aname, tname)

    @pytest.mark.parametrize(["gname", "aname", "tname"],
                             [("human_repeats", "fasta", "default"),
                              ("rCRSd", "fasta", "default")])
    def test_preexisting_asset_prompt(self, cfg_file, gname, aname, tname):
        rgc = RefGenConf(filepath=cfg_file)
        path = rgc.seek(genome_name=gname, asset_name=aname, tag_name=tname)
        with mock.patch("refgenconf.refgenconf.query_yes_no", return_value=False):
            assert not rgc.add(path, gname, aname, tname)

    @pytest.mark.parametrize(["gname", "aname", "tname"],
                             [("human_repeats", "fasta", "default"),
                              ("rCRSd", "fasta", "default")])
    def test_force_overwrite_asset(self, cfg_file, gname, aname, tname):
        rgc = RefGenConf(filepath=cfg_file)
        path = rgc.seek(genome_name=gname, asset_name=aname, tag_name=tname, enclosing_dir=True)
        gname = gname + "_new"
        assert rgc.add(path, gname, aname, tname)
        assert rgc.add(path, gname, aname, tname, force=True)

    @pytest.mark.parametrize(["gname", "aname", "tname"],
                             [("human_repeats", "fasta", "default"),
                              ("rCRSd", "fasta", "default")])
    def test_nofile(self, cfg_file, gname, aname, tname):
        rgc = RefGenConf(filepath=cfg_file)
        pth = rgc.seek(gname, aname, tname, enclosing_dir=True)
        rgc_new = RefGenConf()
        assert rgc_new.add(pth, gname, aname, tname, seek_keys={"file": "b"})