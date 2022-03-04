from mnemocards.any2dict.json_reader import JSON


def test_json_reader():
    actual_dict = JSON().loads("""
        [
            {
                "front": "front1",
                "back": "back1"
            },
            {
                "front": "front2",
                "back": "back2"
            }
        ]
    """)
    expected_dict = [
        dict(front="front1", back="back1"),
        dict(front="front2", back="back2"),
    ]
    assert actual_dict == expected_dict
