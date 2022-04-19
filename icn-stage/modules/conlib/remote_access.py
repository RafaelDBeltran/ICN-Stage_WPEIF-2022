#
#	@author: Nelson Antonio Antunes Junior
#	@email: nelson.a.antunes at gmail.com
#	@date: (DD/MM/YYYY) 24/01/2017

import paramiko, paramiko.rsakey, io, scp, hashlib, os
import logging
from time import sleep

def MD5(filename):
	hash_md5 = hashlib.md5()
	with open(filename, "rb") as f:
		for chunk in iter(lambda: f.read(4096), b""):
			hash_md5.update(chunk)
	return hash_md5.hexdigest()


class Channel(object):
	def __init__(self, hostname, username=None, password=None,
		pkey=None, timeout=None):
		
		self.password = password
		self.ssh = paramiko.SSHClient()
		self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		if type(hostname) is bytes:
			self.hostname = hostname.decode('utf-8')
		else:
			self.hostname = hostname
		
		if type(username) is bytes:
			self.username = username.decode('utf-8')
		else:
			self.username = username
		
		self.timeout = timeout

		if type(password) is bytes:
			password = password.decode('utf-8')

		if type(pkey) is bytes:
			pkey = pkey.decode('utf-8')

		if password == '':
			password = None
		if pkey is None or pkey == "":
			self.pkey = None
		else:
			self.pkey = paramiko.rsakey.RSAKey(file_obj=io.StringIO(pkey), password=password)
			password = None
		
		self.path = "~/"
		try:
			logging.debug("Channel hostname: {}  username: {}   password: {}   pkey: {}   timeout: {} ".format(
				self.hostname,  self.username, self.password, self.pkey, self.timeout))

			self.ssh.connect(hostname=self.hostname, username=self.username,
				password=self.password, pkey=self.pkey, timeout=self.timeout)
			logging.debug('Channel connected! hostname: {} '.format(self.hostname))
			self.scp = scp.SCPClient(self.ssh.get_transport())

		except Exception as e:
			self.connected = False
			print('Channel Exception: {}'.format(e))
			raise e

		self.connected = True

	def _actual_path(self, path):
		return self.path+path

	def run(self, cmd, async_=False):
		if not self.connected:
			return None,None,None
		cmd = "cd %s; %s" % (self.path, cmd)

		if async_:
			return tuple(self.ssh.exec_command(cmd)[1:])

		_,stdout,stderr = self.ssh.exec_command(cmd)
		logging.debug("Channel.run()")
		logging.debug(stdout.readlines())
		logging.debug(stderr.readlines())
		stdout.channel.recv_exit_status()
		stderr.channel.recv_exit_status()

		return (stdout, stderr)

	def chkdir(self, path):
		stdout,_ = self.run("[ -d %s ]" % path)
		return stdout.channel.recv_exit_status() == 0

	def chkfile(self, path):
		stdout,_ = self.run("[ -f %s ]" % path)
		return stdout.channel.recv_exit_status() == 0

	def chdir(self, path):

		if type(path) is bytes:
			path = path.decode('utf-8')

		if path[-1] != "/":
			path += "/"

		if path[0] in ["/", "~"]:
			if self.chkdir(path):
				self.path = path
		else:
			if self.chkdir(path):
				self.path = self._actual_path(path)

	def mkdir(self, path):
		self.run("mkdir -p %s" % path)

	def _cmpfiles(self, local_path, remote_path):
		stdout,_ = self.run("md5sum %s" % remote_path)
		return stdout.read().decode('utf-8').split(' ', 1)[0] != str(MD5(local_path))

	def put(self, local_path, remote_path):
		logging.debug("Channel.put(local_path={}, remote_path={})".format(local_path, remote_path))
		local_path = local_path.replace('//','/')
		remote_path = remote_path.replace('//','/')
		if self.connected and os.path.isfile(local_path):
			if self.chkfile(self._actual_path(remote_path)):
				if self._cmpfiles(local_path, self._actual_path(remote_path)):
					self.scp.put(local_path,self._actual_path(remote_path))
					return True
			else:
				self.scp.put(local_path,self._actual_path(remote_path))
				return True
		
		return False


	def get(self, remote_path, local_path):
		if self.connected and self.chkfile(self._actual_path(remote_path)):
			if os.path.isfile(local_path):
				if self._cmpfiles(local_path, self._actual_path(remote_path)):
					self.scp.get(self._actual_path(remote_path),local_path)
					return True
			else:
				self.scp.get(self._actual_path(remote_path),local_path)
				return True
		return False

	def get_full_path(self, remote_path, local_path):
		if self.connected and self.chkfile(remote_path):
			if os.path.isfile(local_path):
				if self._cmpfiles(local_path, self._actual_path(remote_path)):
					self.scp.get(self._actual_path(remote_path),local_path)
					return True
			else:
				self.scp.get(remote_path, local_path)
				return True
		return False

	def close(self):
		if self.connected:
			return self.ssh.close()
		return None
