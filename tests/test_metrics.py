"""Regression checks for public data integrity and cached-image preservation."""

import contextlib
from datetime import date,timedelta
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
import refresh_metrics as refresh
from render_profile import languages
from verify_profile import validate_svg


def calendar_html(missing_count=False,missing_day=False):
    start=date(2026,5,24)
    chunks=[]
    for i in range(180):
        if missing_day and i==50:
            continue
        day=start+timedelta(days=i)
        count=12 if i==0 else 0
        chunks.append(f'<td id="d{i}" data-date="{day}" data-level="{3 if count else 0}"></td>')
        if missing_count and i==0:
            continue
        label="12 contributions" if count else "No contributions"
        chunks.append(f'<tool-tip for="d{i}">{label} on a date.</tool-tip>')
    return ''.join(chunks)


class PublicMetricsTests(unittest.TestCase):
    def test_actual_tooltip_count_is_used_instead_of_level(self):
        parser=refresh.Contributions();parser.feed(calendar_html())
        snapshot=parser.snapshot(date(2026,11,19))
        self.assertEqual(snapshot["days"][0]["count"],12)
        self.assertEqual(sum(d["count"] for d in snapshot["days"]),12)

    def test_missing_count_and_missing_day_both_fail_closed(self):
        for options in [{"missing_count":True},{"missing_day":True}]:
            with self.subTest(options=options):
                parser=refresh.Contributions();parser.feed(calendar_html(**options))
                with self.assertRaises(ValueError):parser.snapshot(date(2026,11,19))

    def test_stale_calendar_is_not_published_as_current(self):
        parser=refresh.Contributions();parser.feed(calendar_html())
        with self.assertRaises(ValueError):parser.snapshot(date(2026,12,1))

    def test_notebook_markup_and_fork_bytes_do_not_change_code_shares(self):
        data={"repositories":[
            {"fork":False,"languages":{"Java":100,"Python":100,"Jupyter Notebook":50000,"HTML":6000}},
            {"fork":True,"languages":{"JavaScript":90000}}]}
        self.assertEqual(languages(data),{"Java":100,"Python":100})

    def test_failed_refresh_does_not_write_assets(self):
        with patch.object(refresh,"snapshot",side_effect=OSError("offline")), \
             patch.object(refresh,"write_outputs") as write, \
             patch.object(sys,"argv",["refresh_metrics.py"]), \
             contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(refresh.main(),1)
            write.assert_not_called()

    def test_native_render_rejects_active_content_and_remote_images(self):
        samples=['<script>bad()</script>',
                 '<image href="https://example.com/remote.png"/>',
                 '<foreignObject><div xmlns="http://www.w3.org/1999/xhtml" onclick="bad()">bad</div></foreignObject>']
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/"native.svg"
            for sample in samples:
                with self.subTest(sample=sample):
                    path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="480" height="800">{sample}</svg>',encoding="utf-8")
                    with self.assertRaises(ValueError):validate_svg(path,allow_native=True)


if __name__=="__main__":
    unittest.main()
