## UnitTesting.py
# Primary Owner: Alex Eckensweiler

import socket
import json
import sys
import standards
import jsonToSqlParms
from cautils import parseCLA

host, port, data = parseCLA.HostPortData()
sys.argv = [sys.argv[0]]

import unittest

class TestStringMethods(unittest.TestCase):

    # Test incorrect JSON
    def test_formatting(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.sendall("hello".encode('utf-8'))
        data = json.loads(s.recv(1024).decode('utf-8'))
        s.close()

        self.assertEqual(data['code'], 'ERROR_01')

    # Test missing operation key
    def test_missing_operation_key(self):

      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.connect((host, port))
      s.sendall('{"animals":"all","fields":"weight"}'.encode('utf-8'))
      data = json.loads(s.recv(1024).decode('utf-8'))
      s.close()

      self.assertEqual(data['code'], 'ERROR_10')

    # Test missing animal key
    def test_missing_animal_key(self):

      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.connect((host, port))
      s.sendall('{"operation":"lookup","fields":"weight"}'.encode('utf-8'))
      data = json.loads(s.recv(1024).decode('utf-8'))
      s.close()

      self.assertEqual(data['code'], 'ERROR_11')

    # Test missing field key
    def test_missing_field_key(self):

      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.connect((host, port))
      s.sendall('{"operation":"lookup","animals":"all"}'.encode('utf-8'))
      data = json.loads(s.recv(1024).decode('utf-8'))
      s.close()

      self.assertEqual(data['code'], 'ERROR_12')

    def test_jsonToSqlParms_simple(self):
        json = '{"operation": "operation-here", "animals": "animal-here", "field": {"height":{"gt":5}}}'
        sql = jsonToSqlParms.JsonToSqlParms(json)
        self.assertEqual(sql, 'height > 5')

    def test_jsonToSqlParms_simple_2(self):
        json = '{"operation": "operation-here", "animals": "animal-here", "field": { "$and": [{"length" : {"lt" : 20} }, {"$or": [{"height": {"lt": 20}}, [{"age":{"eq":10}}]]}, {"$or": [{"height": {"lt": 20}}]}]}}';
        sql = jsonToSqlParms.JsonToSqlParms(json)
        self.assertEqual(sql, '(length < 20 and (height < 20 or (age = 10)) and (height < 20))')

    def test_jsonToSqlParms_nested(self):
        json = '{"operation": "operation-here", "animals": "animal-here", "field": { "$and": [{ "height": { "eq": 5 } }, { "weight": { "lt": 20 } }, { "$or": [{ "height": { "eq": 20 } }, { "length": { "eq": 20 } } ] } ] }}'
        sql = jsonToSqlParms.JsonToSqlParms(json)
        self.assertEqual(sql, '(height = 5 and weight < 20 and (height = 20 or length = 20))')

    def test_jsonToSqlParms_complex(self):
        json = '{"operation": "operation-here", "animals": "animal-here", "field": { "$and": [{ "age": { "eq": 5 } }, { "weight": { "lt": 20 } }, { "$or": [{ "height": { "eq": 20 } }, { "length": { "eq": 20 } }] }, { "$or": [{ "height": { "eq": 20 } }, { "length": { "eq": 20 } }] }] }}'
        sql = jsonToSqlParms.JsonToSqlParms(json)
        self.assertEqual(sql, '(age = 5 and weight < 20 and (height = 20 or length = 20) and (height = 20 or length = 20))')

    def test_jsonToSqlParms_complex_2(self):
        json = '{"operation": "lookup", "animals": "cat", "field": { "$or": [{ "age": { "eq": 5 } }, { "weight": { "lt": 20 } }, { "$or": [{ "height": { "eq": 20 } }, { "length": { "eq": 20 } }] }, { "$or": [{ "height": { "eq": 20 } }, { "length": { "eq": 20 } }] }] }}'
        sql = jsonToSqlParms.JsonToSqlParms(json)
        self.assertEqual(sql, '(age = 5 or weight < 20 or (height = 20 or length = 20) or (height = 20 or length = 20))')

    def test_jsonToSqlParms_complex_3(self):
        json = '{"operation": "lookup", "animals": "cat", "field": { "$or": [{ "age": { "eq": 5 } }, { "weight": { "lt": 20 } }, { "$and": [{ "height": { "eq": 20 } }, { "length": { "eq": 20 } }] }, { "$and": [{ "height": { "eq": 20 } }, { "length": { "eq": 20 } }] }] }}'
        sql = jsonToSqlParms.JsonToSqlParms(json)
        self.assertEqual(sql, '(age = 5 or weight < 20 or (height = 20 and length = 20) or (height = 20 and length = 20))')

    def test_jsonToSqlParms_complex_4(self):
        json = '{"operation":"lookup","animals":"cat","field":{"$or":[{"age":{"eq":"5"}},{"$and":[{"height":{"lt":"50"}},{"weight":{"gt":"500"}},{"age":{"eq":"100"}},{"$or":[{"butts":{"eq":"1"}},{"diabetes":{"ne":"true"}},{"$and":[{"dob":{"eq":"1998"}},{"dod":{"eq":"1999"}},{"$or":{"tail":{"ne":"false"}}},{"color":{"eq":"orange"}}]}]}]}]}}'
        sql = jsonToSqlParms.JsonToSqlParms(json)
        self.assertEqual(sql, '(age = 5 or (height < 50 and weight > 500 and age = 100 and (butts = 1 or diabetes != true or (dob = 1998 and dod = 1999 and tail != false and color = orange))))')

    def test_jsonToSqlParms_gte(self):
        json = '{"operation": "operation-here", "animals": "animal-here", "field": {"height":{"gte":5}}}'
        sql = jsonToSqlParms.JsonToSqlParms(json)
        self.assertEqual(sql, 'height >= 5')

    def test_jsonToSqlParms_lte(self):
        json = '{"operation": "operation-here", "animals": "animal-here", "field": {"height":{"lte":5}}}'
        sql = jsonToSqlParms.JsonToSqlParms(json)
        self.assertEqual(sql, 'height <= 5')

    def test_invalid_operation(self):
        json_string = '{"operation": "operation-here", "animals": "animal-here", "field": {"height":{"ltee":5}}}'
        data = jsonToSqlParms.JsonToSqlParms(json_string)
        self.assertEqual(data['code'], 'ERROR_02')



if __name__ == '__main__':
    unittest.main()