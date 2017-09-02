import smtplib
import os
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from sacred.observers import RunObserver
from sacred.config.config_files import load_config_file
import outputHandler

def td_format(td_object):
    seconds = int(td_object.total_seconds())
    if seconds == 0:
        return "less than a second"

    periods = [
        ('year', 60 * 60 * 24 * 365),
        ('month', 60 * 60 * 24 * 30),
        ('day', 60 * 60 * 24),
        ('hour', 60 * 60),
        ('minute', 60),
        ('second', 1)
    ]

    strings = []
    for period_name, period_seconds in periods:
        if seconds >= period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            if period_value == 1:
                strings.append("%s %s" % (period_value, period_name))
            else:
                strings.append("%s %ss" % (period_value, period_name))

    return ", ".join(strings)

class MailObserver(RunObserver):

    @classmethod
    def from_config(cls, filename, repetitionNumber):
        d = load_config_file(filename)
        obs = None
        if 'server' in d and 'user' in d and 'password' in d:
            obs = cls(d['server'],d['user'],d['password'], d['csvFilename'])
        else:
            raise ValueError("Mail configuration file must contain "
                             "an entry for 'server', 'user' and 'password'!")
        for k in ['started_text', 'completed_text', 'interrupted_text', 'failed_text']:
            if k in d:
                setattr(obs, k, d[k])

        setattr(obs,'repetitionNumber',repetitionNumber)

        return obs

    def __init__(self, server, user, password, csvFilename):
        self.server = server
        self.user = user
        self.password = password
        self.csvFilename = csvFilename

        self.started_text = "*{config[title]}* " \
                            "started at {start_time} " \
                            "on host `{host_info[hostname]}` with configuration:\n{config}.\n\n"

        self.completed_text = "*{config[title]}* " \
            "completed after {elapsed_time}.`\n\n"
            
        self.interrupted_text = "*{config[title]}* " \
                                "interrupted after {elapsed_time}.\n\n"
        self.failed_text = ":x: *{config[title]}* failed after " \
                           "{elapsed_time} with `{error}`.\n\n"
        self.run = None
        self.message = ""
        self.result_files = []

    def get_started_text(self):
        return self.started_text.format(**self.run)

    def get_completed_text(self):
        return self.completed_text.format(**self.run)

    def get_interrupted_text(self):
        return self.interrupted_text.format(**self.run)

    def get_failed_text(self):
        return self.failed_text.format(**self.run)

    def started_event(self, ex_info, command, host_info, start_time,
                      config, meta_info, _id):
        self.run = {
            '_id': _id,
            'config': config,
            'start_time': start_time,
            'experiment': ex_info,
            'command': command,
            'host_info': host_info,
        }

        self.message += self.get_started_text()

    def completed_event(self, stop_time, result):
        if self.completed_text is None:
            return

        self.run['result'] = result
        self.run['stop_time'] = stop_time
        self.run['elapsed_time'] = td_format(stop_time -
                                             self.run['start_time'])

        self.message += self.get_completed_text()
        self.result_files = []

        for i in range(1, self.repetitionNumber+1):
            self.result_files.append(outputHandler.generateCSVFilename(self.csvFilename, i))

        self.send_mail()

    def interrupted_event(self, interrupt_time, status):
        if self.interrupted_text is None:
            return

        self.run['status'] = status
        self.run['interrupt_time'] = interrupt_time
        self.run['elapsed_time'] = td_format(interrupt_time -
                                             self.run['start_time'])

        self.message += self.get_interrupted_text()
        self.send_mail()

    def failed_event(self, fail_time, fail_trace):
        if self.failed_text is None:
            return

        self.run['fail_trace'] = fail_trace
        self.run['error'] = fail_trace[-1].strip()
        self.run['fail_time'] = fail_time
        self.run['elapsed_time'] = td_format(fail_time -
                                             self.run['start_time'])

        self.message += self.get_failed_text()
        self.send_mail()
            
    def send_mail(self):
        smtp = None
        if self.user:
            smtp = smtplib.SMTP_SSL(self.server)
            smtp.ehlo()
            smtp.login(self.user, self.password)
        else:
            smtp = smtplib.SMTP(self.server)
            smtp.ehlo()
            self.user="Test@example.org"

        msg = MIMEMultipart()
        msg['From'] = self.user
        msg['To'] = COMMASPACE.join(self.user)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = self.run['config']['title'] + " results"

        msg.attach(MIMEText(self.message))
        
        for f in self.result_files or []:
            if os.path.exists(f):
                with open(f, "rb") as fil:
                    part = MIMEApplication(
                        fil.read(),
                        Name=basename(f)
                    )
                    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
                    msg.attach(part)

        smtp.sendmail(self.user, self.user, msg.as_string())
        smtp.close()