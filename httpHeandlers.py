import http
import string
import datetime
import calendar
import urllib.parse
import re
from datetime import datetime
import urllib


class HttpRequest:
  def __init__(self):
    # self._headers = dict()
    self.method = ''
    self.path = ''
    # self.query_params = ''
    self.error = ''
    self.file_type = ''

  def process(self, input):
    init_line, _, other = input.partition('\r\n') 
    self.method, query_string, self.protocol = init_line.split(' ') 
    query_args = query_string.split('?')
  #  print("query_args ", query_args)
    
    self.path = query_args[0]
    if len(query_args) == 1:
      query_args = ''
    else: 
      query_args = query_args[1]
    
      self.query_arguments = dict( 
                                  map( 
                                      lambda x: x.split('='), 
                                      query_args.split('&') 
                                      ) 
                                  ) 
    # self.headers = dict( 
    #                     map( 
    #                         lambda x: x.split(": "), 
    #                         other.partition('\r\n\r\n')[0].strip('\r\n ').split("\r\n") 
    #                         ) 
    #  
    self.path = urllib.parse.unquote(self.path)
    if self.path[0] == '/':
      self.path = self.path[1:]
  
    if self.path in ['', '/', ' ']:
      self.path = 'index.html'
      
    if re.search(r'/\.\.', self.path):
      self.error = 'Root directory escape'
  #  print("Path is: ", self.path)
    self.file_type = self.path.split('.')[-1]
  #  print("self.file_type  is: ", self.file_type )
    if self.method not in ['GET', 'HEAD', 'POST', 'OPTIONS', 'PUT', 'PATCH', 'DELETE', 'TRACE', 'CONNECT']:
      self.error = 'Unknown method'
    # pattern = re.compile(r'(GET|HEAD|POST|OPTIONS|PUT|PATCH|DELETE|TRACE|CONNECT) /([A-Za-z0-9%][A-Za-z0-9%.\-_/ ]*)(\??.*) HTTP')
    # params = re.search(pattern, input)
    # print("Params is: ", params)
    # if params:
    #   self.method, self.path, self.query_params = params[1], params[2], params[3]
    #   self.path = parse.unquote(self.path)
    # #  print("Path is: ", self.path)
    #   if self.path in ['', '/', ' ']:
    #     self.path = 'index.html'
    # print("Now path is: ", self.path)
    
  def givePath(self):
    return self.path
  
  def giveError(self):
    return self.error
  
  def giveMethod(self):
    return self.method
  
  
  
class HTTPResponse():
  def __init__(self): 
    self.headers = dict() 
    self.response = '' 
    self.body = '' 
    self.status = '200 OK' 
    self.http_version = 'HTTP/1.1'

  def add_header(self, header, value): 
    self.headers.update({header: value}) 

  def add_body(self, body): 
    self.body = body
  
  def set_http_version(self, http_version = 'HTTP/1.1'):
    self.http_version = http_version
    
  def set_status(self, code = 200, status = 'OK'):
    self.status = F'{code} {status}'
    # self.add_header(self.http_version, self.status)

  def set_current_date(self):
    now = datetime.now()
    data = F'{calendar.day_abbr[now.weekday()]}, {now.day} {calendar.month_abbr[now.month]} {now.year} {now.hour}:{now.minute}:{now.second} GMT'
    self.add_header('Date', data)

  # def set_content_contentType(self, contentType = 'text/html; charset=UTF-8'):
  #   self.add_header('Content-Type', contentType)

  # def set_transfer_Encoding(self, encoding = 'chunked'):
  #   self.add_header('Transfer-Encoding', encoding)

  def generate_response(self):
    
    self.set_http_version()
    if not self.status:
      self.set_status()
    self.set_current_date()
    # print(self.headers)
    self.response += F'{self.http_version}: {self.status}\r\n'
    for key, value in self.headers.items():
      self.response += f'{key}: {value}\r\n'
    # self.response = F'{self.response}\n\n{self.body}' #Error
    
    if self.body: 
      if type(self.body) == bytes: 
        return self.response.encode() + b'\r\n' + self.body
      else: 
        self.response += '\r\n' + self.body 
    else: 
      self.response += '\r\n'
  #  print("response: ",self.response.encode()[:256],)
    return self.response.encode()