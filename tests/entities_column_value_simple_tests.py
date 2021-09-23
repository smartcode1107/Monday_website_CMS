import collections
import json
from datetime import datetime
from nose.tools import ok_, eq_, raises

from moncli import entities as en, error as e
from moncli.enums import *


def test_should_return_empty_text_column_value():

    # Arrange
    id = 'text_1'
    column_type = ColumnType.text
    title = 'Text 1'
    column_value = en.cv.create_column_value(column_type, id=id, title=title)

    # Act
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.value, None)
    eq_(format, '')


def test_should_return_text_column_value_with_loaded_text():

    # Arrange
    id = 'text_2'
    column_type = ColumnType.text
    title = 'Text 2'
    text = 'Hello, Grandma!'
    column_value = en.cv.create_column_value(
        column_type, id=id, title=title, value=json.dumps(text))

    # Act
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.value, text)
    eq_(format, text)


def test_should_return_empty_text_column_value_when_value_is_set_to_native_default():

    # Arrange
    id = 'text_3'
    column_type = ColumnType.text
    title = 'Text 3'
    text = 'Hello, Grandma!'
    column_value = en.cv.create_column_value(
        column_type, id=id, title=title, value=json.dumps(text))

    # Act
    column_value.value = None

    # Assert
    eq_(column_value.value, None)


def test_should_return_text_column_with_value_when_setting_an_int_value():

    # Arrange
    id = 'text_4'
    column_type = ColumnType.text
    title = 'Text 4'
    text = 12345
    column_value = en.cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.value = text

    # Assert
    eq_(column_value.value, str(text))


def test_should_return_text_column_with_value_when_setting_an_float_value():

    # Arrange
    id = 'text_5'
    column_type = ColumnType.text
    title = 'Text 5'
    text = 123.45
    column_value = en.cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.value = text
    # Assert
    eq_(column_value.value, str(text))


@raises(e.ColumnValueError)
def test_should_throw_exception_when_setting_an_invalid_value():

    # Arrange
    id = 'text_5'
    column_type = ColumnType.text
    title = 'Text 5'
    text = {'value': 123.45}
    column_value = en.cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.value = text

    # Assert
    eq_(column_value.value, str(text))


def test_should_create_a_people_column_value_with_no_api_input_data():

    # Arrange

    id = 'people_1'
    column_type = ColumnType.people
    title = 'people 1'
    value = None

    column_value = en.cv.create_column_value(
        column_type, id=id, title=title, value=value)

    # Act
    format = column_value.format()

    # Assert

    eq_(format, {})


def test_should_create_a_people_column_value_with_no_api_input_data():

    # Arrange

    id = 'people_1'
    column_type = ColumnType.people
    title = 'people 1'
    value_dict = {'personsAndTeams': [
        {'id': 134, 'kind': 'person'}, {'id': 11234, 'kind': 'person'}]}
    value = json.dumps(value_dict)
    column_value = en.cv.create_column_value(
        column_type, id=id, title=title, value=value)

    # Act
    person_value = column_value.format()['personsAndTeams']
    format = person_value[0]

    # Assert

    eq_(format['id'], 134)



def test_should_set_people_column_value_to_none():
    # Arrange

    id = 'people_1'
    column_type = ColumnType.people
    title = 'people 1'
    column_value = en.cv.create_column_value(column_type, id=id, title=title)

    # Act

    column_value.value = None

    # Assert

    eq_(column_value.value, [])



@raises(e.ColumnValueError)
def test_should_throw_an_exception_when_setting_an_invalid_value_to_people_column_value():

    id = 'people_1'
    column_type = ColumnType.people
    title = 'people 1'
    value_dict = {'personsAndTeams': [
        {'id': 123, 'kind': 'not person'}, {'id': 11234, 'kind': 'person'}]}
    value = json.dumps(value_dict)
    column_value = en.cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.value = value


def test_should_create_a_number_column_value_with_no_api_input_data():

    # Arrange
    id = 'value_1'
    title = "value"
    column_type = ColumnType.numbers
    column_value = en.cv.create_column_value(column_type, id=id, title=title)

    # Act
    format = column_value.format()

    # Assert
    eq_(format, "")


def test_should_create_a_number_column_value_with_api_input_data():

    id = 'value_1'
    title = "value"
    column_type = ColumnType.numbers
    value = "123"
    column_value = en.cv.create_column_value(
        column_type, id=id, title=title, value=value)

    # Act
    format = column_value.format()

    # Assert
    eq_(format, value)


def test_should_set_number_column_value_to_none_to_value():

    # Arrange
    id = 'value_1'
    title = "value"
    column_type = ColumnType.numbers
    value = None
    column_value = en.cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.value = value

    # Assert
    eq_(column_value.value, None)


def test_should_set_number_column_value_to_int_or_float_to_value():
    id = 'value_1'
    title = "value"
    column_type = ColumnType.numbers
    value = 123.32
    column_value = en.cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.value = value

    # Assert
    eq_(column_value.value, value)



@raises(e.ColumnValueError)
def test_should_set_number__an_improper_string_to_column_value_and_error():
    id = 'value_1'
    title = "value"
    column_type = ColumnType.numbers
    value = "just a number"
    column_value = en.cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.value = value


def test_should_set_number_column_value_to__a_valid_string_value():
    id = 'value_1'
    title = "value"
    column_type = ColumnType.numbers
    value = "123.32"
    column_value = en.cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.value = value

    # Assert
    eq_(column_value.value, float(value))


def test_should_create_date_column_value_with_no_input_data():

    # Arrange
    id = 'date_1'
    title = 'date'
    column_type = ColumnType.date
    value=None
    column_value = en.cv.create_column_value(column_type, id=id, title=title,value=value)

    # Act
    format = column_value.format()

    # Assert
    eq_(format, {})


def test_should_create_date_column_value_with_input_data():

    # Arrange

    id = 'date_1'
    title = 'date'
    column_type = ColumnType.date
    date_value = datetime(2020,12,12,12,20,30)
    date_value = {
        'date': str(date_value.date()),
        'time': str(date_value.time())
    }
    value = json.dumps(date_value)
    column_value = en.cv.create_column_value(column_type, id=id, title=title,value=value)

    # Act
    format = column_value.format()

    # Assert
    eq_(format['date'],'2020-12-12')
    eq_(format['time'], '12:20:30')


def test_should_set_date_value_to_none_to_value():
    id = 'date_1'
    title = 'date'
    column_type = ColumnType.date
    column_value = en.cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.value=None

    # Assert
    eq_(column_value.value,None)

def test_should_set_datetime_input_value_to_date_column_value():
    id = 'date_1'
    title = 'date'
    column_type = ColumnType.date
    value = datetime(2020, 12, 12, 12, 30, 12)
    column_value = en.cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.value=value

    # Assert
    eq_(column_value.value,value)


@raises(e.ColumnValueError)
def test_should_set_invalid_unix_timestamp_to_date_column_value():
    id = 'date_1'
    title = 'date'
    column_type = ColumnType.date
    value = 999999999999
    column_value = en.cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.value=value


def test_should_set_valid_unix_timestamp_to_date_column_value():
    id = 'date_1'
    title = 'date'
    column_type = ColumnType.date
    value = 9999999999
    date_value=datetime(2286, 11, 20, 23, 16, 39)
    date = str(date_value.date())
    column_value = en.cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.value=value
    format = column_value.format()

    # Assert
    eq_(format['date'],date)


@raises(e.ColumnValueError)
def test_should_set_invalid_monday_simple_string_to_date_column_value():
    id = 'date_1'
    title = 'date'
    column_type = ColumnType.date
    value = "202020-120-120 123:234:233"
    column_value = en.cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.value=value


def test_should_set_monday_simple_string_to_date_column_value():
    id = 'date_1'
    title = 'date'
    column_type = ColumnType.date
    value = "2020-12-12 12:24:23"
    date_value = datetime(2020,12,12,12,24,23)
    column_value = en.cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.value=value
    format = column_value.format()
    # Assert
    eq_(format['date'],str(date_value.date()))


def test_should_set_none_to_dropdown_column_value():

    # Arrange

    id = 'dropdown_1'
    column_type = ColumnType.dropdown
    title = 'drop down 1'
    value = None

    column_value = en.cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.value = value

    # Assert
    eq_(column_value.value, [])


def test_should_create_a_dropdown_column_value_with_no_api_input_data():

    # Arrange
    id = 'dropdown_1'
    column_type = ColumnType.dropdown
    title = 'drop down 1'
    value = None
    column_value = en.cv.create_column_value(column_type, id=id, title=title,value=value)

    # Act
    format = column_value.format()

    # Assert
    eq_(format, {})


def test_should_create_a_dropdown_column_value_with_api_input_data():

    # Arrange
    id = 'dropdown_1'
    column_type = ColumnType.dropdown
    title = 'drop down 1'
    api_value = {
        'ids': [1],
        'changed_at': '2021-09-19T21:51:49.093Z'
    }
    settings = {
        "hide_footer": False,
        "labels": [
            {"id": 1, "name": "Date"},
            {"id": 2, "name": "Datetime"},
            {"id": 3, "name": "Text"},
            {"id": 4, "name": "Text Array"},
            {"id": 5, "name": "Text with Label"},
            {"id": 6, "name": "Numeric"},
            {"id": 7, "name": "Boolean"},
            {"id": 8, "name": "User Emails"}
        ]
    }
    value = json.dumps(api_value)
    settings_str = json.dumps(settings)
    column_value = en.cv.create_column_value(
        column_type, id=id, title=title, value=value, settings_str=settings_str)

    # Act 
    format = column_value.format()

    # Assert    
    eq_(format['ids'], [1])


@raises(e.ColumnValueError)
def test_should_set_invalid_integer_to_dropdown_column_value():
    
    # Arrange
    id = 'dropdown_1'
    column_type = ColumnType.dropdown
    title = 'drop down 1'
    settings = {
        "hide_footer": False,
        "labels": [
            {"id": 1, "name": "Date"},
            {"id": 2, "name": "Datetime"},
            {"id": 3, "name": "Text"},
            {"id": 4, "name": "Text Array"},
            {"id": 5, "name": "Text with Label"},
            {"id": 6, "name": "Numeric"},
            {"id": 7, "name": "Boolean"},
            {"id": 8, "name": "User Emails"}
        ]
    }
    settings_str = json.dumps(settings)
    column_value = en.cv.create_column_value(column_type, id=id, title=title,settings_str =settings_str)

    # Act
    column_value.value.append(123)
    column_value.format()


@raises(e.ColumnValueError)
def test_should_set_invalid_string_to_dropdown_index_column_value():
    
    # Arrange
    id = 'dropdown_1'
    column_type = ColumnType.dropdown
    title = 'drop down 1'
    settings = {
        "hide_footer": False,
        "labels": [
            {"id": 1, "name": "Date"},
            {"id": 2, "name": "Datetime"},
            {"id": 3, "name": "Text"},
            {"id": 4, "name": "Text Array"},
            {"id": 5, "name": "Text with Label"},
            {"id": 6, "name": "Numeric"},
            {"id": 7, "name": "Boolean"},
            {"id": 8, "name": "User Emails"}
        ]
    }
    settings_str = json.dumps(settings)
    column_value = en.cv.create_column_value(column_type, id=id, title=title,settings_str =settings_str)

    # Act
    column_value.value.append('42069')
    column_value.format()


@raises(e.ColumnValueError)
def test_should_set_invalid_string_to_dropdown_label_column_value():
    
    # Arrange
    id = 'dropdown_1'
    column_type = ColumnType.dropdown
    title = 'drop down 1'
    settings = {
        "hide_footer": False,
        "labels": [
            {"id": 1, "name": "Date"},
            {"id": 2, "name": "Datetime"},
            {"id": 3, "name": "Text"},
            {"id": 4, "name": "Text Array"},
            {"id": 5, "name": "Text with Label"},
            {"id": 6, "name": "Numeric"},
            {"id": 7, "name": "Boolean"},
            {"id": 8, "name": "User Emails"}
        ]
    }
    settings_str = json.dumps(settings)
    column_value = en.cv.create_column_value(column_type, id=id, title=title,settings_str =settings_str)

    # Act
    column_value.value.append("dateTime")
    column_value.format()


def test_should_create_a_status_column_value_with_no_api_input_data():

    # Arrange
    id = 'status_1'
    title = "status"
    column_type = ColumnType.status
    column_value = en.cv.create_column_value(column_type, id=id, title=title)

    # Act
    format = column_value.format() 
    
    #Assert
    eq_(format, {})


def test_should_create_a_status_column_value_with_api_input_data():

    # Arrange
    id = 'status_1'
    title = "status"
    column_type = ColumnType.status
    index_value = {
        'index': 1,
    }
    settings = {'labels': {'0': 'Working on it', '1': 'Done', '2': 'Stuck'}}
    settings_str = json.dumps(settings)
    value = json.dumps(index_value)
    column_value = en.cv.create_column_value(column_type, id=id, title=title,value=value,settings_str=settings_str)

    # Act
    format = column_value.format()

    #Assert
    eq_(column_value.value,'Done')
    eq_(format['index'], 1)


def test_should_set_none_to_status_value():
    # Arrange
    id = 'status_1'
    title = "status"
    column_type = ColumnType.status
    column_value = en.cv.create_column_value(column_type, id=id, title=title)

    # Act 
    column_value.value = None

    #Assert
    eq_(column_value.value, None)


@raises(e.ColumnValueError)
def test_should_set_invalid_string_label_value_to_status_value():
    # Arrange
    id = 'status_1'
    title = "status"
    column_type = ColumnType.status
    settings = {'labels': {'0': 'Working on it', '1': 'Done', '2': 'Stuck'}}
    settings_str = json.dumps(settings)
    column_value = en.cv.create_column_value(column_type, id=id, title=title,settings_str=settings_str)

    # Act 
    column_value.value = "Not Done"


def test_should_set_a_status_column_value_with_string_label_value():

    # Arrange
    id = 'status_1'
    title = "status"
    column_type = ColumnType.status
    settings = {'labels': {'0': 'Working on it', '1': 'Done', '2': 'Stuck'}}
    settings_str = json.dumps(settings)
    value = 'Done'
    column_value = en.cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.settings_str=settings_str
    column_value.value=value

    #Assert
    eq_(column_value.value,'Done')


@raises(e.ColumnValueError)
def test_should_set_invalid_integer_to_status_index_value():
    # Arrange
    id = 'status_1'
    title = "status"
    column_type = ColumnType.status
    settings = {'labels': {'0': 'Working on it', '1': 'Done', '2': 'Stuck'}}
    settings_str = json.dumps(settings)
    value = 123
    column_value = en.cv.create_column_value(column_type, id=id, title=title,settings_str=settings_str)

    # Act 

    column_value.value = value


def test_should_set_a_status_column_value_with_valid_integer_index_value():

    # Arrange
    id = 'status_1'
    title = "status"
    column_type = ColumnType.status
    settings = {'labels': {'0': 'Working on it', '1': 'Done', '2': 'Stuck'}}
    settings_str = json.dumps(settings)
    column_value = en.cv.create_column_value(column_type, id=id, title=title)
    value = 1

    # Act
    column_value.settings_str=settings_str
    column_value.value = value

    #Assert
    eq_(column_value.value,'Done')


@raises(e.ColumnValueError)
def test_should_set_invalid_string_to_status_index_value():
    # Arrange
    id = 'status_1'
    title = "status"
    column_type = ColumnType.status
    settings = {'labels': {'0': 'Working on it', '1': 'Done', '2': 'Stuck'}}
    settings_str = json.dumps(settings)
    value = '123'
    column_value = en.cv.create_column_value(column_type, id=id, title=title,settings_str=settings_str)

    # Act 
    column_value.value = value


def test_should_set_a_status_column_value_with_valid_integer_index_value():

    # Arrange
    id = 'status_1'
    title = "status"
    column_type = ColumnType.status
    value = "1"
    settings = {'labels': {'0': 'Working on it', '1': 'Done', '2': 'Stuck'}}
    settings_str = json.dumps(settings)
    column_value = en.cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.settings_str=settings_str
    column_value.value=value

    #Assert
    eq_(column_value.value,'Done')