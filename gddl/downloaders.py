# Copyright (C) 2007 Free Software Foundation
# This is a modified file form https://github.com/coursera-dl/coursera-dl/blob/master/coursera/downloaders.py , Under LGPLv3+ License
# You may get a copy of the license here: https://github.com/coursera-dl/coursera-dl/blob/master/LICENSE

"""
Module for download-related classes and functions.

"""

import math
import os
import sys
import time
import requests

CHUNK_SIZE = 512000

class Downloader(object):
    def _start_download(self, url, filename, resume, file_size):
        """
        Actual method to download the given url to the given file.
        This method should be implemented by the subclass.
        """
        raise NotImplementedError("Subclasses should implement this")

    def download(self, url, filename, resume=False, file_size=None):
        """
        Download the given url to the given file. When the download
        is aborted by the user, the partially downloaded file is also removed.
        """

        try:
            self._start_download(url, filename, resume, file_size)
        except KeyboardInterrupt as e:
            # keep the file if resume is True
            if resume:
                print('\nKeyboard Interrupt - Exiting...')
            else:
                print('\nKeyboard Interrupt - Removing partial file: {}'.format(filename))
                try:
                    os.remove(filename)
                except OSError:
                    pass

def format_bytes(bytes):
    """
    Get human readable version of given bytes.
    Ripped from https://github.com/rg3/youtube-dl
    """
    if bytes is None:
        return '[Unknown Size]'
    if type(bytes) is str:
        bytes = float(bytes)
    if bytes == 0.0:
        exponent = 0
    else:
        exponent = int(math.log(bytes, 1024.0))
    suffix = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'][exponent]
    converted = float(bytes) / float(1024 ** exponent)
    return '{0:.2f}{1}'.format(converted, suffix)


class DownloadProgress(object):
    """
    Report download progress.
    Inspired by https://github.com/rg3/youtube-dl
    """

    def __init__(self, total):
        if total in [0, '0', None]:
            self._total = None
        else:
            self._total = int(total)

        self._current = 0
        self._start = 0
        self._now = 0
        self._from = 0

        self._finished = False

    def start(self, from_=0):
        self._now = time.time()
        self._start = self._now
        self._from = from_
        self._current = from_

    def stop(self):
        self._now = time.time()
        self._finished = True
        self._total = self._current
        self.report_progress()

    def read(self, bytes_):
        self._now = time.time()
        self._current += bytes_
        self.report_progress()

    def report(self, bytes_):
        self._now = time.time()
        self._current = bytes_ + self._from
        self.report_progress()

    def calc_percent(self):
        if self._total is None:
            return '--%'
        if self._total == 0:
            return '100% done'
        percentage = int(float(self._current) / float(self._total) * 100.0)
        done = int(percentage / 4)
        return '[{0: <25}] {1}%'.format(done * '=', percentage)

    def calc_speed(self):
        dif = self._now - self._start
        this_session = self._current - self._from
        if this_session <= 0 or dif < 0.001:  # One millisecond
            return '---b/s'
        return '{0}/s'.format(format_bytes(float(this_session) / dif))

    def report_progress(self):
        """Report download progress."""
        percent = self.calc_percent()
        total = format_bytes(self._total)
        done = format_bytes(self._current)

        speed = self.calc_speed()
        total_speed_report = '{0} at {1}'.format(total, speed)

        report = '\r{0: <31} {1} of {2: <27}'.format(percent, done, total_speed_report)

        if self._finished:
            print(report)
        else:
            print(report, end="")
        sys.stdout.flush()


class NativeDownloader(Downloader):
    """
    'Native' python downloader -- slower than the external downloaders.

    :param session: Requests session.
    """

    def __init__(self, session):
        self.session = session

    def _start_download(self, url, filename, resume=False, content_length=None):
        # resume has no meaning if the file doesn't exists!
        resume = resume and os.path.exists(filename)

        headers = {}
        filesize = None
        if resume:
            filesize = os.path.getsize(filename)
            headers['Range'] = 'bytes={}-'.format(filesize)
            print('Resume downloading: {}'.format(filename))
        else:
            print('Downloading {}'.format(filename))

        max_attempts = 3
        attempts_count = 0
        error_msg = ''
        while attempts_count < max_attempts:
            r = self.session.get(url, stream=True, headers=headers)

            if r.status_code != 200:
                # because in resume state we are downloading only a
                # portion of requested file, server may return
                # following HTTP codes:
                # 206: Partial Content
                # 416: Requested Range Not Satisfiable
                # which are OK for us.
                if resume and r.status_code == 206:
                    pass
                elif resume and r.status_code == 416:
                    print('{} already downloaded'.format(filename))
                    r.close()
                    return True

                elif r.status_code == 403:
                    print('Error Downloading.\nMaybe the file has been downloaded too many times.\nPlease wait some time and try again.')
                    return False
                
                else:
                    if r.reason:
                        error_msg = r.reason + ' ' + str(r.status_code)
                    else:
                        error_msg = 'HTTP Error ' + str(r.status_code)

                    wait_interval = 2 ** (attempts_count + 1)
                    msg = 'Error downloading ({0}), will retry in {1} seconds ...'
                    print(msg.format(error_msg, wait_interval))
                    time.sleep(wait_interval)
                    attempts_count += 1
                    continue

            if resume and r.status_code == 200:
                # if the server returns HTTP code 200 while we are in
                # resume mode, it means that the server does not support
                # partial downloads.
                print('The server is not supporting resume.')
                resume = False

            chunk_sz = CHUNK_SIZE
            progress = DownloadProgress(content_length)
            progress.start(filesize if resume else 0)
            f = open(filename, 'ab') if resume else open(filename, 'wb')
            while True:
                data = r.raw.read(chunk_sz, decode_content=True)
                if not data:
                    progress.stop()
                    break
                progress.report(r.raw.tell())
                f.write(data)
            f.close()
            r.close()
            return True
        
        if attempts_count == max_attempts:
            print('Can\'t download file ...')
            print(error_msg)
            return False
        
def get_downloader(session, args):
    return NativeDownloader(session)

