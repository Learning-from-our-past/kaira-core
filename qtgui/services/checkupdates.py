import http.client
import json
import re
import webbrowser
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtCore import pyqtSlot, QObject
from PyQt5.QtWidgets import QDialog
from app_information import ABOUT_INFORMATION
from qtgui.layouts.ui_updatedialog import Ui_CheckUpdatesDialog
from distutils.version import StrictVersion

class UpdateDialog(QDialog):
    """
    Dialog to check the updates and to navigate to downloads page in Github.
    """
    def __init__(self, their_version=None, parent=None):
        super(UpdateDialog, self).__init__(parent)
        self.ui = Ui_CheckUpdatesDialog()
        self.ui.setupUi(self)

        self.ui.goToDownloads_Button.clicked.connect(self._go_to_downloads)
        self.ui.currentVersion_label.setText(self.ui.currentVersion_label.text() + ABOUT_INFORMATION['version'])

        if their_version is None:
            self.worker = CheckUpdatesWorker(ABOUT_INFORMATION['github_api_host'],
                                             ABOUT_INFORMATION['github_api_releases_url'],
                                             ABOUT_INFORMATION['version'])
            self.worker.threadResultsSignal.connect(self._updates_information_retrieved)

            self.thread = QThread()
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.check_updates)
            self.thread.start()
        else:
            self.ui.newVersion_label.setText(self.ui.newVersion_label.text() + their_version)

    def _updates_information_retrieved(self, result):
        self.thread.quit()
        if result['status'] == 'success':
            # Update version info to the dialog
            their_version = result['their_version']
            self.ui.newVersion_label.setText(self.ui.newVersion_label.text() + their_version)
        else:
            self.ui.newVersion_label.setText(self.ui.newVersion_label.text() + 'fetch failed')

    def _go_to_downloads(self):
        webbrowser.open(ABOUT_INFORMATION['releases_url'])


class CheckUpdatesOnStartup:
    """
    Helper class to check updates automatically on background when application starts up.
    """
    def __init__(self):
        # Retrieve update information on background:
        self.worker = CheckUpdatesWorker(ABOUT_INFORMATION['github_api_host'],
                                         ABOUT_INFORMATION['github_api_releases_url'],
                                         ABOUT_INFORMATION['version'])

        self.worker.threadResultsSignal.connect(self._updates_information_retrieved)
        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.check_updates)
        self.thread.start()

    def _updates_information_retrieved(self, result):
        self.thread.quit()
        if result['status'] == 'success' and result['should_update']:
            updates_dialog = UpdateDialog(their_version=result['their_version'])
            updates_dialog.exec()



class CheckUpdatesWorker(QObject):
    """
    Implements threading to fetch and parse version update information from the web.
    """
    threadResultsSignal = pyqtSignal(object, name="results")

    def __init__(self, host, url, current_version, parent=None):
        super().__init__(parent)
        self.url = url
        self.host = host
        self.current_version = current_version

    def _get_release_version(self, received):
        if not received['prerelease']:
            # tags should be in form of v0.71.1 or v1.2b etc.
            p = re.compile('v\.?\s?(.+)', flags=re.IGNORECASE)

            # Strip v and other letters
            their_version = p.search(received['tag_name']).group(1)
            my_version = p.search(self.current_version).group(1)

            return StrictVersion(their_version) > StrictVersion(my_version)

    def check_updates(self):
        try:
            connection = http.client.HTTPSConnection(self.host)
            headers = {'User-Agent': 'Kaira'}
            connection.request("GET", self.url, headers=headers)
            response = connection.getresponse()
            if response.status == 200:
                data = response.read().decode('utf-8')
                data = json.loads(data)
                should_update = self._get_release_version(data)
                self.threadResultsSignal.emit({'status': 'success', 'raw_data': data,
                                               'should_update': should_update,
                                               'their_version': data['tag_name']})
            else:
                raise Exception('Error ' + str(response.status))
        except Exception:
            self.threadResultsSignal.emit({'status': 'error'})
