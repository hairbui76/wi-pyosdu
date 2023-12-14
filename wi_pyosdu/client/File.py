from .Token import access_token, auth_headers
from ..config import *
from .Http import *
from ..models.Record import Record
from ..models.FileGeneric import FileGeneric
import json

__FILE_BASE_URL = f'{OSDU_BASE}/api/file/v2'
def file_info():
  resp = httpGet(f'{__FILE_BASE_URL}/info', headers=auth_headers())
  print(resp.content.decode('utf-8'))

def __file_get_upload_url():
  resp = httpGet(f'{__FILE_BASE_URL}/files/uploadURL', headers=auth_headers())
  return json.loads(resp.content)

def file_get_upload_url():
  return __file_get_upload_url()

def __file_upload_file(signed_url, local_file_path):
  resp = httpPutFile(signed_url, local_file_path)
  print(resp.status_code, resp.content)

def file_upload_file(signed_url, local_file_path):
  __file_upload_file(signed_url, local_file_path)

def __file_add_metadata(filesource, filename):
  dataset = FileGeneric(filesource, filename)
  resp = httpPostJson(f'{__FILE_BASE_URL}/files/metadata', json=dataset.todict(), headers=auth_headers())
  print(resp.status_code, resp.content)

def file_add_metadata(filesource, filename):
  __file_add_metadata(filesource, filename) 

def file_ingest_file(filename, local_file_path):
  obj = __file_get_upload_url()
  file_id = obj['FileID']
  file_source = obj['Location']['FileSource']
  signed_url = obj['Location']['SignedURL']
  print(obj)
  __file_upload_file(signed_url, local_file_path)
  __file_add_metadata(file_source, filename)

def file_delete_record(file_record_id):
  resp = httpDelete(f'{__FILE_BASE_URL}/files/{file_record_id}/metadata', headers=auth_headers())
  print(resp.status_code, resp.content)

def file_get_file_list():
  resp = httpPostJson(f'{__FILE_BASE_URL}/getFileList', json = {
    "TimeFrom": "2022-01-10T00:00:00.000Z",
    "TimeTo": "2023-12-01T00:00:00.000Z",
    "PageNum": 0,
    "Items": 100,
    "UserID": "demo@osdu.local"
  }, headers=auth_headers())
  return json.loads(resp.content)

def file_get_file_signed_url(srn):
  resp = httpPostJson(f'{__FILE_BASE_URL}/delivery/getFileSignedUrl', json = {
    "srns": [srn]  
  }, headers = auth_headers())
  return json.loads(resp.content)
