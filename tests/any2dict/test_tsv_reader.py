from mnemocards.any2dict.tsv_reader import TSV


TSV_TXT = """front	back
front1	back1
front2	back2
"""


def test_tsv_reader():
    actual_dict = TSV().loads(TSV_TXT)
    expected_dict = [
        dict(front="front1", back="back1"),
        dict(front="front2", back="back2"),
    ]
    assert actual_dict == expected_dict
