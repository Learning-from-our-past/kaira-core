from distutils.core import setup
import py2exe
import guitool

setup(windows=[r'guitool/processDialog.py'],
      options = {
          'py2exe' : {
              'packages': ['lxml', 'regex', 'unicodecsv']
          }
      })
