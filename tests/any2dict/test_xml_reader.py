from mnemocards.any2dict.xml_reader import XML


XML_TXT = """
<cards>
    <card>
        <front>front1</front>
        <back>back1</back>
    </card>
    <card>
        <front>front2</front>
        <back>back2</back>
    </card>
</cards>
"""


def test_xml_reader():
    actual_dict = XML().loads(XML_TXT)
    expected_dict = dict(
        cards=dict(
            card=[
                dict(front="front1", back="back1"),
                dict(front="front2", back="back2"),
            ],
        ),
    )
    assert actual_dict == expected_dict
