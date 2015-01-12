from distutils.core import setup
import py2exe
import guitool

setup(windows=[{ "script" : r'guitool/processDialog.py',
                 "icon_resources" : [(1,"favicon.ico")],
                 "dest_base" : "AnalyzerTool"
               }],
      zipfile = None,
      options = {
          'py2exe' : {
              'packages': ['lxml', 'regex', 'unicodecsv']
          }
      })
