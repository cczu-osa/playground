#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from os import listdir
from sys import version as python_version
from cgi import parse_header, parse_multipart
from urllib.parse import parse_qs, urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer
from json import dumps, dump

import string
import random


def generate_random_code(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class S(BaseHTTPRequestHandler):
    def _set_headers(self, status_code=200, content_type='text/html'):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def _parse_POST(self):
        ctype, pdict = parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            postvars = parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            postvars = parse_qs(
                    self.rfile.read(length).decode(encoding='utf-8'),
                    keep_blank_values=1)
        else:
            postvars = {}
        return postvars

    def do_GET(self):
        ok = 0
        pathobj = urlparse(self.path)
        if pathobj.path != '/checkcode':
            self._set_headers(status_code=404)
            self.wfile.write(b'page not found')
            return
        params = parse_qs(pathobj.query, keep_blank_values=1)
        params = {k: params[k][0] for k in params}
        if 'code' in params and '.' not in params['code']:
            try:
                # os.remove('/Users/richard/Desktop/' + params['code'])
                os.remove('/home/richard/qqgroup/' + params['code'])
                ok = 1
            except FileNotFoundError:
                pass
        self._set_headers(content_type='text/plain')
        self.wfile.write(str(ok).encode(encoding='utf-8'))

    # def do_HEAD(self):
    #     self._set_headers(status_code=404)

    def do_POST(self):
        pathobj = urlparse(self.path)
        if pathobj.path != '/signup' and pathobj.path != '/signup2':
            self._set_headers(status_code=404)
            self.wfile.write(b'page not found')
            return
        form = self._parse_POST()
        form = {k: form[k][0] for k in form}
        rcode = generate_random_code()
        filepath = '/usr/share/nginx/cczu-dev/signup/' + rcode + '.json'
        # filepath = '/Users/richard/Desktop/' + rcode + '.json'
        # html = ''.join(('<html><head></head>',
        #                '<body><pre><code>',
        #                dumps(form, ensure_ascii=False, indent=4),
        #                '</code></pre></body>'))
        with open(filepath, 'w') as f:
            # f.write(html)
            dump(form, f, ensure_ascii=False, indent=4)
        # with open('/Users/richard/Desktop/' + rcode, 'w') as f:
        with open('/home/richard/qqgroup/' + rcode, 'w') as f:
            f.write('')
        if pathobj.path == '/signup':
            self._set_headers(content_type='application/json')
            self.wfile.write(dumps({'rcode': rcode}).encode(encoding='utf-8'))
        else:
            # /signup2
            self._set_headers()
            ok = True
            if 'name' not in form or form['name'].strip() == '' or \
               'intro' not in form or form['intro'].strip() == '' or \
               'contacts' not in form or form['contacts'].strip() == '':
                ok = False
            a = '成功' if ok else '失败'
            b = """
<p>恭喜，你已经报名成功！</p>
<p>我们为你生成了一个验证码：<strong style="color: red;">""" + rcode + """</strong>，请妥善保管。</p>
<p>你可以通过这个验证码来加预备 QQ 群 530812134，当然，你也可以选择不加预备群，我们会通过你填写的联系方式通知你进行面试。</p>
<p>也可以在 <a href="https://dev.cczu.edu.cn/signup/""" + rcode + """.json">https://dev.cczu.edu.cn/signup/""" + rcode + """.json</a> 查看你的报名信息。</p>
            """
            c = """<p>必填项没填完你就想提交？？？喵喵喵？？？</p>"""
            d = b if ok else c
            html = """
<html>

<head>
  <meta charset="utf-8">
  <meta name="language" content="zh-cn" />
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="x-ua-compatible" content="ie=edge">
  <meta http-equiv="cleartype" content="on">
  <script src="//cdn.bootcss.com/jquery/3.1.1/jquery.min.js"></script>
  <script src="//cdn.bootcss.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
  <link href="//cdn.bootcss.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet">
  <link href="//lug.ustc.edu.cn/wiki/lib/tpl/bootstrap3/assets/bootstrap/flatly/bootstrap.min.css" rel="stylesheet">
  <title>常州大学开发者协会 - 报名成功</title>
</head>
<body>
  <div class="section">
    <div class="container">
      <div class="row">
        <div class="col-md-12">
          <h1>报名"""
            html += a
            html += """</h1>"""
            html += d
            html += """
        </div>
      </div>
    </div>
  </div>
</body>
</html>
            """
            self.wfile.write(html.encode(encoding='utf-8'))


def run(server_class=HTTPServer, handler_class=S, host='127.0.0.1', port=80):
    server_address = (host, port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    elif len(argv) == 3:
        run(host=argv[1], port=int(argv[2]))
    else:
        run()
