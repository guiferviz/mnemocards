from mnemocards.any2dict.csv_reader import CSV


CSV_TXT = """front,back
front1,back1
front2,back2
"""


def test_csv_reader():
    actual_dict = CSV().loads(CSV_TXT)
    expected_dict = [
        dict(front="front1", back="back1"),
        dict(front="front2", back="back2"),
    ]
    assert actual_dict == expected_dict
