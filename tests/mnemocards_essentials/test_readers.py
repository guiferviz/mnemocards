import textwrap

import pytest

from mnemocards_essentials import readers


class TestReader:
    def test_load(self, mocker, tmp_path):
        mocker.patch.object(readers.Reader, "__abstractmethods__", set())
        file = tmp_path / "joke.txt"
        file.write_text(":-P")
        reader = readers.Reader()  # type: ignore
        reader.loads = mocker.Mock()
        reader.load(file)
        reader.loads.assert_called_with(":-P")


class TestInferReader:
    def test_get_reader_known_extension(self):
        reader = readers.InferReader()
        actual = reader._get_reader("file.csv")
        assert type(actual) == readers.CSV

    def test_get_reader_unknown_extension(self):
        reader = readers.InferReader()
        with pytest.raises(
            ValueError, match="I cannot infer reader for file `file.unknown`"
        ):
            reader._get_reader("file.unknown")

    def test_load(self, mocker):
        reader_mock = mocker.Mock()
        mocker.patch.object(
            readers.InferReader, "_get_reader", return_value=reader_mock
        )
        reader = readers.InferReader()
        reader.load("file.unknown")
        reader_mock.load.assert_called_with("file.unknown")


class TestCSV:
    @pytest.fixture
    def input_text(self):
        return textwrap.dedent(
            """
                front,back
                front1,back1
                front2,back2
            """[
                1:
            ]
        )

    def test_loads(self, input_text):
        actual_dict = readers.CSV().loads(input_text)
        expected_dict = [
            dict(front="front1", back="back1"),
            dict(front="front2", back="back2"),
        ]
        assert actual_dict == expected_dict


class TestTSV:
    @pytest.fixture
    def input_text(self):
        return textwrap.dedent(
            """
                front	back
                front1	back1
                front2	back2
            """[
                1:
            ]
        )

    def test_loads(self, input_text):
        actual_dict = readers.TSV().loads(input_text)
        expected_dict = [
            dict(front="front1", back="back1"),
            dict(front="front2", back="back2"),
        ]
        assert actual_dict == expected_dict


class TestJSON:
    @pytest.fixture
    def input_text(self):
        return textwrap.dedent(
            """
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
            """
        )

    def test_loads(self, input_text):
        actual_dict = readers.JSON().loads(input_text)
        expected_dict = [
            dict(front="front1", back="back1"),
            dict(front="front2", back="back2"),
        ]
        assert actual_dict == expected_dict


class TestTOML:
    @pytest.fixture
    def input_text(self):
        return textwrap.dedent(
            """
                [[cards]]
                front = "front1"
                back = "back1"

                [[cards]]
                front = "front2"
                back = "back2"
            """
        )

    def test_loads(self, input_text):
        actual_dict = readers.TOML().loads(input_text)
        expected_dict = dict(
            cards=[
                dict(front="front1", back="back1"),
                dict(front="front2", back="back2"),
            ],
        )
        assert actual_dict == expected_dict

    def test_fail_when_toml_is_not_installed(self, mocker):
        mocker.patch.object(readers, "toml_exists", False)
        with pytest.raises(
            ImportError, match="toml package is required to read toml files"
        ):
            readers.TOML()


class TestXML:
    @pytest.fixture
    def input_text(self):
        return textwrap.dedent(
            """
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
        )

    def test_loads(self, input_text):
        actual_dict = readers.XML().loads(input_text)
        expected_dict = dict(
            cards=dict(
                card=[
                    dict(front="front1", back="back1"),
                    dict(front="front2", back="back2"),
                ],
            ),
        )
        assert actual_dict == expected_dict

    def test_fail_when_xmltodict_is_not_installed(self, mocker):
        mocker.patch.object(readers, "xmltodict_exists", False)
        with pytest.raises(
            ImportError, match="xmltodict package is required to read xml files"
        ):
            readers.XML()


class TestYAML:
    @pytest.fixture
    def input_text(self):
        return textwrap.dedent(
            """
                - front: front1
                  back: back1
                - front: front2
                  back: back2
            """
        )

    def test_loads(self, input_text):
        actual_dict = readers.YAML().loads(input_text)
        expected_dict = [
            dict(front="front1", back="back1"),
            dict(front="front2", back="back2"),
        ]
        assert actual_dict == expected_dict
